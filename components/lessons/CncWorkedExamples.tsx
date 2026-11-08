"use client";

/**
 * Tab "Bài mẫu" của CNC Bài 2 (tiện) và Bài 3 (phay): chương trình giải sẵn từng block.
 * N6: ví dụ có lời giải trước Luyện tập, xen block bị che để tự đoán (fading).
 * N5: mỗi lần một ví dụ, chọn bằng chip. C2: lời giải trong cột ≤ 65ch. D1: thiết kế từ 375px.
 */
import { useState } from "react";
import { Eye, TriangleAlert } from "lucide-react";
import { cncWorkedExamples, type CncWorkedBlock, type CncWorkedExample } from "@/services/cnc-worked-examples";
import { CNC_WORKED_FIGURES } from "@/services/cnc-worked-examples-hinh";
import styles from "./CncWorkedExamples.module.css";

export default function CncWorkedExamples({ lessonId, onDone }: { lessonId: string; onDone?: () => void }) {
  const examples = cncWorkedExamples(lessonId);
  const [index, setIndex] = useState(0);
  const example = examples[index];
  if (!example) return null;
  const last = index === examples.length - 1;

  return (
    <div className={styles.root}>
      <p className={styles.lead}>
        Đọc từng block cùng lời giải. Gặp block bị che, tự viết ra giấy rồi mới bấm xem.
      </p>
      <div className={styles.chips} aria-label="Chọn ví dụ">
        {examples.map((item, i) => (
          <button
            key={item.id}
            type="button"
            aria-pressed={i === index}
            onClick={() => setIndex(i)}
          >
            VD{i + 1} · {item.level}
          </button>
        ))}
      </div>
      <Example key={example.id} example={example} number={index + 1} />
      <div className={styles.next}>
        {last ? (
          onDone && (
            <button type="button" className="lesson-btn" onClick={onDone}>
              Xong bài mẫu → sang Luyện tập
            </button>
          )
        ) : (
          <button type="button" className="lesson-btn" onClick={() => setIndex(index + 1)}>
            Ví dụ tiếp: VD{index + 2} →
          </button>
        )}
      </div>
    </div>
  );
}

function Example({ example, number }: { example: CncWorkedExample; number: number }) {
  return (
    <article className={styles.card}>
      <h3>
        VD{number}. {example.title}
      </h3>
      <p className={styles.task}>{example.task}</p>
      <figure
        className={styles.figure}
        dangerouslySetInnerHTML={{ __html: CNC_WORKED_FIGURES[example.figure] ?? "" }}
      />
      <dl className={styles.params}>
        {example.params.map(([label, value]) => (
          <div key={label}>
            <dt>{label}</dt>
            <dd>{value}</dd>
          </div>
        ))}
      </dl>
      <h4>Chương trình</h4>
      <ol className={styles.program}>
        {example.blocks.map((block) => (
          <Block key={block.code} block={block} />
        ))}
      </ol>
      {example.pitfalls.length > 0 && (
        <div className={styles.pitfalls}>
          <strong>
            <TriangleAlert size={16} aria-hidden /> Chỗ hay sai
          </strong>
          <ul>
            {example.pitfalls.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      )}
    </article>
  );
}

function Block({ block }: { block: CncWorkedBlock }) {
  const [shown, setShown] = useState(!block.ask);
  if (!shown) {
    const label = block.code.split(" ")[0];
    return (
      <li className={`${styles.block} ${styles.ask}`}>
        <code>{label} ?</code>
        <p>🤔 {block.ask}</p>
        <button type="button" className="lesson-btn-ghost" onClick={() => setShown(true)}>
          <Eye size={16} aria-hidden /> Tự viết xong, xem đáp án
        </button>
      </li>
    );
  }
  return (
    <li className={`${styles.block}${block.ask ? ` ${styles.revealed}` : ""}`}>
      <code>{block.code}</code>
      <p>{block.note}</p>
    </li>
  );
}
