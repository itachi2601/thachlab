/**
 * components/physics/FormulaPanel.tsx
 *
 * Thanh công thức, trượt/mờ dần khi bật "Hiện công thức". Dùng Framer Motion
 * vì đây là animation có điều kiện bật/tắt theo tương tác người dùng, không
 * phải animation liên tục theo thời gian (phần đó dành cho requestAnimationFrame).
 */

import { AnimatePresence, motion } from "framer-motion";
import { formatNumber } from "@/lib/physics";

export interface FormulaPanelProps {
  open: boolean;
  period: number;
  omega: number;
}

export function FormulaPanel({ open, period, omega }: FormulaPanelProps) {
  const formulas = [
    { expr: "T = 1/f", value: `${formatNumber(period, 2)} s` },
    { expr: "ω = 2πf", value: `${formatNumber(omega, 2)} rad/s` },
    { expr: "k = m(2πf)²", value: null },
  ];

  return (
    <AnimatePresence initial={false}>
      {open && (
        <motion.div
          key="formula-panel"
          initial={{ height: 0, opacity: 0 }}
          animate={{ height: "auto", opacity: 1 }}
          exit={{ height: 0, opacity: 0 }}
          transition={{ duration: 0.28, ease: [0.22, 1, 0.36, 1] }}
          className="overflow-hidden"
        >
          <div className="mt-3 flex flex-wrap items-center gap-x-2 gap-y-1 rounded-xl border border-white/10 bg-white/[0.03] px-3 py-2.5 font-mono text-xs text-slate-300 sm:text-sm">
            {formulas.map((f, i) => (
              <span key={f.expr} className="flex items-center gap-2">
                {i > 0 && <span className="text-slate-600">|</span>}
                <span>
                  {f.expr}
                  {f.value ? ` = ${f.value}` : ""}
                </span>
              </span>
            ))}
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
