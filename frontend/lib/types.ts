// Contratto con il backend: vedi "Contratto API" nel README della root.

export type Game = {
  id: string;
  player: string;
  board: number[]; // 16 numeri letti per righe, 0 = casella vuota
  moves: number;
  solved: boolean;
  created_at: string; // ISO 8601
  finished_at: string | null;
  duration_ms: number | null;
  paused_ms: number; // pausa gia' scontata dal tempo
  paused_at: string | null; // se in pausa adesso, da quando
  movable: number[]; // tessere cliccabili adesso
};

export type LeaderboardEntry = {
  rank: number;
  player: string;
  game_id: string;
  moves: number;
  duration_ms: number;
  finished_at: string;
};
