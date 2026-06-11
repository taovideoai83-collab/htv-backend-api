import os
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# 1. Cấu hình Database (Tự động dùng SQLite để bạn dễ chạy thử)
DATABASE_URL = "sqlite:///./htv_enterprise_v3.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Tạo bảng Dữ liệu (Dự án)
class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    location = Column(String)
    investor = Column(String)
    status = Column(String, default="Đang triển khai")
    description = Column(Text)

Base.metadata.create_all(bind=engine)

# 3. Khởi tạo Web API
app = FastAPI(title="HTV Enterprise API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

class ProjectCreate(BaseModel):
    name: str
    location: str
    investor: str

@app.get("/")
def home():
    return {"message": "Hệ thống HTV Backend API đang hoạt động bình thường!"}

@app.post("/api/projects")
def create_project(proj: ProjectCreate, db: Session = Depends(get_db)):
    db_proj = Project(name=proj.name, location=proj.location, investor=proj.investor)
    db.add(db_proj)
    db.commit()
    return {"message": "Đã thêm dự án thành công", "project_name": proj.name}

@app.get("/api/projects")
def get_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)