"use client";

import { useCallback, useEffect, useState } from "react";

const LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
const SLOTS = 3;

type Props = {
  onConfirm: (initials: string) => void;
  pending: boolean;
};

// Tre lettere stile high score: frecce su/giu' per slot, oppure si digita.
// Tastiera: lettere scrivono e avanzano, sinistra/destra cambiano slot,
// su/giu' scorrono l'alfabeto, Invio conferma.
export default function InitialsPicker({ onConfirm, pending }: Props) {
  const [letters, setLetters] = useState(["A", "A", "A"]);
  const [active, setActive] = useState(0);

  const shift = useCallback((slot: number, delta: number) => {
    setLetters((prev) => {
      const next = [...prev];
      const i = (LETTERS.indexOf(prev[slot]) + delta + LETTERS.length) % LETTERS.length;
      next[slot] = LETTERS[i];
      return next;
    });
  }, []);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (pending) return;
      const key = e.key.toUpperCase();
      if (key.length === 1 && LETTERS.includes(key)) {
        setLetters((prev) => prev.map((l, i) => (i === active ? key : l)));
        setActive((a) => Math.min(a + 1, SLOTS - 1));
      } else if (e.key === "ArrowUp") shift(active, 1);
      else if (e.key === "ArrowDown") shift(active, -1);
      else if (e.key === "ArrowLeft") setActive((a) => Math.max(a - 1, 0));
      else if (e.key === "ArrowRight") setActive((a) => Math.min(a + 1, SLOTS - 1));
      else if (e.key === "Enter") onConfirm(letters.join(""));
      else return;
      e.preventDefault();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [active, letters, pending, shift, onConfirm]);

  return (
    <div className="section" role="group" aria-label="Scegli le tue iniziali">
      <p className="subtitle">ENTER YOUR INITIALS</p>
      <div className="initials">
        {letters.map((letter, slot) => (
          <div key={slot} className={`initials-slot${slot === active ? " initials-slot--active" : ""}`}>
            <button type="button" className="arrow" onClick={() => shift(slot, 1)} aria-label={`Lettera ${slot + 1} su`}>
              ▲
            </button>
            <button type="button" className="letter" onClick={() => setActive(slot)} aria-label={`Lettera ${slot + 1}: ${letter}`}>
              {letter}
            </button>
            <button type="button" className="arrow" onClick={() => shift(slot, -1)} aria-label={`Lettera ${slot + 1} giu'`}>
              ▼
            </button>
          </div>
        ))}
      </div>
      <button type="button" className="btn" onClick={() => onConfirm(letters.join(""))} disabled={pending}>
        {pending ? "..." : "START"}
      </button>
    </div>
  );
}
