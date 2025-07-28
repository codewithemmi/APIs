from . database import Base
from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql.expression import null
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship
from sqlalchemy import select




class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    disabled = Column(Boolean, server_default='FALSE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    

    
    
    


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")

    
class Vote(Base):
    __tablename__ = "votes"
    posts_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    users_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)



