"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
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
  profile: Profile | null;
  loading: boolean;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthState>({
  session: null,
  profile: null,
  loading: true,
  signOut: async () => {},
});

export function useAuth() {
  return useContext(AuthContext);
}

export default function AuthProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [session, setSession] = useState<Session | null>(null);
  const [profile, setProfile] = useState<Profile | null>(null);
  const [loading, setLoading] = useState(supabaseConfigured);

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
                setLoading(false);
              }
            });
          return;
        }
        setProfile((data as Profile) ?? null);
        setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [session]);

  const signOut = useCallback(async () => {
    await getSupabase().auth.signOut();
  }, []);

  return (
    <AuthContext.Provider value={{ session, profile, loading, signOut }}>
      {children}
    </AuthContext.Provider>
  );
}
