type Props = {
  value: number; // 1..15
  index: number; // posizione attuale nella board
  movable: boolean;
  disabled: boolean; // chiamata in corso, partita chiusa o in pausa
  flash: boolean; // appena cliccata
  onClick: (tile: number) => void;
};

// Un <button> vero (focus, Invio/Spazio, disabled gratis), posizionato in
// assoluto dalla riga/colonna: quando l'indice cambia, il CSS lo fa scivolare.
export default function Tile({ value, index, movable, disabled, flash, onClick }: Props) {
  const placed = index === value - 1; // al posto giusto rispetto a GOAL
  const classes = ["tile", movable && "tile--movable", placed && "tile--placed", flash && "tile--flash"]
    .filter(Boolean)
    .join(" ");
  return (
    <button
      type="button"
      className={classes}
      style={{ "--row": Math.floor(index / 4), "--col": index % 4 } as React.CSSProperties}
      disabled={disabled || !movable}
      onClick={() => onClick(value)}
      aria-label={movable ? `Muovi la tessera ${value}` : `Tessera ${value}, non muovibile`}
    >
      <span className="tile-face">{value}</span>
    </button>
  );
}
