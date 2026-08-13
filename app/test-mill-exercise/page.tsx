import millingExercises from "@/data/cnc/phay_bai345.json";

type FillBlankLevel = {
  part_ref: string;
  part_image_note: string;
  program_with_blanks: string[];
  blanks: Array<{ id: string; answer: string; note: string }>;
};

export default function TestMillExercise() {
  const exercise = millingExercises.exercises[0];
  const deLevel = exercise.levels?.[0] as FillBlankLevel;

  return (
    <div className="p-8 bg-white">
      <h1 className="text-2xl font-bold mb-4">{exercise.title}</h1>

      <div className="mb-6">
        <h2 className="font-bold text-lg mb-2">Mức dễ (de):</h2>
        <p className="text-sm text-gray-600 mb-4">{deLevel.part_ref}</p>

        <div className="bg-gray-100 rounded-lg overflow-hidden mb-4">
          <img
            src="/images/cnc/phay_bai3_de.png"
            alt="Bản vẽ chi tiết milling exercise"
            className="w-full max-h-96 object-contain"
          />
        </div>

        <p className="text-sm text-gray-700 mb-4">
          <strong>Gợi ý bản vẽ:</strong> {deLevel.part_image_note}
        </p>
      </div>

      <div className="mb-6">
        <h2 className="font-bold text-lg mb-2">Chương trình với ô trống:</h2>
        <pre className="bg-gray-900 text-green-400 p-4 rounded overflow-auto text-xs">
          {deLevel.program_with_blanks.join("\n")}
        </pre>
      </div>

      <div>
        <h2 className="font-bold text-lg mb-2">Các ô trống cần điền:</h2>
        <ul className="space-y-2">
          {deLevel.blanks.map((blank) => (
            <li key={blank.id} className="bg-amber-50 p-3 rounded text-sm">
              <strong>{blank.id}:</strong> {blank.answer} — {blank.note}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
