import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, GeoJSON } from "react-leaflet";
import type { Feature, FeatureCollection } from "geojson";
import type { Layer, PathOptions } from "leaflet";
import "leaflet/dist/leaflet.css";
import api from "../api/client";

interface ZoneProperties {
  id: number;
  zone_name: string;
  district: string;
  state: string;
  current_risk_level: string;
  last_computed_at?: string;
}

interface ZoneExplanationResponse {
  zone_id: number;
  zone_name: string;
  risk_level: string;
  explanation: string;
  thresholds_checked?: Array<{
    name: string;
    threshold_value: number;
    actual_value: number;
  }>;
  mock_data?: boolean;
}

const getRiskColor = (level?: string): string => {
  switch (level?.toLowerCase()) {
    case "low":
      return "#2f9e44"; // var(--risk-low)
    case "moderate":
      return "#f0b429"; // var(--risk-moderate)
    case "high":
      return "#e8590c"; // var(--risk-high)
    case "severe":
      return "#c92a2a"; // var(--risk-severe)
    default:
      return "#718096";
  }
};

export const RiskHeatmap: React.FC = () => {
  const [geoJsonData, setGeoJsonData] = useState<FeatureCollection | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    const fetchRiskZones = async () => {
      try {
        setLoading(true);
        const res = await api.get<FeatureCollection>("/risk-zones");
        if (isMounted) {
          setGeoJsonData(res.data);
          setError(null);
        }
      } catch (err: unknown) {
        if (isMounted) {
          setError(err instanceof Error ? err.message : "Failed to load risk zones");
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    fetchRiskZones();

    return () => {
      isMounted = false;
    };
  }, []);

  const styleZone = (feature?: Feature): PathOptions => {
    const props = feature?.properties as ZoneProperties | undefined;
    const color = getRiskColor(props?.current_risk_level);
    return {
      fillColor: color,
      weight: 2,
      opacity: 0.9,
      color: color,
      fillOpacity: 0.55,
    };
  };

  const onEachFeature = (feature: Feature, layer: Layer) => {
    const props = feature.properties as ZoneProperties | undefined;
    if (!props) return;

    const initialColor = getRiskColor(props.current_risk_level);

    // Initial popup while explanation is fetched
    layer.bindPopup(
      `<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; min-width: 220px; line-height: 1.4;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #e2e5e9; padding-bottom: 6px; margin-bottom: 8px;">
          <strong style="font-size: 1rem; color: #1e3a5f;">${props.zone_name}</strong>
          <span style="background-color: ${initialColor}; color: #ffffff; font-size: 0.72rem; font-weight: 700; padding: 2px 7px; border-radius: 10px; text-transform: uppercase;">
            ${props.current_risk_level}
          </span>
        </div>
        <div style="font-size: 0.8rem; color: #5a6472; margin-bottom: 6px;">
          <strong>District:</strong> ${props.district} (${props.state})
        </div>
        <div style="font-size: 0.8rem; color: #8c9ba5; font-style: italic;">
          Fetching live threshold explanation...
        </div>
      </div>`
    );

    // Dynamic fetch on popup open or click
    layer.on("click", async () => {
      try {
        const res = await api.get<ZoneExplanationResponse>(
          `/risk-zones/${props.id}/explanation`
        );
        const exp = res.data;
        const riskColor = getRiskColor(exp.risk_level || props.current_risk_level);

        const popupHtml = `
          <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; min-width: 260px; max-width: 320px; line-height: 1.4;">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #e2e5e9; padding-bottom: 6px; margin-bottom: 8px;">
              <strong style="font-size: 1.05rem; color: #1e3a5f;">${exp.zone_name || props.zone_name}</strong>
              <span style="background-color: ${riskColor}; color: #ffffff; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 12px; text-transform: uppercase;">
                ${exp.risk_level || props.current_risk_level}
              </span>
            </div>
            <div style="font-size: 0.8rem; color: #5a6472; margin-bottom: 8px;">
              <strong>Location:</strong> ${props.district}, ${props.state}
            </div>
            <div style="background: #f7f8fa; border-left: 3px solid ${riskColor}; padding: 8px 10px; border-radius: 4px; font-size: 0.82rem; color: #1a202c; margin-bottom: 6px;">
              ${exp.explanation}
            </div>
            <div style="font-size: 0.72rem; color: #718096; text-align: right;">
              Status: Threshold Model Verified
            </div>
          </div>
        `;
        layer.setPopupContent(popupHtml);
      } catch (err: unknown) {
        layer.setPopupContent(`
          <div style="font-family: sans-serif; padding: 6px;">
            <strong style="color: #1e3a5f;">${props.zone_name}</strong>
            <div style="color: #c92a2a; font-size: 0.8rem; margin-top: 4px;">
              Failed to load explanation (${err instanceof Error ? err.message : "Network error"}).
            </div>
          </div>
        `);
      }
    });

    // Hover highlight effect
    layer.on("mouseover", () => {
      (layer as unknown as { setStyle: (style: PathOptions) => void }).setStyle({
        weight: 3,
        fillOpacity: 0.78,
      });
    });

    layer.on("mouseout", () => {
      (layer as unknown as { setStyle: (style: PathOptions) => void }).setStyle({
        weight: 2,
        fillOpacity: 0.55,
      });
    });
  };

  return (
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
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-start",
          marginBottom: "16px",
          borderBottom: "1px solid var(--color-border)",
          paddingBottom: "14px",
          flexWrap: "wrap",
          gap: "10px",
        }}
      >
        <div>
          <h2
            style={{
              margin: 0,
              fontSize: "1.15rem",
              fontWeight: 700,
              color: "var(--color-text-primary)",
            }}
          >
            Regional Risk Heatmap
          </h2>
          <p
            style={{
              margin: "4px 0 0 0",
              fontSize: "0.82rem",
              color: "var(--color-text-secondary)",
            }}
          >
            North Eastern Region — PostGIS spatial hazard polygons &amp; threshold classification
          </p>
        </div>

        {/* Legend */}
        <div style={{ display: "flex", gap: "10px", alignItems: "center" }}>
          <span style={{ fontSize: "0.75rem", color: "var(--color-text-secondary)", fontWeight: 500 }}>
            Risk Scale:
          </span>
          <div style={{ display: "flex", alignItems: "center", gap: "4px" }}>
            <span
              style={{
                width: "10px",
                height: "10px",
                borderRadius: "2px",
                backgroundColor: "var(--risk-low)",
                display: "inline-block",
              }}
            />
            <span style={{ fontSize: "0.75rem", color: "var(--risk-low)", fontWeight: 600 }}>Low</span>
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: "4px" }}>
            <span
              style={{
                width: "10px",
                height: "10px",
                borderRadius: "2px",
                backgroundColor: "var(--risk-moderate)",
                display: "inline-block",
              }}
            />
            <span style={{ fontSize: "0.75rem", color: "var(--risk-moderate)", fontWeight: 600 }}>
              Moderate
            </span>
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: "4px" }}>
            <span
              style={{
                width: "10px",
                height: "10px",
                borderRadius: "2px",
                backgroundColor: "var(--risk-high)",
                display: "inline-block",
              }}
            />
            <span style={{ fontSize: "0.75rem", color: "var(--risk-high)", fontWeight: 600 }}>
              High
            </span>
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: "4px" }}>
            <span
              style={{
                width: "10px",
                height: "10px",
                borderRadius: "2px",
                backgroundColor: "var(--risk-severe)",
                display: "inline-block",
              }}
            />
            <span style={{ fontSize: "0.75rem", color: "var(--risk-severe)", fontWeight: 600 }}>
              Severe
            </span>
          </div>
        </div>
      </div>

      {error && (
        <div
          style={{
            marginBottom: "12px",
            padding: "8px 12px",
            backgroundColor: "#fff5f5",
            border: "1px solid #ffc9c9",
            borderRadius: "var(--radius)",
            color: "var(--risk-severe)",
            fontSize: "0.82rem",
          }}
        >
          Warning: Failed to load spatial zones ({error}). Check backend connection.
        </div>
      )}

      {/* Leaflet Map View */}
      <div
        style={{
          flex: 1,
          minHeight: "440px",
          borderRadius: "calc(var(--radius) - 2px)",
          overflow: "hidden",
          border: "1px solid var(--color-border)",
          position: "relative",
        }}
      >
        {loading && (
          <div
            style={{
              position: "absolute",
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              backgroundColor: "rgba(255, 255, 255, 0.75)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              zIndex: 1000,
              fontSize: "0.9rem",
              fontWeight: 600,
              color: "var(--color-primary)",
            }}
          >
            Loading GeoJSON risk zones...
          </div>
        )}

        <MapContainer
          center={[26.19, 91.72]}
          zoom={13}
          scrollWheelZoom={true}
          style={{ height: "100%", width: "100%", minHeight: "440px" }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {geoJsonData && (
            <GeoJSON
              key={JSON.stringify(geoJsonData.features?.length ?? 0)}
              data={geoJsonData}
              style={styleZone}
              onEachFeature={onEachFeature}
            />
          )}
        </MapContainer>
      </div>
    </div>
  );
};

