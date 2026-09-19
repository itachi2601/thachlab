import { notFound } from 'next/navigation';
import { Suspense } from 'react';
import { LocalPreviewRoute } from '@/components/tro-giang/LocalAssistantPreview';
export default function Page() {
  if (process.env.NODE_ENV !== 'development') notFound();
  return <Suspense fallback={<p className="p-5 text-slate-400">Đang mở mẫu…</p>}><LocalPreviewRoute/></Suspense>;
}
