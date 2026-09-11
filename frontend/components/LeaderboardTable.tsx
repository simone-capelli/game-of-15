import type { LeaderboardEntry } from "@/lib/types";
import { formatMoves, formatTime, initials } from "@/lib/format";

type Props = {
  entries: LeaderboardEntry[];
  highlightPlayer?: string | null; // la riga del giocatore corrente
};

export default function LeaderboardTable({ entries, highlightPlayer }: Props) {
  if (entries.length === 0) {
    return <p className="subtitle">NO SCORES YET. BE THE FIRST!</p>;
  }
  return (
    <table className="scores">
      <thead>
        <tr>
          <th>RANK</th>
          <th>NAME</th>
          <th className="num">MOVES</th>
          <th className="num">TIME</th>
        </tr>
      </thead>
      <tbody>
        {entries.map((entry) => (
          <tr key={entry.game_id} className={entry.player === highlightPlayer ? "mine" : undefined}>
            <td>{entry.rank}.</td>
            <td title={entry.player}>{initials(entry.player)}</td>
            <td className="num">{formatMoves(entry.moves)}</td>
            <td className="num">{formatTime(entry.duration_ms)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
