"use client";

import Modal from "@/components/ui/Modal";
import Button from "@/components/ui/Button";

/** Hộp thoại xác nhận dùng chung — thay window.confirm() bằng UI đồng bộ với giao diện. */
export default function ConfirmDialog({
  open,
  title,
  description,
  confirmLabel = "Đồng ý",
  cancelLabel = "Huỷ",
  onConfirm,
  onCancel,
}: {
  open: boolean;
  title: string;
  description?: string;
  confirmLabel?: string;
  cancelLabel?: string;
  onConfirm: () => void;
  onCancel: () => void;
}) {
  return (
    <Modal open={open} onClose={onCancel}>
      <h2 className="font-display text-lg font-semibold text-white">{title}</h2>
      {description && <p className="mt-2 text-sm text-slate-400">{description}</p>}
      <div className="mt-6 flex justify-end gap-2">
        <Button variant="outline" onClick={onCancel}>
          {cancelLabel}
        </Button>
        <Button variant="primary" onClick={onConfirm}>
          {confirmLabel}
        </Button>
      </div>
    </Modal>
  );
}
