import { useState } from "react";
import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

const REGIONS = ["India", "Southeast Asia", "Middle East", "Europe"];

function App() {
  const [selectedRegions, setSelectedRegions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);

  const toggleRegion = (region) => {
    setSelectedRegions((prev) =>
      prev.includes(region)
        ? prev.filter((r) => r !== region)
        : [...prev, region]
    );
  };

  const runSearch = async () => {
    if (selectedRegions.length === 0) {
      setError("Select at least one region first.");
      return;
    }
    setError(null);
    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE}/api/search/`, {
        regions: selectedRegions,
        include_maps: true,
        include_directories: true,
      });
      setResults(response.data.leads || []);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Couldn't reach the backend. Is uvicorn running on port 8000?"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-2xl font-semibold mb-1">Lead Generation Dashboard</h1>
        <p className="text-slate-400 mb-6">
          Pharma and general manufacturing leads across your target regions.
        </p>

        {/* Search form */}
        <div className="bg-slate-800 rounded-lg p-5 mb-6">
          <h2 className="text-sm font-medium text-slate-300 mb-3">Regions</h2>
          <div className="flex flex-wrap gap-2 mb-4">
            {REGIONS.map((region) => (
              <button
                key={region}
                onClick={() => toggleRegion(region)}
                className={`px-3 py-1.5 rounded-md text-sm border transition ${
                  selectedRegions.includes(region)
                    ? "bg-blue-600 border-blue-500 text-white"
                    : "bg-slate-700 border-slate-600 text-slate-300 hover:bg-slate-600"
                }`}
              >
                {region}
              </button>
            ))}
          </div>

          <button
            onClick={runSearch}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed text-white px-4 py-2 rounded-md text-sm font-medium"
          >
            {loading ? "Scraping..." : "Run Search"}
          </button>

          {error && (
            <p className="text-red-400 text-sm mt-3">{error}</p>
          )}
        </div>

        {/* Results table */}
        <div className="bg-slate-800 rounded-lg p-5">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-sm font-medium text-slate-300">
              Results {results.length > 0 && `(${results.length})`}
            </h2>
            {results.length > 0 && (
              
                href={`${API_BASE}/api/export/csv`}
                className="bg-green-600 hover:bg-green-500 text-white px-3 py-1.5 rounded-md text-xs font-medium"
              >
                Export CSV
              </a>
            )}
          </div>

          {results.length === 0 ? (
            <p className="text-slate-500 text-sm">
              No results yet. Select regions and run a search.
            </p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-slate-400 border-b border-slate-700">
                    <th className="pb-2 pr-4">Company</th>
                    <th className="pb-2 pr-4">Region</th>
                    <th className="pb-2 pr-4">Website</th>
                    <th className="pb-2 pr-4">Source</th>
                  </tr>
                </thead>
                <tbody>
                  {results.map((lead, i) => (
                    <tr key={i} className="border-b border-slate-700/50">
                      <td className="py-2 pr-4">{lead.company_name || "—"}</td>
                      <td className="py-2 pr-4">{lead.region || "—"}</td>
                      <td className="py-2 pr-4">{lead.website || "—"}</td>
                      <td className="py-2 pr-4">{lead.source || "—"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;