import type { SupabaseClient } from "@supabase/supabase-js";

const BUCKET = "lesson-media";

/** Tên file an toàn cho Storage (bỏ dấu, chỉ a-z 0-9 _ -). */
export function safeFileName(name: string): string {
  const ext = name.includes(".") ? `.${name.split(".").pop()}` : "";
  const stem = name
    .replace(/\.[^.]+$/, "")
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/[^a-zA-Z0-9_-]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .toLowerCase();
  return `${stem || "hinh"}${ext.toLowerCase()}`;
}

const MIME_BY_EXT: Record<string, string> = {
  png: "image/png",
  jpg: "image/jpeg",
  jpeg: "image/jpeg",
  webp: "image/webp",
  gif: "image/gif",
  svg: "image/svg+xml",
};

export interface RasterImageInput {
  /** tên file gốc, vd "thi-nghiem-brown.jpg" */
  name: string;
  /** data URI base64: "data:image/jpeg;base64,..." */
  dataUri: string;
  /** token trong HTML sẽ được thay bằng URL công khai, vd "media/thi-nghiem-brown.jpg" */
  placeholder: string;
}

export interface UploadedMedia {
  placeholder: string;
  url: string;
  storagePath: string;
}

function dataUriToBytes(dataUri: string): { bytes: Uint8Array; mime: string } {
  const m = dataUri.match(/^data:([^;,]+)?(;base64)?,([\s\S]*)$/);
  if (!m) throw new Error("data URI không hợp lệ");
  const mime = m[1] || "application/octet-stream";
  const isB64 = !!m[2];
  const raw = isB64
    ? (typeof atob === "function"
        ? atob(m[3])
        : Buffer.from(m[3], "base64").toString("binary"))
    : decodeURIComponent(m[3]);
  const bytes = new Uint8Array(raw.length);
  for (let i = 0; i < raw.length; i++) bytes[i] = raw.charCodeAt(i);
  return { bytes, mime };
}

/**
 * Upload các ảnh raster của một bài học lên bucket `lesson-media`.
 * Trả về danh sách { placeholder, url } để caller thay chuỗi trong HTML.
 * Nhận `client` (browser dùng phiên admin, script dùng service-role) để tái sử dụng.
 */
export async function uploadLessonMedia(
  client: SupabaseClient,
  lessonId: number,
  images: RasterImageInput[],
): Promise<UploadedMedia[]> {
  const done: UploadedMedia[] = [];
  for (const img of images) {
    const { bytes, mime } = dataUriToBytes(img.dataUri);
    const fileName = safeFileName(img.name);
    const ext = fileName.split(".").pop()?.toLowerCase() ?? "";
    const contentType = MIME_BY_EXT[ext] ?? mime;
    const storagePath = `${lessonId}/${Date.now()}-${fileName}`;
    const { error } = await client.storage
      .from(BUCKET)
      .upload(storagePath, bytes, { contentType, upsert: false });
    if (error) {
      // rollback những cái đã lên
      if (done.length) await client.storage.from(BUCKET).remove(done.map((d) => d.storagePath));
      throw new Error(`Upload "${img.name}" thất bại: ${error.message}`);
    }
    const { data } = client.storage.from(BUCKET).getPublicUrl(storagePath);
    done.push({ placeholder: img.placeholder, url: data.publicUrl, storagePath });
  }
  return done;
}

export async function removeLessonMedia(client: SupabaseClient, storagePaths: string[]) {
  if (storagePaths.length) await client.storage.from(BUCKET).remove(storagePaths);
}

/** Thay mọi token placeholder trong một chuỗi HTML bằng URL công khai. */
export function applyMediaUrls(html: string, media: UploadedMedia[]): string {
  let out = html;
  for (const m of media) out = out.split(m.placeholder).join(m.url);
  return out;
}
