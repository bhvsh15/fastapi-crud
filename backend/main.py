from fastapi import FastAPI
from routes.worker import router as worker_router
from routes.supplier import router as supplier_router
from routes.items import router as items_router
from routes.inwards import router as inward_router
from routes.outward import router as outward_router
from routes.outwardslip import router as slip_router
from routes.outwardbar import router as barcode_router
from auth.auth_routes import router as auth_router


app = FastAPI()

app.include_router(worker_router)
app.include_router(supplier_router)
app.include_router(items_router)
app.include_router(inward_router)
app.include_router(outward_router)
app.include_router(slip_router)
app.include_router(barcode_router)
app.include_router(auth_router)


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)