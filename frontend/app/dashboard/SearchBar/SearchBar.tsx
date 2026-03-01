// SPDX-License-Identifier: Apache-2.0

"use client";

import { useState } from "react";
import DocumentTable from "../DocumentTable/DocumentTable";

export default function MainPage() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [filters, setFilters] = useState({
    nombre: "",
    extension: "",
    size_min: null as number | null,
    size_max: null as number | null,
    date_min: null as string | null,
    date_max: null as string | null,
  });

  const handleSearch = async () => {
    const filtersOn = filters.extension || filters.size_min || filters.size_max || filters.date_min || filters.date_max;

    try {
      let res;

      if (filtersOn){
        setLoading(true);
        //GET a busquedaExacta con filtros
        const params = new URLSearchParams();
        if (query) params.append("nombre", query);
        if (filters.extension) params.append("extension", filters.extension);
        if (filters.size_min !== null) params.append("size_min", filters.size_min.toString());
        if (filters.size_max !== null) params.append("size_max", filters.size_max.toString());
        if (filters.date_min) params.append("date_min", filters.date_min);
        if (filters.date_max) params.append("date_max", filters.date_max);

        res = await fetch(`http://localhost:8000/sherlock/busquedaExacta?${params.toString()}`, {
          method: "GET",
          credentials: "include",
        });
      } else{
        if (!query.trim()) return;
        setLoading(true);
        //GET a busquedaVectorial
        res = await fetch(`http://localhost:8000/sherlock/busquedaVectorial?string=${encodeURIComponent(query)}`,
          {
            method: "GET",
            credentials: "include",
          }
        );
      }

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
    <div className="w-full p-4 sm:p-8">
      <h1 className="text-2xl font-bold mb-4">Search</h1>

      <div className="flex flex-col sm:flex-row gap-2 mb-4 w-full">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()}
          placeholder="Enter search query..."
          className="w-full min-w-0 sm:flex-1 px-4 py-2 border rounded"
        />
        <button
          onClick={handleSearch}
          disabled={loading}
          className="w-full sm:w-auto px-6 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-gray-400"
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </div>

      <div className="mb-6 p-3 bg-white border rounded dark:bg-black">
        <div className="flex items-center justify-between">
          <span className="text-sm font-semibold">Advanced options</span>
          <button
            type="button"
            onClick={() => setShowAdvanced((prev) => !prev)}
            className="h-7 w-7 flex items-center justify-center border rounded hover:bg-zinc-100 dark:hover:bg-zinc-900"
            title={showAdvanced ? "Contraer" : "Expandir"}
            aria-label={showAdvanced ? "Contraer opciones avanzadas" : "Expandir opciones avanzadas"}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
              className={`h-4 w-4 transition-transform ${showAdvanced ? "rotate-180" : "rotate-0"}`}
              aria-hidden="true"
            >
              <path
                fillRule="evenodd"
                d="M5.23 7.21a.75.75 0 0 1 1.06.02L10 11.17l3.71-3.94a.75.75 0 1 1 1.08 1.04l-4.25 4.5a.75.75 0 0 1-1.08 0l-4.25-4.5a.75.75 0 0 1 .02-1.06Z"
                clipRule="evenodd"
              />
            </svg>
          </button>
        </div>

      {showAdvanced && (
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-5 gap-3 mt-3">
          <div className="w-full min-w-0">
            <label className="block text-xs font-semibold mb-1">Extension</label>
            <select
              value={filters.extension}
              onChange={(e) => handleFilterChange("extension", e.target.value)}
              className="w-full px-2 py-1.5 text-sm border rounded bg-white dark:bg-gray-800 text-black dark:text-white"
            >
              <option value="">all</option>
              <option value=".pdf">.pdf</option>
              <option value=".txt">.txt</option>
              <option value=".docx">.doc</option>
              <option value=".jpg">.jpg</option>
              <option value=".png">.png</option>
            </select>
          </div>

          <div className="w-full min-w-0">
            <label className="block text-xs font-semibold mb-1">Size Min (bytes)</label>
            <input
              type="number"
              value={filters.size_min || ""}
              onChange={(e) => handleFilterChange("size_min", e.target.value ? parseInt(e.target.value) : null)}
              placeholder="0"
              className="w-full px-2 py-1.5 text-sm border rounded"
            />
          </div>

          <div className="w-full min-w-0">
            <label className="block text-xs font-semibold mb-1">Size Max (bytes)</label>
            <input
              type="number"
              value={filters.size_max || ""}
              onChange={(e) => handleFilterChange("size_max", e.target.value ? parseInt(e.target.value) : null)}
              placeholder="9999999"
              className="w-full px-2 py-1.5 text-sm border rounded"
            />
          </div>

          <div className="w-full min-w-0">
            <label className="block text-xs font-semibold mb-1">Date From</label>
            <input
              type="date"
              value={filters.date_min || ""}
              onChange={(e) => handleFilterChange("date_min", e.target.value || null)}
              className="w-full px-2 py-1.5 text-sm border rounded"
            />
          </div>

          <div className="w-full min-w-0">
            <label className="block text-xs font-semibold mb-1">Date To</label>
            <input
              type="date"
              value={filters.date_max || ""}
              onChange={(e) => handleFilterChange("date_max", e.target.value || null)}
              className="w-full px-2 py-1.5 text-sm border rounded"
            />
          </div>
        </div>
      )}
      </div>

      {result && !result.error && Array.isArray(result) && (
        <div className="mt-4">
          <DocumentTable results={result} />
        </div>
      )}
    </div>
  );
}