from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import UserDefinedType


class Base(DeclarativeBase):
    pass


class Geometry(UserDefinedType):
    """PostGIS GEOMETRY type placeholder for SQLAlchemy."""

    cache_ok = True

    def __init__(self, geometry_type="GEOMETRY", srid=4326):
        self.geometry_type = geometry_type
        self.srid = srid

    def bind_processor(self, dialect):
        return None

    def result_processor(self, dialect, coltype):
        return None


class RiskZone(Base):
    __tablename__ = "risk_zones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    zone_name: Mapped[str | None] = mapped_column(String(255))
    district: Mapped[str | None] = mapped_column(String(100))
    state: Mapped[str | None] = mapped_column(String(100))
    geom: Mapped[dict | None] = mapped_column(Geometry("Polygon"))
    current_risk_level: Mapped[str | None] = mapped_column(String(20), default="Low")
    last_computed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class WeatherReading(Base):
    __tablename__ = "weather_readings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    station_id: Mapped[str] = mapped_column(String(50))
    zone_id: Mapped[int | None] = mapped_column(Integer)
    reading_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    rainfall_mm: Mapped[float | None] = mapped_column(Float)
    soil_moisture_pct: Mapped[float | None] = mapped_column(Float)
    source: Mapped[str | None] = mapped_column(String(50))


class HistoricalLandslide(Base):
    __tablename__ = "historical_landslides"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_date: Mapped[date | None] = mapped_column(Date)
    geom: Mapped[dict | None] = mapped_column(Geometry("Point"))
    severity: Mapped[str | None] = mapped_column(String(20))
    source: Mapped[str | None] = mapped_column(String(50))


class FieldReport(Base):
    __tablename__ = "field_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer)
    geom: Mapped[dict | None] = mapped_column(Geometry("Point"))
    photo_url: Mapped[str | None] = mapped_column(Text)
    video_url: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    report_type: Mapped[str | None] = mapped_column(String(50))
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    sync_status: Mapped[str | None] = mapped_column(String(20), default="synced")


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    zone_id: Mapped[int] = mapped_column(Integer)
    risk_level: Mapped[str] = mapped_column(String(20))
    message: Mapped[str] = mapped_column(Text)
    language: Mapped[str | None] = mapped_column(String(10))
    channel: Mapped[str | None] = mapped_column(String(20))
    dispatched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    explanation: Mapped[str | None] = mapped_column(Text)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True)
    role: Mapped[str | None] = mapped_column(String(20), default="citizen")
    district: Mapped[str | None] = mapped_column(String(100))
    preferred_language: Mapped[str | None] = mapped_column(String(10), default="en")
