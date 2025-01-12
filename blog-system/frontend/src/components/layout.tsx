import { Link, Outlet } from "react-router-dom";
import { Newspaper } from "lucide-react";

export function Layout() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <header className="border-b border-neon-cyan/20">
        <div className="container mx-auto px-4 py-4">
          <nav className="flex justify-between items-center">
            <Link 
              to="/" 
              className="flex items-center space-x-2 hover-glow text-neon-cyan"
            >
              <Newspaper className="h-6 w-6" />
              <span className="text-2xl font-bold neon-text">赛博格志</span>
            </Link>
          </nav>
        </div>
      </header>
      <main className="container mx-auto px-4 py-8">
        <Outlet />
      </main>
      <footer className="border-t border-neon-cyan/20 mt-auto">
        <div className="container mx-auto px-4 py-6 text-center text-muted-foreground">
          <span className="text-neon-cyan/70">
            © {new Date().getFullYear()} 赛博格志. All rights reserved.
          </span>
        </div>
      </footer>
    </div>
  );
}
