"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import type { Game } from "@/lib/types";
import { ApiError, describeError, getGame, makeMove, pauseGame, resumeGame } from "@/lib/api";
import { formatMoves, formatTime, initials } from "@/lib/format";
import Board from "@/components/Board";
import ScoreBar from "@/components/ScoreBar";
import PauseOverlay from "@/components/PauseOverlay";
import ErrorMessage from "@/components/ErrorMessage";
import GoalPreview from "@/components/GoalPreview";
import ControlsHint from "@/components/ControlsHint";
import LeaderboardSection from "@/components/LeaderboardSection";

type Props = { id: string };

// Freccia -> quale tessera scivolerebbe nel vuoto. UP spinge in su la tessera
// SOTTO il vuoto, ecc. E' solo una mappa direzione -> tessera: la legalita'
// resta decisa dal server (si invia solo se e' tra i `movable` ricevuti).
const ARROW_OFFSET: Record<string, { di: number; guard: (row: number, col: number) => boolean }> = {
  ArrowUp: { di: 4, guard: (row) => row < 3 },
  ArrowDown: { di: -4, guard: (row) => row > 0 },
  ArrowLeft: { di: 1, guard: (_, col) => col < 3 },
  ArrowRight: { di: -1, guard: (_, col) => col > 0 },
};

function tileForArrow(board: number[], key: string): number | null {
  const arrow = ARROW_OFFSET[key];
  if (!arrow) return null;
  const blank = board.indexOf(0);
  const row = Math.floor(blank / 4);
  const col = blank % 4;
  return arrow.guard(row, col) ? board[blank + arrow.di] : null;
}

export default function GameScreen({ id }: Props) {
  const [game, setGame] = useState<Game | null>(null);
  const [loadError, setLoadError] = useState<ApiError | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);
  const [showGoal, setShowGoal] = useState(false);

  // Lo stato vive sul server: al mount (e a ogni refresh) si ricarica da GET.
  useEffect(() => {
    getGame(id)
      .then(setGame)
      .catch((err) => setLoadError(err instanceof ApiError ? err : new ApiError(0, describeError(err))));
  }, [id]);

  // Fantasmi "spaventati" (blu) mentre la partita e' vinta.
  useEffect(() => {
    if (game?.solved) document.documentElement.dataset.win = "1";
    return () => {
      delete document.documentElement.dataset.win;
    };
  }, [game?.solved]);

  // Tutte le azioni passano di qui: una sola chiamata in volo alla volta,
  // e la board mostrata e' sempre l'ultima risposta del server.
  const run = useCallback(
    async (action: () => Promise<Game>) => {
      if (pending) return;
      setPending(true);
      setActionError(null);
      try {
        setGame(await action());
      } catch (err) {
        setActionError(describeError(err));
        // 409 = lo stato sul server e' cambiato (chiusa/in pausa): riallineo la griglia.
        if (err instanceof ApiError && err.status === 409) {
          getGame(id).then(setGame).catch(() => undefined);
        }
      } finally {
        setPending(false);
      }
    },
    [pending, id],
  );

  const onMove = useCallback((tile: number) => run(() => makeMove(id, tile)), [run, id]);
  const onPause = useCallback(() => run(() => pauseGame(id)), [run, id]);
  const onResume = useCallback(() => run(() => resumeGame(id)), [run, id]);

  const paused = game?.paused_at != null;
  const playable = !!game && !game.solved && !paused && !pending;

  // Frecce: muovono la tessera adiacente al vuoto nella direzione premuta.
  useEffect(() => {
    if (!playable) return;
    const onKey = (e: KeyboardEvent) => {
      const tile = tileForArrow(game.board, e.key);
      if (tile === null) return;
      e.preventDefault();
      if (game.movable.includes(tile)) onMove(tile);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [playable, game, onMove]);

  if (loadError) {
    const message = loadError.status === 404 ? "GAME NOT FOUND (SERVER RESTARTED?)" : loadError.message.toUpperCase();
    return <ErrorMessage message={message} homeLink />;
  }
  if (!game) return <p className="subtitle">LOADING...</p>;

  return (
    <>
      <ScoreBar game={game} />

      {game.solved && (
        <div className="win" role="status">
          <h2 className="win-title">YOU WIN!</h2>
          <p className="subtitle">
            {initials(game.player)} — {formatMoves(game.moves)} MOVES IN {formatTime(game.duration_ms ?? 0)}
          </p>
        </div>
      )}

      <Board board={game.board} movable={game.movable} locked={!playable} won={game.solved} onMove={onMove} />
      {!game.solved && <ControlsHint />}

      {actionError && <ErrorMessage message={actionError.toUpperCase()} />}

      <div className="controls">
        {!game.solved && (
          <button type="button" className="btn btn--small" onClick={onPause} disabled={pending || paused}>
            PAUSE
          </button>
        )}
        <button type="button" className="btn btn--small" onClick={() => setShowGoal((s) => !s)} aria-pressed={showGoal}>
          GOAL
        </button>
        <Link href="/" className="btn btn--small">
          NEW GAME
        </Link>
      </div>
      {showGoal && <GoalPreview />}

      <LeaderboardSection player={game.player} refreshKey={game.solved} />

      {paused && <PauseOverlay onResume={onResume} busy={pending} />}
    </>
  );
}
