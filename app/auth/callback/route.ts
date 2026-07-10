import { NextRequest, NextResponse } from "next/server";
import { getSupabase } from "@/services/supabase";

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const code = searchParams.get("code");
  const userType = searchParams.get("type") || "student";

  if (!code) {
    return NextResponse.redirect(new URL("/dang-nhap", request.url));
  }

  try {
    const supabase = getSupabase();
    const { error } = await supabase.auth.exchangeCodeForSession(code);

    if (error) {
      return NextResponse.redirect(
        new URL(`/dang-nhap?error=${encodeURIComponent(error.message)}`, request.url)
      );
    }

    // Redirect to appropriate page based on user type
    const redirectPath = userType === "teacher" ? "/quan-tri" : "/dashboard";
    return NextResponse.redirect(new URL(redirectPath, request.url));
  } catch (err) {
    return NextResponse.redirect(
      new URL(`/dang-nhap?error=Authentication failed`, request.url)
    );
  }
}
