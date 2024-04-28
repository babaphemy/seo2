from siteseo.app.db.base import Base
from sqlalchemy import Column,DateTime
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import Integer,String,Boolean
class Webbuilder(Base):
    __tablename__ = "webbuilder"
    id = Column(String, primary_key=True, index=True)
    content = Column(String)
    product_id = Column(Integer)
    is_live = Column(Boolean, default=False)
    timestamp = Column(DateTime(), server_default=func.now())