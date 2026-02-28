// SPDX-License-Identifier: Apache-2.0

"use client";

import Image from "next/image";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import SearchBar from "./SearchBar/SearchBar";
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

  const handleLogout = async () => {
    try {
      await fetch("http://localhost:8000/auth/google/logout", {
        credentials: "include",
      });
    } catch (err) {
      console.error("Logout error:", err);
    } finally {
      router.push("/");
    }
  };

  const handleReload = async () => {
    try {
      const res = await fetch("http://localhost:8000/downloadall/google", {
        credentials: "include",
      });
      if (res.ok) {
      
      } else {

      }
    } catch (err) {
      console.error("Reload error:", err);
    }
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-8 bg-zinc-50 font-sans dark:bg-black p-4">
      <div className="absolute top-4 right-4 flex gap-3">
        <button
          onClick={handleReload}
          className="p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          title="Reload"
        >
          <Image
            src="/reload.svg"
            alt="Reload"
            width={20}
            height={20}
          />
        </button>
        <button
          onClick={handleLogout}
          className="p-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
          title="Logout"
        >
          <Image
            src="/logout.svg"
            alt="Logout"
            width={20}
            height={20}
          />
        </button>
      </div>

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