import Link from "next/link";
import { ArrowRight, GraduationCap, Wrench } from "lucide-react";

const entries = [
  {
    href: "/lop-hoc",
    icon: GraduationCap,
    title: "Học sinh THPT",
    desc: "KHTN 9 và Vật lý 10–12 theo chương trình GDPT 2018",
    tone: "bg-cyan-400/10 text-cyan-300",
  },
  {
    href: "/lop-hoc/cttc",
    icon: Wrench,
    title: "Sinh viên CTTC",
    desc: "Gia công CNC, Tiện – Phay truyền thống",
    tone: "bg-amber-400/10 text-amber-300",
  },
];

export default function AudienceChooser() {
  return (
    <section className="bg-[#05070B] px-6 pt-24 sm:pt-28 lg:px-12">
      <div className="mx-auto max-w-4xl">
        <p className="font-mono text-xs uppercase tracking-widest text-cyan-300">Bắt đầu từ đây</p>
        <h2 className="mt-2 font-display text-xl font-bold text-ink sm:text-2xl">Em đang học ở đâu?</h2>

        <div className="mt-5 grid divide-y divide-line overflow-hidden rounded-xl border border-line sm:grid-cols-2 sm:divide-x sm:divide-y-0">
          {entries.map((e) => (
            <Link
              key={e.href}
              href={e.href}
              className="group flex items-center gap-4 p-5 transition-colors hover:bg-white/[0.04]"
            >
              <span className={`grid h-11 w-11 shrink-0 place-items-center rounded-lg ${e.tone}`}>
                <e.icon size={22} />
              </span>
              <span className="min-w-0 flex-1">
                <strong className="block text-ink">{e.title}</strong>
                <span className="text-sm text-muted">{e.desc}</span>
              </span>
              <ArrowRight
                size={18}
                className="shrink-0 text-muted transition group-hover:translate-x-0.5 group-hover:text-cyan-300"
              />
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}
