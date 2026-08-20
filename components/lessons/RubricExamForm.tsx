"use client";

import { AlertTriangle, Check } from "lucide-react";
import {
  RUBRIC_LEVELS,
  RUBRIC_LEVEL_LABEL,
  RUBRIC_LEVEL_PCT,
  gradeRubricExam,
  rubricMaxScore,
  type RubricDefinition,
  type RubricLevel,
} from "@/services/cnc-rubric";

export interface RubricExamFormProps {
  rubric: RubricDefinition;
  levels: Record<string, RubricLevel | undefined>;
  onLevelChange: (criterionId: string, level: RubricLevel) => void;
  zeroToleranceConfirmed: Record<number, boolean>;
  onZeroToleranceChange: (index: number, confirmed: boolean) => void;
  notes: string;
  onNotesChange: (notes: string) => void;
  readOnly?: boolean;
  referenceLevels?: Record<string, RubricLevel | undefined>;
  referenceLabel?: string;
}

export default function RubricExamForm({
  rubric, levels, onLevelChange, zeroToleranceConfirmed, onZeroToleranceChange,
  notes, onNotesChange, readOnly, referenceLevels, referenceLabel,
}: RubricExamFormProps) {
  const result = gradeRubricExam(rubric, levels, zeroToleranceConfirmed);

  return <div className="cnc-rubric-form">
    {rubric.groups.map((group) => {
      const groupMax = rubricMaxScore(rubric, group.id);
      const groupScore = result.groupScores[group.id] ?? 0;
      const gated = group.id === rubric.gatedGroupId;
      return <section key={group.id} className="cnc-rubric-group">
        <header>
          <h4>{group.title}</h4>
          <b>{groupScore.toFixed(2)} / {groupMax.toFixed(1)} điểm</b>
        </header>
        {gated && !result.gatePassed && (
          <p className="cnc-checklist-hint cnc-rubric-gate-warning">
            <AlertTriangle size={14} /> Nhóm {rubric.groups.find((g) => g.id === rubric.gateGroupId)?.title} chưa đạt ngưỡng {rubric.gateThreshold.toFixed(1)}đ nên nhóm này tạm không được tính điểm.
          </p>
        )}
        {group.criteria.map((criterion) => {
          const refLevel = referenceLevels?.[criterion.id];
          return <div key={criterion.id} className="cnc-rubric-criterion">
            <div className="cnc-rubric-criterion-head">
              <strong>{criterion.label}</strong>
              <span>{criterion.maxScore.toFixed(1)}đ</span>
            </div>
            {refLevel && (
              <p className="cnc-rubric-reference">{referenceLabel ?? "Tham khảo"}: <b>{refLevel} — {RUBRIC_LEVEL_LABEL[refLevel]}</b></p>
            )}
            <div className="cnc-rubric-levels">
              {RUBRIC_LEVELS.map((level) => {
                const selected = levels[criterion.id] === level;
                return <label key={level} className={`cnc-rubric-level ${selected ? "selected" : ""} ${readOnly ? "readonly" : ""}`}>
                  <input
                    type="radio"
                    name={criterion.id}
                    checked={selected}
                    disabled={readOnly}
                    onChange={() => onLevelChange(criterion.id, level)}
                  />
                  <span className="cnc-rubric-level-head">
                    <b>{level}</b><small>{RUBRIC_LEVEL_LABEL[level]} · {(RUBRIC_LEVEL_PCT[level] * criterion.maxScore).toFixed(2)}đ</small>
                  </span>
                  <p>{criterion.descriptors[level]}</p>
                </label>;
              })}
            </div>
          </div>;
        })}
      </section>;
    })}

    <section className="cnc-zero-tolerance">
      <header>
        <AlertTriangle size={20} />
        <div><strong>Lỗi loại trực tiếp (Zero-tolerance)</strong><p>Xác nhận không vi phạm đầy đủ {rubric.zeroTolerance.length} điều kiện dưới đây — vi phạm bất kỳ điều nào sẽ xếp loại Không đạt.</p></div>
      </header>
      {rubric.zeroTolerance.map((item, index) => <label key={item}>
        <input
          type="checkbox"
          disabled={readOnly}
          checked={Boolean(zeroToleranceConfirmed[index])}
          onChange={(event) => onZeroToleranceChange(index, event.target.checked)}
        />
        <i><Check size={13} /></i><span><b>{index + 1}</b>{item}</span>
      </label>)}
    </section>

    <label className="cnc-rubric-notes">
      <span>Nhận xét</span>
      <textarea
        value={notes}
        disabled={readOnly}
        onChange={(event) => onNotesChange(event.target.value)}
        placeholder="Ghi chú thêm về bài thi (nếu có)…"
        rows={3}
      />
    </label>

    <div className={`cnc-checklist-score ${result.xepLoai.startsWith("Không đạt") ? "" : "passed"}`}>
      <div><small>TỔNG ĐIỂM</small><strong>{result.totalScore.toFixed(2)}<span>/10.0</span></strong></div>
      <div className="cnc-checklist-status">
        <b>{result.xepLoai}</b>
        <p>KỸ THUẬT {(result.groupScores[rubric.gateGroupId] ?? 0).toFixed(2)}đ · THÀNH PHẦN {(result.groupScores[rubric.gatedGroupId] ?? 0).toFixed(2)}đ</p>
      </div>
    </div>
  </div>;
}
