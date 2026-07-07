"use client";

import {
  createContext,
  useCallback,
  useContext,
  useRef,
  useState,
} from "react";

interface ToastItem {
  id: number;
  kind: "success" | "error" | "info";
  text: string;
}

const ToastContext = createContext<(kind: ToastItem["kind"], text: string) => void>(
  () => {},
);

/** useToast()("success", "Đã lưu") — hiện thông báo nổi góc màn hình. */
export function useToast() {
  return useContext(ToastContext);
}

const COLORS: Record<ToastItem["kind"], string> = {
  success: "border-emerald-500/40 text-emerald-200",
  error: "border-red-500/40 text-red-200",
  info: "border-[#3B82F6]/40 text-slate-200",
};

const ICONS: Record<ToastItem["kind"], string> = {
  success: "✓",
  error: "✕",
  info: "ℹ",
};

export default function ToastProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [items, setItems] = useState<ToastItem[]>([]);
  const nextId = useRef(1);

  const push = useCallback((kind: ToastItem["kind"], text: string) => {
    const id = nextId.current++;
    setItems((prev) => [...prev, { id, kind, text }]);
    setTimeout(
      () => setItems((prev) => prev.filter((t) => t.id !== id)),
      3500,
    );
  }, []);

  return (
    <ToastContext.Provider value={push}>
      {children}
      <div className="pointer-events-none fixed bottom-5 right-5 z-100 flex w-80 flex-col gap-2">
        {items.map((t) => (
          <div
            key={t.id}
            className={`pointer-events-auto rounded-xl border bg-[#0B1020]/95 px-4 py-3 text-sm shadow-lg backdrop-blur-md ${COLORS[t.kind]}`}
          >
            <span className="mr-2 font-semibold">{ICONS[t.kind]}</span>
            {t.text}
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}
