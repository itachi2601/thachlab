"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { Camera, RotateCcw } from "lucide-react";

/**
 * components/scan/QrScannerCard.tsx
 *
 * Mở camera sau, quét mã QR của đề, trả nội dung mã cho trang gọi (`app/quet-ma`).
 *
 * Hai đường giải mã, vì không có cách nào chạy đủ mọi máy:
 *  1. `BarcodeDetector` — API sẵn có của Chrome/Edge/Opera (kể cả Chrome trên Android), nhanh
 *     và không tốn thêm byte nào.
 *  2. `jsqr` — tải CHẬM (`import()` trong lúc quét) cho Safari/iOS và Firefox, nơi `BarcodeDetector`
 *     chưa bật mặc định (MDN: Safari 17 để sau cờ, Firefox chưa có). Bộ giải mã này không nằm
 *     trong JS ban đầu của trang.
 *
 * Quy tắc thiết kế (docs/QUY-TAC-THIET-KE.md): D2 nút ≥ 44px, D3 hành động chính (Bật camera) ở
 * dưới khung ngắm trong tầm ngón tay, N1 màn chỉ một việc là quét, M2 chữ đủ tương phản, B4 không
 * hoạt hình lặp (chỉ vòng xoay báo đang mở camera lúc chờ).
 */

type DetectorLike = { detect(source: HTMLVideoElement): Promise<{ rawValue: string }[]> };
type DetectorCtor = new (options?: { formats?: string[] }) => DetectorLike;

/** Nạp bộ giải mã jsQR đúng một lần cho cả phiên (chỉ khi máy không có BarcodeDetector). */
let jsQrPromise: Promise<(typeof import("jsqr"))["default"]> | null = null;
function loadJsQr() {
  jsQrPromise ??= import("jsqr").then((mod) => mod.default);
  return jsQrPromise;
}

function messageFor(err: unknown): string {
  const name = err instanceof DOMException ? err.name : "";
  if (name === "NotAllowedError" || name === "SecurityError")
    return "Em chưa cho phép dùng camera. Bấm vào ổ khoá trên thanh địa chỉ → cho phép Camera, rồi thử lại.";
  if (name === "NotFoundError" || name === "OverconstrainedError")
    return "Không tìm thấy camera sau trên máy này. Em gõ mã đề ở ô bên dưới nhé.";
  if (name === "NotReadableError") return "Camera đang bị ứng dụng khác chiếm. Đóng ứng dụng đó rồi thử lại.";
  return "Không mở được camera. Em gõ mã đề ở ô bên dưới nhé.";
}

/** Thời gian giữa hai lần đọc khung hình — 5 lần/giây là đủ bắt mã, không nóng máy. */
const FRAME_MS = 200;

