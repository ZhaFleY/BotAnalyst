import uvicorn
from fastapi import FastAPI,Depends
from backend.s3.init_bucket import init_bucket
from backend.routers import file_router

app = FastAPI()

app.include_router(file_router.router)

@app.on_event("startup")
def startup():
    init_bucket()

@app.get("/")
def main():




    return {"message": "I'm Alive"}





if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8300)

