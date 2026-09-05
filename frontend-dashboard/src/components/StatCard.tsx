import React from "react";

export interface StatCardProps {
  label: string;
  value: string | number;
  accentColor?: string;
  helperText?: string;
}

export const StatCard: React.FC<StatCardProps> = ({
  label,
  value,
  accentColor,
  helperText,
}) => {
  return (
    <div
      style={{
        backgroundColor: "var(--color-surface)",
        borderRadius: "var(--radius)",
        boxShadow: "var(--shadow-card)",
        border: "1px solid var(--color-border)",
        padding: "20px 24px",
        position: "relative",
        overflow: "hidden",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
      }}
    >
      {accentColor && (
        <div
          style={{
            position: "absolute",
            left: 0,
            top: 0,
            bottom: 0,
            width: "5px",
            backgroundColor: accentColor,
          }}
        />
      )}
      <div
        style={{
          fontSize: "0.82rem",
          fontWeight: 600,
          color: "var(--color-text-secondary)",
          textTransform: "uppercase",
          letterSpacing: "0.04em",
          marginBottom: "6px",
        }}
      >
        {label}
      </div>
      <div
        style={{
          fontSize: "2.1rem",
          fontWeight: 700,
          color: accentColor ? accentColor : "var(--color-text-primary)",
          lineHeight: 1.1,
        }}
      >
        {value}
      </div>
      {helperText && (
        <div
          style={{
            fontSize: "0.78rem",
            color: "var(--color-text-secondary)",
            marginTop: "6px",
          }}
        >
          {helperText}
        </div>
      )}
    </div>
  );
};

