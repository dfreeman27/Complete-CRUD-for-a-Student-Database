from fastapi import FastAPI
from app.database import Base, engine
from app.models import student  # registers the Student model on Base
from app.routers import students

app = FastAPI(title="Student CRUD API")

Base.metadata.create_all(bind=engine)

app.include_router(students.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)