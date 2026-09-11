// Unico punto di contatto con il backend. Ogni errore diventa un ApiError
// con lo status HTTP, cosi' le pagine decidono cosa mostrare senza conoscere fetch.

import type { Game, LeaderboardEntry } from "./types";

// Senza NEXT_PUBLIC_API_URL il backend si assume sullo stesso host della pagina,
// porta 8000: cosi' l'app funziona anche aperta da un altro dispositivo in rete
// locale (http://192.168.x.x:3000), dove "localhost" sarebbe il dispositivo stesso.
function baseUrl(): string {
  if (process.env.NEXT_PUBLIC_API_URL) return process.env.NEXT_PUBLIC_API_URL;
  if (typeof window !== "undefined") return `${window.location.protocol}//${window.location.hostname}:8000`;
  return "http://localhost:8000";
}

export class ApiError extends Error {
  /** 0 = backend non raggiungibile (rete, server spento). */
  constructor(public readonly status: number, message: string) {
    super(message);
    this.name = "ApiError";
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${baseUrl()}${path}`, {
      ...init,
      headers: { "content-type": "application/json", ...init?.headers },
      cache: "no-store",
    });
  } catch {
    throw new ApiError(0, "Backend non raggiungibile");
  }

  if (!response.ok) {
    const detail = await response
      .json()
      .then((body: { detail?: unknown }) => body.detail)
      .catch(() => undefined);
    const message = typeof detail === "string" ? detail : `Errore ${response.status}`;
    throw new ApiError(response.status, message);
  }
  return response.json() as Promise<T>;
}

export function createGame(player: string): Promise<Game> {
  return request<Game>("/api/games", { method: "POST", body: JSON.stringify({ player }) });
}

export function getGame(id: string): Promise<Game> {
  return request<Game>(`/api/games/${id}`);
}

export function makeMove(id: string, tile: number): Promise<Game> {
  return request<Game>(`/api/games/${id}/moves`, { method: "POST", body: JSON.stringify({ tile }) });
}

export function pauseGame(id: string): Promise<Game> {
  return request<Game>(`/api/games/${id}/pause`, { method: "POST" });
}

export function resumeGame(id: string): Promise<Game> {
  return request<Game>(`/api/games/${id}/resume`, { method: "POST" });
}

export function getLeaderboard(limit = 10): Promise<LeaderboardEntry[]> {
  return request<LeaderboardEntry[]>(`/api/leaderboard?limit=${limit}`);
}

/** Messaggio leggibile per l'utente a partire da un errore qualsiasi. */
export function describeError(error: unknown): string {
  if (error instanceof ApiError) return error.message;
  return "Qualcosa e' andato storto";
}
