"use client";

export default function SegmentedControl<T extends string>({
  label,
  value,
  onChange,
  options,
}: {
  label: string;
  value: T;
  onChange: (value: T) => void;
  options: readonly (readonly [T, string])[];
}) {
  return (
    <div role="tablist" aria-label={label} className="inline-flex max-w-full overflow-x-auto rounded-xl border border-line bg-panel-deep p-1">
      {options.map(([id, text]) => (
        <button
          key={id}
          role="tab"
          aria-selected={value === id}
          onClick={() => onChange(id)}
          className={`shrink-0 rounded-lg px-4 py-2 text-sm font-bold ${value === id ? "bg-blue-600 text-white" : "text-muted hover:text-primary"}`}
        >
          {text}
        </button>
      ))}
    </div>
  );
}
