import type { Metadata } from "next";
import Link from "next/link";
import { Press_Start_2P } from "next/font/google";
import ArcadeAmbient from "@/components/ArcadeAmbient";
import "./globals.css";

const pixel = Press_Start_2P({
  weight: "400",
  subsets: ["latin"],
  variable: "--font-pixel",
  display: "swap",
});

export const metadata: Metadata = {
  title: "15 Puzzle",
  description: "Griglia 4x4, 15 tessere, una casella vuota. Stile arcade.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="it" className={pixel.variable}>
      {/* suppressHydrationWarning: estensioni del browser (es. ColorZilla) aggiungono
          attributi al body prima che React parta; non e' un errore nostro. */}
      <body suppressHydrationWarning>
        <main className="screen">
          <h1 className="title">
            <Link href="/">15 PUZZLE</Link>
          </h1>
          {children}
        </main>
        <ArcadeAmbient />
      </body>
    </html>
  );
}
