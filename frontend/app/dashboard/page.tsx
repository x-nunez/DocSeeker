"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import SearchBar from "./SearchBar/SearchBar";

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
        <SearchBar/>
      </main>
    </div>
  );
}