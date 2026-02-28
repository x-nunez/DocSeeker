"use client";

import { useState } from "react";
import DocumentTable from "../DocumentTable/DocumentTable";

export default function MainPage() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({
    nombre: "",
    extension: "",
    size_min: null as number | null,
    size_max: null as number | null,
    date_min: null as string | null,
    date_max: null as string | null,
  });

  const handleSearch = async () => {
    if (!query.trim() && !Object.values(filters).some(v => v)) return;

    setLoading(true);
    try {
      const body = {
        nombre: filters.nombre || undefined,
        extension: filters.extension || undefined,
        size_min: filters.size_min || undefined,
        size_max: filters.size_max || undefined,
        date_min: filters.date_min || undefined,
        date_max: filters.date_max || undefined,
      };

      const res = await fetch(
        "http://localhost:8000/sherlock/busquedaExacta",
        {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(body),
        }
      );

      if (res.ok) {
        const data = await res.json();
        setResult(data);
      } else {
        setResult({ error: "Search failed" });
      }
    } catch (error) {
      setResult({ error: "Network error" });
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (filterName: string, value: any) => {
    setFilters((prev) => ({ ...prev, [filterName]: value }));
  };

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Search</h1>

      <div className="flex gap-2 mb-4">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()}
          placeholder="Enter search query..."
          className="flex-1 px-4 py-2 border rounded"
        />
        <button
          onClick={handleSearch}
          disabled={loading}
          className="px-6 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-gray-400"
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </div>

      <div className="flex gap-4 mb-6 p-4 bg-white border rounded overflow-x-auto dark:bg-black">
        <div className="flex-shrink-0 w-48">
          <label className="block text-sm font-semibold mb-2">Extension</label>
          <select
            value={filters.extension}
            onChange={(e) => handleFilterChange("extension", e.target.value)}
            className="px-3 py-2 border rounded bg-white dark:bg-gray-800 text-black dark:text-white"
          >
            <option value="">all</option>
            <option value=".pdf">.pdf</option>
            <option value=".txt">.txt</option>
            <option value=".docx">.doc</option>
            <option value=".jpg">.jpg</option>
            <option value=".png">.png</option>
          </select>
        </div>

        <div className="flex-shrink-0">
          <label className="block text-sm font-semibold mb-2">Size Min (bytes)</label>
          <input
            type="number"
            value={filters.size_min || ""}
            onChange={(e) => handleFilterChange("size_min", e.target.value ? parseInt(e.target.value) : null)}
            placeholder="0"
            className="px-3 py-2 border rounded"
          />
        </div>

        <div className="flex-shrink-0">
          <label className="block text-sm font-semibold mb-2">Size Max (bytes)</label>
          <input
            type="number"
            value={filters.size_max || ""}
            onChange={(e) => handleFilterChange("size_max", e.target.value ? parseInt(e.target.value) : null)}
            placeholder="9999999"
            className="px-3 py-2 border rounded"
          />
        </div>

        <div className="flex-shrink-0">
          <label className="block text-sm font-semibold mb-2">Date From</label>
          <input
            type="date"
            value={filters.date_min || ""}
            onChange={(e) => handleFilterChange("date_min", e.target.value || null)}
            className="px-3 py-2 border rounded"
          />
        </div>

        <div className="flex-shrink-0">
          <label className="block text-sm font-semibold mb-2">Date To</label>
          <input
            type="date"
            value={filters.date_max || ""}
            onChange={(e) => handleFilterChange("date_max", e.target.value || null)}
            className="px-3 py-2 border rounded"
          />
        </div>
      </div>

      {result && !result.error && Array.isArray(result) && (
        <div className="mt-4">
          <DocumentTable results={result} />
        </div>
      )}
    </div>
  );
}