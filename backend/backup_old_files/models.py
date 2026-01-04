from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

# Association table for many-to-many relationship between videos and keywords
video_keywords = Table(
    'video_keywords',
    Base.metadata,
    Column('video_id', Integer, ForeignKey('videos.id')),
    Column('keyword_id', Integer, ForeignKey('keywords.id'))
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    searches = relationship("Search", back_populates="user")
    saved_videos = relationship("SavedVideo", back_populates="user")

class Video(Base):
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True, index=True)
    youtube_id = Column(String, unique=True, index=True)
    title = Column(String)
    description = Column(Text)
    channel = Column(String)
    duration = Column(String)
    thumbnail_url = Column(String)
    view_count = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    keywords = relationship("Keyword", secondary=video_keywords, back_populates="videos")
    saved_by = relationship("SavedVideo", back_populates="video")
    search_results = relationship("SearchResult", back_populates="video")

class Keyword(Base):
    __tablename__ = "keywords"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    # Relationships
    videos = relationship("Video", secondary=video_keywords, back_populates="keywords")

class Search(Base):
    __tablename__ = "searches"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    query = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="searches")
    results = relationship("SearchResult", back_populates="search")

class SearchResult(Base):
    __tablename__ = "search_results"
    
    id = Column(Integer, primary_key=True, index=True)
    search_id = Column(Integer, ForeignKey("searches.id"))
    video_id = Column(Integer, ForeignKey("videos.id"))
    relevance_score = Column(Float)
    rank = Column(Integer)
    
    # Relationships
    search = relationship("Search", back_populates="results")
    video = relationship("Video", back_populates="search_results")

class SavedVideo(Base):
    __tablename__ = "saved_videos"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    video_id = Column(Integer, ForeignKey("videos.id"))
    saved_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="saved_videos")
    video = relationship("Video", back_populates="saved_by")
