// Miniatura della configurazione vinta, per ricordare sempre l'obiettivo.
const GOAL = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0];

export default function GoalPreview() {
  return (
    <div className="section" style={{ gap: "0.3rem" }}>
      <span className="subtitle">GOAL</span>
      <div className="goal" aria-label="Configurazione da raggiungere">
        {GOAL.map((v) => (
          <span key={v}>{v === 0 ? "" : v}</span>
        ))}
      </div>
    </div>
  );
}
