"use client";

import { useEffect, useState } from "react";
import type { Game } from "@/lib/types";
import { elapsedMs, formatMoves, formatTime, initials } from "@/lib/format";

// MOVES: 042 - TIME: 01:23. Il tempo deriva da created_at/pause del server,
// non da un contatore locale: sopravvive al refresh e coincide con la classifica.
export default function ScoreBar({ game }: { game: Game }) {
  const [now, setNow] = useState(() => Date.now());
  const running = !game.solved && game.paused_at === null;

  useEffect(() => {
    if (!running) return;
    const timer = setInterval(() => setNow(Date.now()), 250);
    return () => clearInterval(timer);
  }, [running]);

  return (
    <div className="scorebar" aria-live="off">
      <span className="player" title={game.player}>
        {initials(game.player)}
      </span>
      <span>
        MOVES: <b>{formatMoves(game.moves)}</b>
      </span>
      <span>
        TIME: <b>{formatTime(elapsedMs(game, now))}</b>
      </span>
    </div>
  );
}
