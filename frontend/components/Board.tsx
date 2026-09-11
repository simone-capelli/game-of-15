"use client";

import { useState } from "react";
import Tile from "./Tile";

type Props = {
  board: number[]; // 16 numeri letti per righe, 0 = vuoto
  movable: number[]; // dal server: il frontend non lo ricalcola
  locked: boolean;
  won: boolean;
  onMove: (tile: number) => void;
};

const FLASH_MS = 150;

export default function Board({ board, movable, locked, won, onMove }: Props) {
  const [flashing, setFlashing] = useState<number | null>(null);
  const blank = board.indexOf(0);

  function handleClick(tile: number) {
    setFlashing(tile);
    setTimeout(() => setFlashing(null), FLASH_MS);
    onMove(tile);
  }

  const classes = ["board", locked && !won && "board--locked", won && "board--win"].filter(Boolean).join(" ");

  return (
    <div className="board-wrap">
      <div className={classes} aria-label="Griglia 4x4">
        <div className="board-inner">
          <div
            className="slot-empty"
            aria-hidden="true"
            style={{ "--row": Math.floor(blank / 4), "--col": blank % 4 } as React.CSSProperties}
          >
            <i />
            <i />
            <i />
            <i />
          </div>
          {board.map((value, index) =>
            value === 0 ? null : (
              <Tile
                // chiave = tessera, non indice: React tiene il nodo e il CSS lo sposta
                key={value}
                value={value}
                index={index}
                movable={movable.includes(value)}
                disabled={locked}
                flash={flashing === value}
                onClick={handleClick}
              />
            ),
          )}
        </div>
      </div>
    </div>
  );
}
