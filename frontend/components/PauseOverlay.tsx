"use client";

import { useEffect } from "react";

type Props = {
  onResume: () => void;
  busy: boolean;
};

export default function PauseOverlay({ onResume, busy }: Props) {
  // Esc riprende: la pausa non deve intrappolare chi usa la tastiera.
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape" && !busy) onResume();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onResume, busy]);

  return (
    <div className="overlay" role="dialog" aria-modal="true" aria-labelledby="pause-title">
      <div className="overlay-box">
        <h2 id="pause-title">PAUSED</h2>
        <p className="subtitle">TIME IS FROZEN</p>
        <button type="button" className="btn" onClick={onResume} disabled={busy} autoFocus>
          RESUME
        </button>
      </div>
    </div>
  );
}