export default function QrScannerCard({ onResult }: { onResult: (text: string) => void }) {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const timerRef = useRef<number | null>(null);
  const detectorRef = useRef<DetectorLike | null>(null);
  const busyRef = useRef(false); // đang xử lý một khung — không chồng lên khung trước

  const [phase, setPhase] = useState<"idle" | "starting" | "scanning" | "error">("idle");
  const [error, setError] = useState("");

  const stop = useCallback(() => {
    if (timerRef.current !== null) {
      window.clearTimeout(timerRef.current);
      timerRef.current = null;
    }
    streamRef.current?.getTracks().forEach((t) => t.stop());
    streamRef.current = null;
    if (videoRef.current) videoRef.current.srcObject = null;
    setPhase("idle");
  }, []);

  const start = useCallback(async () => {
    setError("");
    setPhase("starting");
    if (!navigator.mediaDevices?.getUserMedia) {
      setPhase("error");
      setError("Trình duyệt này không cho mở camera (cần trang https). Em gõ mã đề ở ô bên dưới nhé.");
      return;
    }
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: { ideal: "environment" } },
        audio: false,
      });
      const video = videoRef.current;
      if (!video) {
        stream.getTracks().forEach((t) => t.stop());
        return;
      }
      streamRef.current = stream;
      video.srcObject = stream;
      await video.play();
      setPhase("scanning");

      const tick = async () => {
        timerRef.current = null;
        const el = videoRef.current;
        if (!el || busyRef.current) {
          timerRef.current = window.setTimeout(tick, FRAME_MS);
          return;
        }
        busyRef.current = true;
        try {
          const Ctor = (window as unknown as { BarcodeDetector?: DetectorCtor }).BarcodeDetector;
          if (Ctor) {
            detectorRef.current ??= new Ctor({ formats: ["qr_code"] });
            const codes = await detectorRef.current.detect(el);
            const value = codes[0]?.rawValue;
            if (value) {
              stop();
              onResult(value);
              return;
            }
          } else if (el.readyState >= 2 && el.videoWidth > 0) {
            const jsQR = await loadJsQr();
            const canvas = canvasRef.current ?? document.createElement("canvas");
            canvasRef.current = canvas;
            canvas.width = el.videoWidth;
            canvas.height = el.videoHeight;
            const ctx = canvas.getContext("2d", { willReadFrequently: true });
            if (ctx) {
              ctx.drawImage(el, 0, 0, canvas.width, canvas.height);
              const frame = ctx.getImageData(0, 0, canvas.width, canvas.height);
              const hit = jsQR(frame.data, canvas.width, canvas.height, { inversionAttempts: "dontInvert" });
              if (hit?.data) {
                stop();
                onResult(hit.data);
                return;
              }
            }
          }
        } catch {
          // Khung hình lỗi (máy đang lấy nét, tạm tối…) — bỏ qua, thử khung sau.
        } finally {
          busyRef.current = false;
        }
        timerRef.current = window.setTimeout(tick, FRAME_MS);
      };
      timerRef.current = window.setTimeout(tick, FRAME_MS);
    } catch (e) {
      streamRef.current?.getTracks().forEach((t) => t.stop());
      streamRef.current = null;
      setPhase("error");
      setError(messageFor(e));
    }
  }, [onResult, stop]);

  // Rời trang giữa lúc quét: tắt camera ngay, đừng để đèn camera sáng mãi.
  useEffect(() => stop, [stop]);

  return (
    <div className="space-y-3">
      <div className="relative mx-auto w-full max-w-sm overflow-hidden rounded-2xl border border-white/10 bg-black/60 aspect-square">
        <video
          ref={videoRef}
          playsInline
          muted
          autoPlay
          className={`h-full w-full object-cover ${phase === "scanning" ? "" : "opacity-0"}`}
        />
        {phase === "scanning" && (
          <div aria-hidden className="pointer-events-none absolute inset-0 flex items-center justify-center">
            <div className="h-3/5 w-3/5 rounded-2xl border-2 border-white/70" />
          </div>
        )}
        {phase !== "scanning" && (
          <div className="absolute inset-0 flex flex-col items-center justify-center gap-3 p-6 text-center">
            <Camera size={32} className="text-slate-400" />
            <p className="text-sm text-slate-400">
              {phase === "starting" ? "Đang mở camera…" : "Bấm nút bên dưới để mở camera và quét mã QR của đề."}
            </p>
          </div>
        )}
      </div>

      {phase === "scanning" ? (
        <p className="text-center text-sm text-slate-300">Đưa mã QR vào giữa khung, giữ máy cách khoảng 20–30 cm.</p>
      ) : (
        <button
          type="button"
          onClick={() => void start()}
          disabled={phase === "starting"}
          className="mx-auto flex min-h-12 w-full max-w-sm items-center justify-center gap-2 rounded-full bg-primary px-6 py-3 text-base font-semibold text-white hover:bg-primary-dark disabled:opacity-50"
        >
          {phase === "error" ? <RotateCcw size={17} /> : <Camera size={17} />}
          {phase === "starting" ? "Đang mở camera…" : phase === "error" ? "Thử lại" : "Bật camera để quét"}
        </button>
      )}

      {error && (
        <p role="alert" className="mx-auto max-w-sm text-center text-sm text-amber-300">
          {error}
        </p>
      )}
    </div>
  );
}
