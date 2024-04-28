from siteseo.app.db.base import Base
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
class Message(Base):
    """Model for in-app messaging."""
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String)
    recipient = Column(String)
    content = Column(String)
    timestamp = Column(DateTime(), server_default=func.now())
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}