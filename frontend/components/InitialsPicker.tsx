"use client";

import { useState } from "react";

const LENGTH = 3;

type Props = {
  onConfirm: (initials: string) => void;
  pending: boolean;
};

// Campo per le tre lettere del nome, stile high score: solo lettere,
// maiuscole automatiche, Invio o START per confermare.
export default function InitialsPicker({ onConfirm, pending }: Props) {
  const [name, setName] = useState("");
  const valid = name.length === LENGTH;

  function onChange(e: React.ChangeEvent<HTMLInputElement>) {
    const letters = e.target.value.toUpperCase().replace(/[^A-Z]/g, "").slice(0, LENGTH);
    setName(letters);
  }

  function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (valid && !pending) onConfirm(name);
  }

  return (
    <form className="section" onSubmit={onSubmit}>
      <label htmlFor="initials" className="subtitle">
        ENTER YOUR NAME (3 LETTERS)
      </label>
      <input
        id="initials"
        className="initials-input"
        value={name}
        onChange={onChange}
        placeholder="AAA"
        maxLength={LENGTH}
        autoFocus
        autoComplete="off"
        autoCapitalize="characters"
        spellCheck={false}
        inputMode="text"
        aria-describedby="initials-help"
      />
      <span id="initials-help" className="hint" style={{ margin: 0 }}>
        {name.length}/{LENGTH}
      </span>
      <button type="submit" className="btn" disabled={!valid || pending}>
        {pending ? "..." : "START"}
      </button>
    </form>
  );
}
