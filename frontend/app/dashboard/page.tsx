"use client";

import Image from "next/image";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import SearchBar from "./SearchBar/SearchBar";

export default function MainPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [providerStatus, setProviderStatus] = useState({
    google: false,
    microsoft: false,
  });

  // Check if authorized
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const [googleRes, microsoftRes] = await Promise.all([
          fetch("http://localhost:8000/auth/google/me", {
            credentials: "include",
          }),
          fetch("http://localhost:8000/auth/microsoft/me", {
            credentials: "include",
          }),
        ]);

        setProviderStatus({
          google: googleRes.ok,
          microsoft: microsoftRes.ok,
        });

        if (!googleRes.ok && !microsoftRes.ok) {
          router.push("/");
          return;
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

  const handleLogin = (provider: "google" | "microsoft") => {
    window.location.href = `http://localhost:8000/auth/${provider}/login`;
  };

  const handleLogout = async (provider: "google" | "microsoft") => {
    try {
      await fetch(`http://localhost:8000/auth/${provider}/logout`, {
        credentials: "include",
      });
    } catch (err) {
      console.error("Logout error:", err);
    } finally {
      setProviderStatus((prev: { google: boolean; microsoft: boolean }) => ({ ...prev, [provider]: false }));
    }
  };

  const handleReload = async (provider: "google" | "microsoft") => {
    try {
      const res = await fetch(`http://localhost:8000/downloadall/${provider}`, {
        credentials: "include",
      });
      if (res.ok) {
      
      } else {

      }
    } catch (err) {
      console.error("Reload error:", err);
    }
  };

  if (loading) return null;

  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-8 bg-zinc-50 font-sans dark:bg-black p-4">
      <div className="absolute top-4 right-4 flex gap-3">
        <div className="relative group">
          <button
            className="w-10 h-10 flex items-center justify-center bg-white border border-zinc-200 rounded-lg hover:bg-zinc-100 transition-colors"
            title="Google"
          >
            <Image src="/google.svg" alt="Google" width={20} height={20} />
          </button>

          <div className="absolute right-0 top-full pt-2 flex flex-col gap-2 opacity-0 invisible pointer-events-none group-hover:opacity-100 group-hover:visible group-hover:pointer-events-auto z-10">
              {providerStatus.google ? (
                <>
                  <button
                    onClick={() => handleReload("google")}
                    className="w-10 h-10 flex items-center justify-center bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                    title="Actualizar Google"
                  >
                    <Image src="/reload.svg" alt="Reload" width={20} height={20} />
                  </button>
                  <button
                    onClick={() => handleLogout("google")}
                    className="w-10 h-10 flex items-center justify-center bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                    title="Cerrar sesión Google"
                  >
                    <Image src="/logout.svg" alt="Logout" width={20} height={20} />
                  </button>
                </>
              ) : (
                <button
                  onClick={() => handleLogin("google")}
                  className="w-10 h-10 flex items-center justify-center bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                  title="Iniciar sesión Google"
                >
                  <Image src="/login.svg" alt="Login Google" width={20} height={20} />
                </button>
              )}
          </div>
        </div>

        <div className="relative group">
          <button
            className="w-10 h-10 flex items-center justify-center bg-white border border-zinc-200 rounded-lg hover:bg-zinc-100 transition-colors"
            title="Microsoft"
          >
            <Image src="/microsoft.svg" alt="Microsoft" width={20} height={20} />
          </button>

          <div className="absolute right-0 top-full pt-2 flex flex-col gap-2 opacity-0 invisible pointer-events-none group-hover:opacity-100 group-hover:visible group-hover:pointer-events-auto z-10">
              {providerStatus.microsoft ? (
                <>
                  <button
                    onClick={() => handleReload("microsoft")}
                    className="w-10 h-10 flex items-center justify-center bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                    title="Actualizar Microsoft"
                  >
                    <Image src="/reload.svg" alt="Reload" width={20} height={20} />
                  </button>
                  <button
                    onClick={() => handleLogout("microsoft")}
                    className="w-10 h-10 flex items-center justify-center bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                    title="Cerrar sesión Microsoft"
                  >
                    <Image src="/logout.svg" alt="Logout" width={20} height={20} />
                  </button>
                </>
              ) : (
                <button
                  onClick={() => handleLogin("microsoft")}
                  className="w-10 h-10 flex items-center justify-center bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                  title="Iniciar sesión Microsoft"
                >
                  <Image src="/login.svg" alt="Login Microsoft" width={20} height={20} />
                </button>
              )}
          </div>
        </div>
      </div>

      <header>
        <h1 className="text-4xl font-bold text-center text-black dark:text-zinc-50">
          Welcome to Your Document Hub
        </h1>
        <p className="mt-2 text-center text-gray-600 dark:text-gray-300">
          Find and manage your documents easily
        </p>
      </header>

      <main className="w-full max-w-6xl">
        <SearchBar/>
      </main>
    </div>
  );
}