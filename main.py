from fastapi import FastAPI
from Routes.worker import router as worker_router
from Routes.supplier import router as supplier_router
from Routes.items import router as items_router
from Routes.inwards import router as inward_router
from Routes.outward import router as outward_router
from Routes.outwardslip import router as slip_router
from Routes.outwardbar import router as barcode_router


app = FastAPI()

app.include_router(worker_router)
app.include_router(supplier_router)
app.include_router(items_router)
app.include_router(inward_router)
app.include_router(outward_router)
app.include_router(slip_router)
app.include_router(barcode_router)
