function isHeic(file: File) {
  return /^image\/hei[cf]$/i.test(file.type) || /\.hei[cf]$/i.test(file.name);
}

// iPhone camera photos default to HEIC, which most non-Safari browsers can't decode
// via createImageBitmap — convert to JPEG first so viewers everywhere can open it.
async function decodeHeicToJpeg(file: File): Promise<Blob> {
  const heic2any = (await import("heic2any")).default;
  const result = await heic2any({ blob: file, toType: "image/jpeg", quality: 0.9 });
  return Array.isArray(result) ? result[0] : result;
}

export async function compressImageFile(file: File, { maxDimension = 1600, quality = 0.8 } = {}): Promise<File> {
  const heic = isHeic(file);
  let source: File | Blob = file;
  if (heic) {
    try {
      source = await decodeHeicToJpeg(file);
    } catch {
      return file;
    }
  } else if (!file.type.startsWith("image/") || file.type === "image/gif" || file.type === "image/svg+xml") {
    return file;
  }

  const jpegName = `${file.name.replace(/\.[^.]+$/, "")}.jpg`;
  let bitmap: ImageBitmap;
  try {
    bitmap = await createImageBitmap(source);
  } catch {
    return heic ? new File([source], jpegName, { type: "image/jpeg" }) : file;
  }
  const scale = Math.min(1, maxDimension / Math.max(bitmap.width, bitmap.height));
  const width = Math.round(bitmap.width * scale);
  const height = Math.round(bitmap.height * scale);
  const canvas = document.createElement("canvas");
  canvas.width = width;
  canvas.height = height;
  const ctx = canvas.getContext("2d");
  if (!ctx) {
    bitmap.close();
    return heic ? new File([source], jpegName, { type: "image/jpeg" }) : file;
  }
  ctx.drawImage(bitmap, 0, 0, width, height);
  bitmap.close();
  const blob = await new Promise<Blob | null>((resolve) => canvas.toBlob(resolve, "image/jpeg", quality));
  if (!blob || (!heic && blob.size >= file.size)) return heic ? new File([source], jpegName, { type: "image/jpeg" }) : file;
  return new File([blob], jpegName, { type: "image/jpeg" });
}
