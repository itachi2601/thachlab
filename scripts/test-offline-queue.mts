import assert from "node:assert/strict";
import {
  MAX_ATTEMPTS,
  MAX_QUEUE_ITEMS,
  enqueue,
  flushQueue,
  isNetworkError,
  pendingCount,
  readQueue,
  type QueueStorage,
  type SendResult,
} from "../lib/offline-queue";

function mem(): QueueStorage {
  const data = new Map<string, string>();
  return { getItem: (k) => data.get(k) ?? null, setItem: (k, v) => void data.set(k, v) };
}

async function main() {
  // thêm + trùng id
  let st = mem();
  assert.equal(enqueue({ id: "a", studentId: "s1", payload: { n: 1 } }, st), true);
  assert.equal(enqueue({ id: "a", studentId: "s1", payload: { n: 1 } }, st), true);
  assert.equal(pendingCount("s1", st), 1);
  assert.equal(pendingCount("s2", st), 0);

  // giới hạn số mục: từ chối, không xoá mục cũ
  st = mem();
  for (let i = 0; i < MAX_QUEUE_ITEMS; i++) assert.equal(enqueue({ id: "i" + i, studentId: "s", payload: 1 }, st), true);
  assert.equal(enqueue({ id: "over", studentId: "s", payload: 1 }, st), false);
  assert.equal(readQueue(st)[0].id, "i0");
  // giới hạn dung lượng
  st = mem();
  assert.equal(enqueue({ id: "big", studentId: "s", payload: "x".repeat(500_000) }, st), false);
  // storage hỏng
  assert.equal(enqueue({ id: "z", studentId: "s", payload: 1 }, null), false);
  const throwing: QueueStorage = {
    getItem: () => {
      throw new Error("blocked");
    },
    setItem: () => {
      throw new Error("blocked");
    },
  };
  assert.equal(enqueue({ id: "z", studentId: "s", payload: 1 }, throwing), false);
  assert.equal(pendingCount("s", throwing), 0);

  // xả tuần tự, chỉ mục của đúng học sinh
  st = mem();
  enqueue({ id: "1", studentId: "s1", payload: 1 }, st);
  enqueue({ id: "2", studentId: "s2", payload: 2 }, st);
  enqueue({ id: "3", studentId: "s1", payload: 3 }, st);
  const order: string[] = [];
  const sent = await flushQueue(
    "s1",
    async (it) => {
      order.push(it.id);
      return "ok" as SendResult;
    },
    st,
  );
  assert.equal(sent, 2);
  assert.deepEqual(order, ["1", "3"]);
  assert.deepEqual(
    readQueue(st).map((i) => i.id),
    ["2"],
  );

  // lỗi mạng: dừng, giữ nguyên, attempts không tăng
  st = mem();
  enqueue({ id: "1", studentId: "s", payload: 1 }, st);
  enqueue({ id: "2", studentId: "s", payload: 2 }, st);
  const seen: string[] = [];
  assert.equal(
    await flushQueue(
      "s",
      async (it) => {
        seen.push(it.id);
        return "network" as SendResult;
      },
      st,
    ),
    0,
  );
  assert.deepEqual(seen, ["1"]);
  assert.equal(readQueue(st).length, 2);
  assert.equal(readQueue(st)[0].attempts, 0);
  // send ném lỗi = coi như mạng
  assert.equal(
    await flushQueue(
      "s",
      async () => {
        throw new Error("x");
      },
      st,
    ),
    0,
  );
  assert.equal(readQueue(st).length, 2);

  // lỗi logic: tăng attempts, quá ngưỡng thì bỏ, mục sau vẫn được thử
  st = mem();
  enqueue({ id: "bad", studentId: "s", payload: 1 }, st);
  enqueue({ id: "good", studentId: "s", payload: 2 }, st);
  const send = async (it: { id: string }): Promise<SendResult> => (it.id === "bad" ? "logic" : "ok");
  assert.equal(await flushQueue("s", send, st), 1);
  assert.deepEqual(
    readQueue(st).map((i) => [i.id, i.attempts]),
    [["bad", 1]],
  );
  for (let i = 1; i < MAX_ATTEMPTS; i++) await flushQueue("s", send, st);
  assert.equal(readQueue(st).length, 0);

  // không chạy chồng
  st = mem();
  enqueue({ id: "1", studentId: "s", payload: 1 }, st);
  let calls = 0;
  const slow = async (): Promise<SendResult> => {
    calls++;
    await new Promise((r) => setTimeout(r, 20));
    return "ok";
  };
  const [r1, r2] = await Promise.all([flushQueue("s", slow, st), flushQueue("s", slow, st)]);
  assert.equal(calls, 1);
  assert.equal(r1 + r2, 1);

  // phân loại lỗi
  assert.equal(isNetworkError({ message: "TypeError: Failed to fetch" }), true);
  assert.equal(isNetworkError({ message: "Load failed" }), true);
  assert.equal(isNetworkError({ status: 503, message: "" }), true);
  assert.equal(isNetworkError({ status: 0 }), true);
  assert.equal(isNetworkError({ code: "42501", message: "new row violates row-level security policy" }), false);
  assert.equal(isNetworkError({ status: 400, message: "bad" }), false);
  assert.equal(isNetworkError(null), false);

  console.log("offline-queue: OK");
}
void main();
