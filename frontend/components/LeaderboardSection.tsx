"use client";

import { useEffect, useState } from "react";
import type { LeaderboardEntry } from "@/lib/types";
import { describeError, getLeaderboard } from "@/lib/api";
import LeaderboardTable from "./LeaderboardTable";
import ErrorMessage from "./ErrorMessage";
import { LAST_PLAYER_KEY } from "./NewGameForm";

type Props = {
  player?: string | null; // se noto (pagina partita); altrimenti l'ultimo usato
  refreshKey?: unknown; // cambia -> ricarica (es. dopo una vittoria)
};

function readLastPlayer(): string | null {
  try {
    return localStorage.getItem(LAST_PLAYER_KEY);
  } catch {
    return null; // storage non disponibile
  }
}

// HIGH SCORES: usata da home, pagina partita e /leaderboard.
export default function LeaderboardSection({ player, refreshKey }: Props) {
  const [entries, setEntries] = useState<LeaderboardEntry[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [lastPlayer, setLastPlayer] = useState<string | null>(null);

  useEffect(() => {
    getLeaderboard(10)
      .then((data) => {
        setEntries(data);
        // letto qui (dopo il mount) per non differire tra server e client
        setLastPlayer(readLastPlayer());
      })
      .catch((err) => setError(describeError(err)));
  }, [refreshKey]);

  return (
    <section className="section">
      <h2 className="section-title">HIGH SCORES</h2>
      {error ? (
        <ErrorMessage message={error} />
      ) : entries === null ? (
        <p className="subtitle">LOADING...</p>
      ) : (
        <LeaderboardTable entries={entries} highlightPlayer={player ?? lastPlayer} />
      )}
    </section>
  );
}
