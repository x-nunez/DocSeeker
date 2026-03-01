"use client";

import { useEffect, useState } from "react";

export default function ThemeToggle() {
    const [dark, setDark] = useState(false);

    useEffect(() => {
        const saved = localStorage.getItem("theme");

        if (saved) {
            const isDark = saved === "dark";
            setDark(isDark);
            document.documentElement.classList.toggle("dark", isDark);
        } else {
            const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
            setDark(prefersDark);
            document.documentElement.classList.toggle("dark", prefersDark);
        }
    }, []);

    const toggle = () => {
        const newTheme = !dark;
        setDark(newTheme);
        document.documentElement.classList.toggle("dark", newTheme);
        localStorage.setItem("theme", newTheme ? "dark" : "light");
    };

    return (
        <button
            onClick={toggle}
            className="w-10 h-10 flex items-center justify-center bg-white border border-zinc-200 rounded-lg hover:bg-zinc-100 dark:bg-zinc-800 dark:border-zinc-700 dark:hover:bg-zinc-700 transition-colors"
            title={dark ? "Cambiar a modo claro" : "Cambiar a modo oscuro"}
        >
            {dark ? "☀️" : "🌙"}
        </button>
    );
}