"use client";

import { useRef, useState } from "react";
import { Camera, Loader2 } from "lucide-react";
import Avatar from "@/components/ui/Avatar";
import { useToast } from "@/components/ui/Toast";
import { useAuth } from "@/components/auth/AuthProvider";
import { updateMyAvatar } from "@/services/student-profile";

const MAX_FILE_SIZE = 8 * 1024 * 1024;

/** Avatar của chính học sinh, bấm vào để đổi ảnh — chỉ role student mới sửa được (RLS chặn phần còn lại). */
export default function AvatarUploader({
  studentId,
  url,
  name,
  size = 56,
}: {
  studentId: string;
  url?: string | null;
  name?: string | null;
  size?: number;
}) {
  const toast = useToast();
  const { refreshProfile } = useAuth();
  const inputRef = useRef<HTMLInputElement>(null);
  const [busy, setBusy] = useState(false);

  async function onPick(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    event.target.value = "";
    if (!file) return;
    if (file.size > MAX_FILE_SIZE) {
      toast("error", "Ảnh quá lớn — chọn ảnh dưới 8MB nhé.");
      return;
    }
    setBusy(true);
    try {
      await updateMyAvatar(studentId, file);
      await refreshProfile();
      toast("success", "Đã đổi ảnh đại diện.");
    } catch (error) {
      toast("error", error instanceof Error ? error.message : "Không đổi được ảnh, thử lại nhé.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <button
      type="button"
      onClick={() => inputRef.current?.click()}
      disabled={busy}
      aria-label="Đổi ảnh đại diện"
      className="group relative shrink-0 rounded-full disabled:opacity-60"
    >
      <Avatar url={url} name={name} size={size} />
      <span className="absolute inset-0 flex items-center justify-center rounded-full bg-black/50 opacity-0 transition-opacity group-hover:opacity-100">
        {busy ? <Loader2 size={size * 0.35} className="animate-spin text-white" /> : <Camera size={size * 0.35} className="text-white" />}
      </span>
      <input ref={inputRef} type="file" accept="image/png,image/jpeg,image/webp" onChange={onPick} className="hidden" />
    </button>
  );
}
