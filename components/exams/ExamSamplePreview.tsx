"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import ContentHtml from "@/components/exams/ContentHtml";
import { useAuth } from "@/components/auth/AuthProvider";
import {
  examSampleLine,
  examSampleLoginHref,
  examSampleSignupHref,
  type ExamSample,
} from "@/components/home/exam-sample-types";

const LETTERS = ["A", "B", "C", "D"];

function readIdFromLocation(): number | null {
  if (typeof window === "undefined") return null;
  const raw = new URLSearchParams(window.location.search).get("id");
  return raw ? Number(raw) : null;
}

export default function ExamSamplePreview() {
  const { session, loading } = useAuth();
  const searchParams = useSearchParams();
  const [fallbackId, setFallbackId] = useState<number | null>(() => readIdFromLocation());
  const [samples, setSamples] = useState<ExamSample[] | null>(null);

  useEffect(() => {
    const sync = () => setFallbackId(readIdFromLocation());
    window.addEventListener("pageshow", sync);
    return () => window.removeEventListener("pageshow", sync);
  }, []);

  useEffect(() => {
    let cancelled = false;
    fetch("/data/exam-samples.json")
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (!cancelled) setSamples(Array.isArray(data?.samples) ? data.samples : []);
      })
      .catch(() => {
        if (!cancelled) setSamples([]);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const id = Number(searchParams.get("id")) || fallbackId || 0;
  const sample = samples?.find((item) => item.id === id) ?? null;

  if (samples === null) {
    return <p className="text-center text-base text-muted">Đang tải câu 1…</p>;
  }
  if (!sample) {
    return (
      <p className="text-center text-base text-ink">
        Không thấy đề mẫu này.{" "}
        <Link href="/#de-thi" className="text-primary hover:underline">
          Về trang chủ
        </Link>
      </p>
    );
  }

  const line = examSampleLine(sample);
  const primary = session
    ? { href: `/kiem-tra/lam?id=${sample.id}`, label: "Làm cả đề" }
    : { href: examSampleSignupHref(sample), label: "Đăng ký để lưu bài làm" };

  return (
    <div className="mx-auto max-w-3xl">
      <p className="text-base text-primary">Làm miễn phí</p>
      <h1 className="mt-2 font-display text-2xl font-bold leading-snug text-ink sm:text-3xl">{line}</h1>
      <p className="mt-2 text-base text-ink">
        {sample.questionCount} câu · {sample.durationMinutes} phút
      </p>

      <div className="mt-6">
        <SampleQuestion sample={sample} />
      </div>

      {loading ? (
        <p className="mt-6 text-base text-muted">Đang kiểm tra tài khoản…</p>
      ) : (
        <>
          <p className="mt-6 text-base leading-relaxed text-ink">
            {session
              ? "Đây là câu 1. Làm cả đề thì điểm được lưu."
              : "Đây là câu 1. Đăng ký để làm nốt đề và lưu bài làm."}
          </p>
          <Link
            href={primary.href}
            className="mt-4 flex min-h-12 items-center justify-center rounded-xl bg-primary px-5 text-base font-semibold text-white hover:bg-primary-dark"
          >
            {primary.label}
          </Link>
          {!session && (
            <p className="mt-3 text-center text-base text-ink">
              <Link href={examSampleLoginHref(sample)} className="text-primary hover:underline">
                Đã có tài khoản? Đăng nhập
              </Link>
            </p>
          )}
        </>
      )}
    </div>
  );
}

function SampleQuestion({ sample }: { sample: ExamSample }) {
  const q = sample.question;
  const [picked, setPicked] = useState<number | null>(null);
  const [flags, setFlags] = useState<Record<number, boolean | null>>({});

  return (
    <div className="rounded-2xl border border-line bg-panel p-5">
      <p className="exam-content text-base font-medium leading-relaxed text-ink">
        <span className="mr-1 font-semibold text-primary">Câu 1.</span>
        <ContentHtml html={q.question} />
      </p>

      {q.type === "multiple_choice" && (
        <div className="mt-4 grid gap-2">
          {(q.options ?? []).map((opt, index) => {
            const on = picked === index;
            return (
              <button
                key={index}
                type="button"
                onClick={() => setPicked(on ? null : index)}
                className={`flex min-h-11 items-start gap-3 rounded-xl border px-3 py-2.5 text-left text-base ${
                  on ? "border-primary bg-primary/15 text-ink" : "border-line bg-surface-2 text-ink"
                }`}
              >
                <span className="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-surface-2 text-sm font-semibold">
                  {LETTERS[index] ?? index + 1}
                </span>
                <ContentHtml html={opt} />
              </button>
            );
          })}
        </div>
      )}

      {q.type === "true_false" && (
        <ul className="mt-4 space-y-3">
          {(q.statements ?? []).map((statement, index) => (
            <li key={index} className="rounded-xl border border-line bg-surface-2 p-3">
              <p className="exam-content text-base text-ink">
                <ContentHtml html={statement.text} />
              </p>
              <div className="mt-2 flex gap-2">
                {[true, false].map((value) => {
                  const on = flags[index] === value;
                  return (
                    <button
                      key={String(value)}
                      type="button"
                      onClick={() => setFlags((cur) => ({ ...cur, [index]: on ? null : value }))}
                      className={`min-h-11 flex-1 rounded-lg border text-base font-semibold ${
                        on ? "border-primary bg-primary/15 text-ink" : "border-line text-ink"
                      }`}
                    >
                      {value ? "Đúng" : "Sai"}
                    </button>
                  );
                })}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
