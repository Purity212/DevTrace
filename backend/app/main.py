from fastapi import FastAPI

app = FastAPI(title="DevTrace")

@app.get("/")
def read_root():
    return {
        "app" : "DevTrace",
        "status": "OK"
    }