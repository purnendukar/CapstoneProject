from sqlalchemy import create_engine, Column, Integer, DateTime, Text, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import UniqueConstraint

engine = create_engine("mysql://root:password@mysqldb/capstone", echo = True)

Base = declarative_base()

class News(Base):
   __tablename__ = 'news'
   id = Column(Integer, primary_key = True)
   title = Column(String(length=255))
   date_time = Column(DateTime)
   summary = Column(Text)
   topic = Column(String(length=100))
   source = Column(String(length=255))
   __table_args__ = (
       UniqueConstraint(
            'title',
            'date_time',
            'topic',
            'source',
            name='uix'
        ),
    )


Base.metadata.create_all(engine)

