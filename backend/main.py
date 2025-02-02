from fastapi import FastAPI
from backend.database import engine, Base
from backend.routes import player_routes, course_routes, competition_routes, round_routes, score_routes
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI
app = FastAPI()

# Include routers
app.include_router(player_routes.router)
app.include_router(course_routes.router)
app.include_router(competition_routes.router)
app.include_router(round_routes.router)
app.include_router(score_routes.router)

#Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific frontend URL if deploying
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Golf Society Backend Running"}
