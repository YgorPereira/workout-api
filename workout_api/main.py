from fastapi import FastAPI

from workout_api.routers import api_router


app = FastAPI(title="Workout API", version="1.0.0")
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8000, log_level="info", reload=True)
