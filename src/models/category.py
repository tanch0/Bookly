from sqlalchemy import Column, Integer, String, DateTime
from src.database.config import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    products = relationship("Product", back_populates="category")
