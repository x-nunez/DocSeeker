import Image from "next/image";

export default function Home() {
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
            <Image
              src="/drive.svg"
              alt="Google Drive logo"
              width={16}
              height={16}
            />
            Login with Google Drive
        </a>
        <a
            className="flex h-12 items-center justify-center gap-2 rounded-full bg-foreground px-5 text-background transition-colors hover:bg-[#383838] dark:hover:bg-[#ccc]"
            href="/main"
            rel="noopener noreferrer"
          >
            <Image
              src="/google.svg"
              alt="Google logo"
              width={16}
              height={16}
            />
            Go to Dashboard
        </a>
      </main>
    </div>
  );
}
