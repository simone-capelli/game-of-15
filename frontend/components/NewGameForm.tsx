"use client";

import { useCallback, useState } from "react";
import { useRouter } from "next/navigation";
import { createGame, describeError } from "@/lib/api";
import InitialsPicker from "./InitialsPicker";
import ErrorMessage from "./ErrorMessage";

export const LAST_PLAYER_KEY = "puzzle15:lastPlayer";

// PLAY A GAME -> iniziali -> START. Il nome (1-32 caratteri per il backend,
// qui sempre 3 lettere) e' obbligatorio: senza non si chiama il server.
export default function NewGameForm() {
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const start = useCallback(
    async (player: string) => {
      if (pending || player.trim().length === 0) return;
      setPending(true);
      setError(null);
      try {
        const game = await createGame(player);
        try {
          localStorage.setItem(LAST_PLAYER_KEY, player);
        } catch {
          /* storage non disponibile: la classifica non evidenzia nessuno */
        }
        router.push(`/game/${game.id}`);
      } catch (err) {
        setError(describeError(err));
        setPending(false);
      }
    },
    [pending, router],
  );

  if (!open) {
    return (
      <button type="button" className="btn btn--coin" onClick={() => setOpen(true)}>
        PLAY A GAME
      </button>
    );
  }

  return (
    <div className="section">
      <InitialsPicker onConfirm={start} pending={pending} />
      {error && <ErrorMessage message={error} />}
    </div>
  );
}
