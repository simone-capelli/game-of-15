import type { Game } from "./types";

const pad2 = (n: number) => String(n).padStart(2, "0");

/** 83000 -> "01:23". Ore solo se servono: 3723000 -> "1:02:03". */
export function formatTime(ms: number): string {
  const totalSeconds = Math.max(0, Math.floor(ms / 1000));
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;
  return hours > 0 ? `${hours}:${pad2(minutes)}:${pad2(seconds)}` : `${pad2(minutes)}:${pad2(seconds)}`;
}

/** 42 -> "042", stile contatore arcade. */
export function formatMoves(moves: number): string {
  return String(moves).padStart(3, "0");
}

/** Prime tre lettere in maiuscolo, stile iniziali da high score. */
export function initials(player: string): string {
  return player.slice(0, 3).toUpperCase().padEnd(3, " ");
}

/**
 * Tempo di gioco "netto" in millisecondi, con la stessa formula del server:
 * (fine - inizio) - pause. Finche' la partita e' in corso, "fine" e' adesso;
 * se e' in pausa, il tempo si ferma all'inizio della pausa.
 */
export function elapsedMs(game: Game, now: number = Date.now()): number {
  if (game.duration_ms !== null) return game.duration_ms;
  const end = game.paused_at ? Date.parse(game.paused_at) : now;
  return Math.max(0, end - Date.parse(game.created_at) - game.paused_ms);
}
