import Link from "next/link";
import LeaderboardSection from "@/components/LeaderboardSection";

export default function LeaderboardPage() {
  return (
    <>
      <LeaderboardSection />
      <Link href="/" className="btn btn--small">
        ← PLAY A GAME
      </Link>
    </>
  );
}
