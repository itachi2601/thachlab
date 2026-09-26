"use client";

import {
  useCallback,
  useEffect,
  useState,
  useSyncExternalStore,
} from "react";
import type { Session } from "@supabase/supabase-js";
import { getSupabase, supabaseConfigured } from "@/services/supabase";
import { AuthContext, type Profile, type PreviewMode } from "./auth-context";

// Types + context + hook useAuth giờ sống ở auth-context.tsx (không import supabase-js) —
// re-export ở đây để các file đang import từ "@/components/auth/AuthProvider" không phải
// sửa gì. Xem auth-context.tsx để biết lý do tách.
export { useAuth } from "./auth-context";
export type { Profile, PreviewMode } from "./auth-context";

const PREVIEW_STORAGE_KEY = "thachlab_preview_as_student";
const PREVIEW_EVENT = "thachlab-preview-change";

function subscribePreview(onChange: () => void) {
  window.addEventListener("storage", onChange);
  window.addEventListener(PREVIEW_EVENT, onChange);
  return () => {
    window.removeEventListener("storage", onChange);
    window.removeEventListener(PREVIEW_EVENT, onChange);
  };
}

function readPreview(): PreviewMode {
  try {
    const raw = sessionStorage.getItem(PREVIEW_STORAGE_KEY);
    if (raw === "1") return "student";
    if (raw === "cttc") return "cttc";
    return null;
  } catch {
    return null;
  }
}

export default function AuthProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [session, setSession] = useState<Session | null>(null);
  const [profile, setProfile] = useState<Profile | null>(null);
  const [loadedProfileUserId, setLoadedProfileUserId] = useState<string | null>(null);
  const [loading, setLoading] = useState(supabaseConfigured);
  const storedPreview = useSyncExternalStore(subscribePreview, readPreview, () => null);
  const [previewOverride, setPreviewOverride] = useState<PreviewMode | undefined>(undefined);
  const previewMode: PreviewMode = previewOverride === undefined ? storedPreview : previewOverride;
  const previewAsStudent = previewMode !== null;

  const setPreviewMode = useCallback((mode: PreviewMode) => {
    setPreviewOverride(mode);
    try {
      if (mode === "student") sessionStorage.setItem(PREVIEW_STORAGE_KEY, "1");
      else if (mode === "cttc") sessionStorage.setItem(PREVIEW_STORAGE_KEY, "cttc");
      else sessionStorage.removeItem(PREVIEW_STORAGE_KEY);
      window.dispatchEvent(new Event(PREVIEW_EVENT));
    } catch {
      // bỏ qua nếu không lưu được — preview vẫn hoạt động trong phiên hiện tại.
    }
  }, []);

  const setPreviewAsStudent = useCallback(
    (value: boolean) => setPreviewMode(value ? "student" : null),
    [setPreviewMode],
  );

  useEffect(() => {
    if (!supabaseConfigured) return;
    const supabase = getSupabase();

    supabase.auth.getSession().then(({ data }) => {
      setSession(data.session);
      if (!data.session) setLoading(false);
    });

    const { data: sub } = supabase.auth.onAuthStateChange((_e, s) => {
      setSession(s);
      if (!s) {
        setProfile(null);
        setLoadedProfileUserId(null);
        setLoading(false);
      }
    });
    return () => sub.subscription.unsubscribe();
  }, []);

  const loadProfile = useCallback(async (userId: string) => {
    const { data, error } = await getSupabase()
      .from("profiles")
      .select("id, full_name, class_name, role, admin_area, track, avatar_url")
      .eq("id", userId)
      .single();
    // Fallback nếu chưa chạy migration thêm cột admin_area/track/avatar_url (tránh khoá luôn tài khoản admin).
    if (error) {
      const { data: fallbackData } = await getSupabase()
        .from("profiles")
        .select("id, full_name, class_name, role")
        .eq("id", userId)
        .single();
      return fallbackData ? ({ ...fallbackData, admin_area: null, track: null, avatar_url: null } as Profile) : null;
    }
    return (data as Profile) ?? null;
  }, []);

  useEffect(() => {
    if (!session) return;
    let cancelled = false;
    loadProfile(session.user.id).then((result) => {
      if (cancelled) return;
      setProfile(result);
      setLoadedProfileUserId(session.user.id);
      setLoading(false);
    });
    return () => {
      cancelled = true;
    };
  }, [session, loadProfile]);

  const refreshProfile = useCallback(async () => {
    if (!session) return;
    const result = await loadProfile(session.user.id);
    setProfile(result);
  }, [session, loadProfile]);

  const signOut = useCallback(async () => {
    await getSupabase().auth.signOut();
  }, []);

  // Chỉ ghi đè khi role thật là admin — phòng trường hợp giá trị cũ còn sót trong
  // sessionStorage sau khi đăng xuất/đăng nhập tài khoản khác không phải admin.
  // Chế độ "cttc" ghi đè luôn track để /tai-khoan đi đúng nhánh sinh viên CTTC
  // (RPC preview_cttc_enroll đã ghi danh admin vào 3 môn, còn track thật thì giữ nguyên).
  const effectiveProfile: Profile | null =
    previewMode && profile?.role === "admin"
      ? { ...profile, role: "student", admin_area: null, track: previewMode === "cttc" ? "cttc" : profile.track }
      : profile;

  return (
    <AuthContext.Provider
      value={{
        session,
        profile: effectiveProfile,
        realProfile: profile,
        loading: loading || Boolean(session && loadedProfileUserId !== session.user.id),
        signOut,
        previewAsStudent,
        setPreviewAsStudent,
        previewMode,
        setPreviewMode,
        refreshProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}
