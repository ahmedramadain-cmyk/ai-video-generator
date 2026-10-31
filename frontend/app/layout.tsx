import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'مولد الفيديو بالذكاء الاصطناعي',
  description: 'منصة عربية لتوليد الفيديوهات من النصوص باستخدام AI',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ar" dir="rtl">
      <body>{children}</body>
    </html>
  );
}
