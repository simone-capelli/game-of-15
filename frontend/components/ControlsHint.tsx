// Una riga discreta sotto la griglia. Il CSS mostra i tasti freccia solo su
// dispositivi con puntatore fine (mouse/trackpad) e "TAP" su quelli touch.
export default function ControlsHint() {
  return (
    <p className="hint" aria-label="Comandi">
      <span className="hint-keys">
        <kbd>←</kbd>
        <kbd>↑</kbd>
        <kbd>↓</kbd>
        <kbd>→</kbd>
        <span className="hint-sep">OR</span>
        CLICK A TILE
      </span>
      <span className="hint-touch">TAP A TILE TO SLIDE IT</span>
    </p>
  );
}
