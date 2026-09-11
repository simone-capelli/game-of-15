import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // In sviluppo Next blocca le richieste alle sue risorse (HMR ecc.) da host
  // diversi da localhost. Le reti locali sono ammesse per aprire l'app da un
  // altro dispositivo (telefono) tramite l'URL "Network" di `npm run dev`.
  allowedDevOrigins: ["192.168.*.*", "10.*.*.*", "172.16.*.*", "172.17.*.*", "172.18.*.*", "172.19.*.*", "172.2*.*.*", "172.30.*.*", "172.31.*.*"],
};

export default nextConfig;
