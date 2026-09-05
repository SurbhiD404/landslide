import React from "react";

export const Header: React.FC = () => {
  const currentDate = new Date().toLocaleDateString("en-IN", {
    weekday: "short",
    year: "numeric",
    month: "short",
    day: "numeric",
  });

  return (
    <header
      style={{
        height: "72px",
        backgroundColor: "var(--color-primary)",
        color: "#ffffff",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0 28px",
        boxShadow: "0 2px 6px rgba(0, 0, 0, 0.12)",
        position: "sticky",
        top: 0,
        zIndex: 1000,
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: "14px" }}>
        {/* Emblem / Shield icon */}
        <div
          style={{
            width: "42px",
            height: "42px",
            borderRadius: "8px",
            backgroundColor: "rgba(255, 255, 255, 0.12)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            border: "1px solid rgba(255, 255, 255, 0.2)",
          }}
        >
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            style={{ color: "#ffffff" }}
          >
            <path d="M12 2L2 7l10 5 10-5-10-5z" />
            <path d="M2 17l10 5 10-5" />
            <path d="M2 12l10 5 10-5" />
          </svg>
        </div>

        <div>
          <div
            style={{
              fontSize: "1.18rem",
              fontWeight: 700,
              letterSpacing: "-0.01em",
              lineHeight: 1.2,
            }}
          >
            Landslide Early Warning System
          </div>
          <div
            style={{
              fontSize: "0.82rem",
              color: "rgba(255, 255, 255, 0.78)",
              fontWeight: 400,
              marginTop: "2px",
            }}
          >
            Ministry of Development of North Eastern Region (MDoNER)
          </div>
        </div>
      </div>

      <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
        <div
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: "7px",
            backgroundColor: "rgba(47, 158, 68, 0.2)",
            border: "1px solid rgba(47, 158, 68, 0.4)",
            color: "#69db7c",
            fontSize: "0.78rem",
            fontWeight: 600,
            padding: "4px 10px",
            borderRadius: "16px",
            letterSpacing: "0.04em",
          }}
        >
          <span
            style={{
              width: "7px",
              height: "7px",
              borderRadius: "50%",
              backgroundColor: "var(--risk-low)",
              display: "inline-block",
              boxShadow: "0 0 6px var(--risk-low)",
            }}
          />
          LIVE
        </div>

        <div
          style={{
            fontSize: "0.82rem",
            color: "rgba(255, 255, 255, 0.82)",
            fontWeight: 500,
          }}
        >
          {currentDate}
        </div>
      </div>
    </header>
  );
};

