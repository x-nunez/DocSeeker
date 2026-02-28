import Image from "next/image";
import SearchBar from "./main/SearchBar/SearchBar";

export default function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <aside>
        <p>
          SideBar1
        </p>
        <p>
          SideBar2
        </p>
      </aside>

      <header></header>

      <main className="flex min-h-screen w-full max-w-3xl flex-col items-center justify-between py-32 px-16 bg-white dark:bg-black sm:items-start">
        <SearchBar placeholder="Search file"/>

        <a
            className="flex h-12 items-center justify-center gap-2 rounded-full bg-foreground px-5 text-background transition-colors hover:bg-[#383838] dark:hover:bg-[#ccc]"
            href="http://localhost:8000/auth/google/login"
            target="_blank"
            rel="noopener noreferrer"
          >
            <Image
              className="dark:invert"
              src="/vercel.svg"
              alt="Vercel logomark"
              width={16}
              height={16}
            />
            Login with Google Drive
        </a>

        <div className="flex flex-col items-center gap-6 text-center sm:items-start sm:text-left">
          <h1 className="max-w-xs text-3xl font-semibold leading-10 tracking-tight text-black dark:text-zinc-50">
            Welcome to the future of your documents
          </h1>
        </div>
      </main>
    </div>
  );
}
