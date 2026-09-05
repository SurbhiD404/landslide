import { Header } from "./components/Header";
import { DashboardStats } from "./components/DashboardStats";
import { RiskHeatmap } from "./components/RiskHeatmap";

function App() {
  return (
    <div style={{ minHeight: "100vh", backgroundColor: "var(--color-background)" }}>
      <Header />

      <main
        style={{
          maxWidth: "1400px",
          margin: "0 auto",
          padding: "24px",
        }}
      >
        <DashboardStats />

        <div className="dashboard-layout">
          {/* Left Column: RiskHeatmap (~65% width) */}
          <RiskHeatmap />

          {/* Right Column: Alert Console Placeholder (~35% width) */}
          <div
            style={{
              backgroundColor: "var(--color-surface)",
              borderRadius: "var(--radius)",
              boxShadow: "var(--shadow-card)",
              border: "1px solid var(--color-border)",
              padding: "24px",
              minHeight: "540px",
              display: "flex",
              flexDirection: "column",
            }}
          >
            <div
              style={{
                borderBottom: "1px solid var(--color-border)",
                paddingBottom: "14px",
                marginBottom: "16px",
              }}
            >
              <h2
                style={{
                  margin: 0,
                  fontSize: "1.15rem",
                  fontWeight: 700,
                  color: "var(--color-text-primary)",
                }}
              >
                Alert Console
              </h2>
              <p
                style={{
                  margin: "4px 0 0 0",
                  fontSize: "0.82rem",
                  color: "var(--color-text-secondary)",
                }}
              >
                Dispatched early warnings &amp; threshold explanations
              </p>
            </div>

            <div
              style={{
                flex: 1,
                minHeight: "420px",
                backgroundColor: "#fafbfc",
                borderRadius: "calc(var(--radius) - 2px)",
                border: "1px dashed var(--color-border)",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                color: "var(--color-text-secondary)",
                padding: "20px",
                textAlign: "center",
              }}
            >
              <svg
                width="40"
                height="40"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
                style={{ opacity: 0.5, marginBottom: "10px" }}
              >
                <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
                <path d="M13.73 21a2 2 0 0 1-3.46 0" />
              </svg>
              <div style={{ fontWeight: 600, fontSize: "0.95rem", color: "var(--color-text-primary)" }}>
                Alert Console — coming next
              </div>
              <div style={{ fontSize: "0.8rem", marginTop: "4px", maxWidth: "260px" }}>
                Real-time notification stream with multilingual translations (EN / AS / BN)
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
