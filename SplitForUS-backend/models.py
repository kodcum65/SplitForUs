# SplitForUS-backend/models.py

from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class User(Base):
    __tablename__ = "users"

    id                      = Column(Integer, primary_key=True, index=True)
    username                = Column(String, unique=True, index=True, nullable=False)
    email                   = Column(String, unique=True, index=True, nullable=False)
    hashed_password         = Column(String, nullable=False)
    created_tables_count    = Column(Integer, default=0, nullable=False)
    is_paid                 = Column(Boolean, default=False, nullable=False)

    email_verified          = Column(Boolean, default=False, nullable=False)
    email_verification_code = Column(String, nullable=True)

    def __repr__(self):
        return f"<User username={self.username} email={self.email} email_verified={self.email_verified}>"
