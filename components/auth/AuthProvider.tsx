"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
  useSyncExternalStore,
} from "react";
import type { Session } from "@supabase/supabase-js";
import { getSupabase, supabaseConfigured } from "@/services/supabase";

export interface Profile {
  id: string;
  full_name: string;
  class_name: string;
  role: "student" | "admin" | "instructor";
  // Khu vực quản trị được phân công cho giảng viên (null = chưa được cấp vào /quan-tri).
  // Chỉ áp dụng cho role "instructor" — role "admin" luôn thấy cả 2 khu vực.
  admin_area: "thpt" | "cttc" | null;
}

interface AuthState {
  session: Session | null;
  /** Hồ sơ đang hiển thị cho phần còn lại của app — bị ghi đè khi admin bật "Xem như học sinh". */
  profile: Profile | null;
  /** Hồ sơ thật, không bị ghi đè — dùng để hiện nút bật preview (chỉ role thật = admin mới thấy). */
  realProfile: Profile | null;
  loading: boolean;
  signOut: () => Promise<void>;
  previewAsStudent: boolean;
  setPreviewAsStudent: (value: boolean) => void;
}

const AuthContext = createContext<AuthState>({
  session: null,
  profile: null,
  realProfile: null,
  loading: true,
  signOut: async () => {},
  previewAsStudent: false,
  setPreviewAsStudent: () => {},
});

export function useAuth() {
  return useContext(AuthContext);
}

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

function readPreview() {
  try {
    return sessionStorage.getItem(PREVIEW_STORAGE_KEY) === "1";
  } catch {
    return false;
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
  const storedPreview = useSyncExternalStore(subscribePreview, readPreview, () => false);
  const [previewOverride, setPreviewAsStudentState] = useState<boolean | null>(null);
  const previewAsStudent = previewOverride ?? storedPreview;

  const setPreviewAsStudent = useCallback((value: boolean) => {
    setPreviewAsStudentState(value);
    try {
      if (value) sessionStorage.setItem(PREVIEW_STORAGE_KEY, "1");
      else sessionStorage.removeItem(PREVIEW_STORAGE_KEY);
      window.dispatchEvent(new Event(PREVIEW_EVENT));
    } catch {
      // bỏ qua nếu không lưu được — preview vẫn hoạt động trong phiên hiện tại.
    }
  }, []);

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

  useEffect(() => {
    if (!session) return;
    let cancelled = false;
    getSupabase()
      .from("profiles")
      .select("id, full_name, class_name, role, admin_area")
      .eq("id", session.user.id)
      .single()
      .then(({ data, error }) => {
        if (cancelled) return;
        // Fallback nếu chưa chạy migration thêm cột admin_area (tránh khoá luôn tài khoản admin).
        if (error) {
          getSupabase()
            .from("profiles")
            .select("id, full_name, class_name, role")
            .eq("id", session.user.id)
            .single()
            .then(({ data: fallbackData }) => {
              if (!cancelled) {
                setProfile(fallbackData ? ({ ...fallbackData, admin_area: null } as Profile) : null);
                setLoadedProfileUserId(session.user.id);
                setLoading(false);
              }
            });
          return;
        }
        setProfile((data as Profile) ?? null);
        setLoadedProfileUserId(session.user.id);
        setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [session]);

  const signOut = useCallback(async () => {
    await getSupabase().auth.signOut();
  }, []);

  // Chỉ ghi đè khi role thật là admin — phòng trường hợp giá trị cũ còn sót trong
  // sessionStorage sau khi đăng xuất/đăng nhập tài khoản khác không phải admin.
  const effectiveProfile: Profile | null =
    previewAsStudent && profile?.role === "admin"
      ? { ...profile, role: "student", admin_area: null }
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
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}
