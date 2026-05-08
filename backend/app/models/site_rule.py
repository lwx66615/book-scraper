from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime
from sqlalchemy.sql import func
from app.database import Base


class SiteRule(Base):
    __tablename__ = "site_rules"

    id = Column(Integer, primary_key=True, index=True)
    site_name = Column(String(100), nullable=False)
    site_url = Column(String(500), nullable=False)
    is_active = Column(Boolean, default=True)
    rule_type = Column(String(20), default="generic")  # specific/generic
    selectors = Column(JSON, default=dict)
    headers = Column(JSON, default=dict)
    requires_js = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
