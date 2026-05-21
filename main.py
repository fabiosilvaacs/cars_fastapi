from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from database import create_db_tables
from routers import carros, marcas, modelos


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_tables()
    yield

openapi_tags = [
    {
        "name": "Main",
        "description": "Operações para o recurso Carros",
    },
    {
        "name": "Carros",
        "description": "Operações para o recurso Carros",
    },
    {
        "name": "Marcas",
        "description": "Operações para o recurso Marcas",
    },
    {
        "name": "Modelos",
        "description": "Operações para o recurso Modelos",
    },
]


class NoneExcludedResponse(JSONResponse):
    def render(self, content) -> bytes:
        return super().render(
            jsonable_encoder(content, exclude_none=True)
        )


app = FastAPI(
    title="API de Carros",
    description="API para gerenciamento de marcas, modelos e carros com FastAPI e SQLite.",
    version="1.0.0",
    lifespan=lifespan,
    openapi_tags=openapi_tags,
    redoc_url=None,
    default_response_class=NoneExcludedResponse,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(carros.router, tags=["Carros"])
app.include_router(marcas.router, tags=["Marcas"])
app.include_router(modelos.router, tags=["Modelos"])


@app.get("/", tags=["Main"])
def root():
    return {"message": "API de Carros funcionando!"}
