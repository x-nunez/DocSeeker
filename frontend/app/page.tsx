"use client";

import Image from "next/image";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const res = await fetch("http://localhost:8000/auth/google/me", {
          credentials: "include",
        });
        if (res.ok) {
          router.push("/dashboard");
        }
      } catch {
        console.log("No valid token")
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, [router]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-8 bg-zinc-50 font-sans dark:bg-black">

      <header>
        <h1 className="max-w-xs text-3xl font-semibold leading-10 tracking-tight text-center text-black dark:text-zinc-50">
            Welcome to the future of your documents
        </h1>
      </header>

      <main className="flex flex-col items-center justify-center gap-4">
        <a
          className="flex h-12 items-center justify-center gap-2 rounded-full bg-foreground px-5 text-background transition-colors hover:bg-[#383838] dark:hover:bg-[#ccc]"
          href="http://localhost:8000/auth/google/login"
          rel="noopener noreferrer"
        >
          {loading ? (
            <>
              <span className="w-4 h-4 border-2 border-black border-t-transparent rounded-full animate-spin"></span>
              <span>Checking login...</span>
            </>
          ) : (
            <>
              <Image
                src="/drive.svg"
                alt="Google Drive logo"
                width={16}
                height={16}
              />
              <span>Login with Google Drive</span>
            </>
          )}
        </a>
      </main>
    </div>
  );
}
