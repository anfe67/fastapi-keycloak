import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from .api import router
    from .settings import get_settings
except ImportError:
    from api import router
    from settings import get_settings


def app_maker():
    settings = get_settings()
    app = FastAPI(title="EXAMPLE")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)
    return app

if __name__ == "__main__":
    app = app_maker()
    uvicorn.run(app, host="0.0.0.0", port=8000)
