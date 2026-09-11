import Link from "next/link";

type Props = {
  message: string;
  homeLink?: boolean;
};

export default function ErrorMessage({ message, homeLink = false }: Props) {
  return (
    <div className="alert" role="alert">
      <p style={{ margin: 0 }}>{message}</p>
      {homeLink && (
        <p style={{ margin: "0.75rem 0 0" }}>
          <Link href="/">← BACK TO START</Link>
        </p>
      )}
    </div>
  );
}
