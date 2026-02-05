import { InventoryMap } from "@/components/InventoryMap";

export default function Home() {
  return (
    <main className="min-h-screen p-8 md:p-12 relative overflow-hidden">
      <div className="scanline" />

      <div className="max-w-7xl mx-auto relative z-10">
        <header className="mb-12 flex items-center justify-between">
          <div>
            <h1 className="text-4xl md:text-6xl font-black tracking-tighter neon-text mb-2">
              RCA AGEN<span className="text-primary">T</span>
            </h1>
            <p className="text-xl text-gray-400">Autonomous Incident Response System</p>
          </div>
          <div className="hidden md:block">
            <div className="flex items-center gap-2 text-sm font-mono text-primary bg-primary/10 px-4 py-2 rounded-full border border-primary/20">
              <span className="relative flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-primary"></span>
              </span>
              SYSTEM ONLINE
            </div>
          </div>
        </header>

        <section className="space-y-8">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold flex items-center gap-3">
              <span className="w-1 h-8 bg-primary rounded-full" />
              Live Inventory
            </h2>
          </div>

          <InventoryMap />
        </section>
      </div>
    </main>
  );
}
