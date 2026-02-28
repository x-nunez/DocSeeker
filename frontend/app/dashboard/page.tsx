"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import DocumentTable from "./DocumentTable/DocumentTable";

export default function MainPage() {
  const [query, setQuery] = useState("");
  const router = useRouter();
  const [loading, setLoading] = useState(true);

  // Check if authorized
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const res = await fetch("http://localhost:8000/auth/google/me", {
          credentials: "include",
        });

        if (!res.ok) {
          router.push("/");
        }
      } catch (err) {
        console.log("Auth check failed:", err);
        router.push("/");
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, [router]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    // For now, just log the query. You can replace this with actual search logic
    console.log("Searching for:", query);
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-8 bg-zinc-50 font-sans dark:bg-black p-4">
      <header>
        <h1 className="text-4xl font-bold text-center text-black dark:text-zinc-50">
          Welcome to Your Document Hub
        </h1>
        <p className="mt-2 text-center text-gray-600 dark:text-gray-300">
          Find and manage your documents easily
        </p>
      </header>

      <main className="w-full max-w-md">
        <form
          onSubmit={handleSearch}
          className="flex gap-2 w-full"
        >
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search documents..."
            className="flex-1 rounded-l-full border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white dark:border-gray-600"
          />
          <button
            type="submit"
            className="rounded-r-full bg-blue-500 px-4 py-2 text-white hover:bg-blue-600 transition-colors"
          >
            Search
          </button>
        </form>

        <DocumentTable results={[
          { "nombre": "Contrato 2024", "fecha": "2024-01-15", "autor": "Ana García", "type": "PDF" },
          { "nombre": "Factura Marzo", "fecha": "2024-03-01", "type": "Word" },
          { "nombre": "Informe Q1", "fecha": "2024-04-10", "autor": "Sara Martín", "type": "Excel", "descripcion": "gato" }]} />
      </main>
    </div>
  );
}