import { Link, Outlet } from "react-router-dom";
import { Newspaper } from "lucide-react";

export function Layout() {
  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container mx-auto px-4 py-4">
          <nav className="flex justify-between items-center">
            <Link to="/" className="flex items-center space-x-2">
              <Newspaper className="h-6 w-6" />
              <span className="text-2xl font-bold">Blog</span>
            </Link>
          </nav>
        </div>
      </header>
      <main className="container mx-auto px-4 py-8">
        <Outlet />
      </main>
      <footer className="border-t mt-auto">
        <div className="container mx-auto px-4 py-6 text-center text-muted-foreground">
          © {new Date().getFullYear()} Blog. All rights reserved.
        </div>
      </footer>
    </div>
  );
}
