import uvicorn

from app.fast_api_app import FastAPIApp


app = FastAPIApp()


@app.get("/ping")
def ping():
    return {"message": "pong"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
