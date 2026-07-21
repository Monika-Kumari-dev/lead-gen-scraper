import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../api/client";

export default function LeadDetail() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [lead, setLead] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLead();
  }, [id]);

  const fetchLead = async () => {
    try {
      const { data } = await api.get(`/api/results/${id}`);
      setLead(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center text-white bg-slate-900">
        Loading...
      </div>
    );
  }

  if (!lead) {
    return (
      <div className="min-h-screen flex items-center justify-center text-white bg-slate-900">
        Company not found
      </div>
    );
  }

  return (
    <div
      className="min-h-screen p-8"
      style={{
        background:
          "linear-gradient(90deg,#020024 0%,#090979 11%,#00d4ff 100%)",
      }}
    >
      <div className="max-w-5xl mx-auto">

        <button
          onClick={() => navigate(-1)}
          className="mb-6 bg-white/10 hover:bg-white/20 px-4 py-2 rounded-lg text-white"
        >
          ← Back
        </button>

        <div className="bg-white/10 backdrop-blur-xl rounded-2xl overflow-hidden border border-white/10">

          <div className="h-72 bg-slate-800 flex justify-center items-center">

            {lead.image_url ? (
              <img
                src={lead.image_url}
                alt={lead.company_name}
                className="w-full h-full object-cover"
              />
            ) : (
              <div className="text-8xl font-bold text-white/30">
                {lead.company_name.charAt(0)}
              </div>
            )}

          </div>

          <div className="p-8">

            <h1 className="text-4xl font-bold text-white mb-2">
              {lead.company_name}
            </h1>

            <p className="text-slate-300 mb-8">
              {lead.region}
            </p>

            <div className="grid md:grid-cols-2 gap-6">

              <Card title="📍 Address" value={lead.address} />
              <Card title="📞 Phone" value={lead.phone} />
              <Card title="✉️ Email" value={lead.email} />
              <Card title="🏭 Industry" value={lead.industry} />
              <Card title="🌍 Country" value={lead.country} />
              <Card title="✔ QA Status" value={lead.qa_status} />
              <Card title="📂 Source" value={lead.source} />
              <Card title="🕒 Scraped" value={lead.scraped_at} />

            </div>

            {lead.website && (
              <a
                href={lead.website}
                target="_blank"
                rel="noreferrer"
                className="inline-block mt-8 bg-cyan-500 hover:bg-cyan-400 text-white px-6 py-3 rounded-lg font-semibold"
              >
                Visit Website
              </a>
            )}

          </div>

        </div>
      </div>
    </div>
  );
}

function Card({ title, value }) {
  return (
    <div className="bg-white/5 border border-white/10 rounded-xl p-5">

      <p className="text-xs uppercase text-slate-400 mb-2">
        {title}
      </p>

      <p className="text-lg text-white break-words">
        {value || "Not Available"}
      </p>

    </div>
  );
}