import GameScreen from "./GameScreen";

// In Next 16 `params` e' una Promise: la si attende qui (server) e si passa
// l'id al componente client, che da solo si carica lo stato dal backend.
export default async function GamePage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return <GameScreen id={id} />;
}
