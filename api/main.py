from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Esta es el servidor de mi api!"}

