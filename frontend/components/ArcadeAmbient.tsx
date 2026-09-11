// Decorazioni in fondo alla pagina: Pac-Man che pattuglia, due fantasmi,
// pellet che spariscono al suo passaggio. Solo CSS, nessuno stato.
// Nascoste con prefers-reduced-motion.
export default function ArcadeAmbient() {
  return (
    <>
      <div className="ambient" aria-hidden="true">
        <div className="dots" />
        <div className="eaten-l" />
        <div className="eaten-r" />
        <div className="pacman" />
        <div className="ghost ghost--red" />
        <div className="ghost ghost--cyan" />
      </div>
      <div className="scanlines" aria-hidden="true" />
    </>
  );
}
