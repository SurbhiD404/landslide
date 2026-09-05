import React, { useEffect, useState } from "react";
import api from "../api/client";
import { StatCard } from "./StatCard";

interface DashboardSummary {
  total_zones: number;
  risk_counts?: {
    Low?: number;
    Moderate?: number;
    High?: number;
    Severe?: number;
  };
  active_alerts: number;
  reports_pending: number;
}

export const DashboardStats: React.FC = () => {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    const fetchSummary = async () => {
      try {
        setLoading(true);
        const res = await api.get<DashboardSummary>("/dashboard/summary");
        if (isMounted) {
          setSummary(res.data);
          setError(null);
        }
      } catch (err: unknown) {
        if (isMounted) {
          setError(err instanceof Error ? err.message : "Failed to load stats");
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    fetchSummary();

    return () => {
      isMounted = false;
    };
  }, []);

  const highSevereCount =
    (summary?.risk_counts?.High ?? 0) + (summary?.risk_counts?.Severe ?? 0);

  return (
    <section aria-label="Key Dashboard Metrics">
      {error && (
        <div
          style={{
            marginBottom: "16px",
            padding: "10px 14px",
            backgroundColor: "#fff5f5",
            border: "1px solid #ffc9c9",
            borderRadius: "var(--radius)",
            color: "var(--risk-severe)",
            fontSize: "0.85rem",
          }}
        >
          Notice: Unable to refresh live stats ({error}). Showing cached/fallback data.
        </div>
      )}

      <div className="stats-grid">
        <StatCard
          label="Total Zones Monitored"
          value={loading ? "..." : (summary?.total_zones ?? 0)}
          helperText="Active administrative units"
        />

        <StatCard
          label="Active Alerts"
          value={loading ? "..." : (summary?.active_alerts ?? 0)}
          accentColor="var(--risk-severe)"
          helperText="Dispatched early warnings"
        />

        <StatCard
          label="High/Severe Zones"
          value={loading ? "..." : highSevereCount}
          accentColor="var(--risk-high)"
          helperText="Critical threshold exceedance"
        />

        <StatCard
          label="Field Reports"
          value={loading ? "..." : (summary?.reports_pending ?? 0)}
          helperText="Citizen & field submissions"
        />
      </div>
    </section>
  );
};

