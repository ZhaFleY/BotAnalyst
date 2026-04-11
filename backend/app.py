import uvicorn
from fastapi import FastAPI,Depends

from backend.routers import file_router

app = FastAPI()

app.include_router(file_router.router)

@app.get("/")
def main():




    return {"message": "I'm Alive"}





if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8300)

