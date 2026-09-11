import NewGameForm from "@/components/NewGameForm";
import LeaderboardSection from "@/components/LeaderboardSection";

export default function HomePage() {
  return (
    <>
      <section className="section">
        <p className="subtitle">SLIDE THE TILES INTO ORDER. FEWER MOVES, LESS TIME.</p>
        <NewGameForm />
      </section>
      <LeaderboardSection />
    </>
  );
}
