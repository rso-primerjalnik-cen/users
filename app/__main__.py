import uvicorn

uvicorn.run("app.api:fastapi_app", host="0.0.0.0", port=8001, reload=True)
