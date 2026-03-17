from pydantic import BaseModel,EmailStr
from typing import Optional, List
from datetime import datetime

class WorkerBase(BaseModel):
    name: str
    type: str
    contact: str

class WorkerCreate(WorkerBase):
    pass

class Worker(WorkerBase):
    id: int
    image: str

class WorkerRead(WorkerBase):
    id: int
    
    class Config:
        orm_mode = True

# === Supplier ===
class SupplierBase(BaseModel):
    name: str
    contact: str
    address: str
    delivery_time: int

class SupplierCreate(SupplierBase):
    pass

class SupplierRead(SupplierBase):
    id: int
    class Config:
        orm_mode = True


# === Item ===
class ItemBase(BaseModel):
    name: str
    price: int
    category: str
    stock: int = 0

class ItemCreate(ItemBase):
    pass

class ItemRead(ItemBase):
    id: int
    class Config:
        orm_mode = True


# === Inward ===
class InwardBase(BaseModel):
    barcode: str
    supplier_id: int
    item_id: int
    quantity: int
    date: Optional[datetime] 

class InwardCreate(InwardBase):
    pass

class InwardRead(InwardBase):
    id: int
    class Config:
        orm_mode = True


# === OutwardSlip ===
class OutwardSlipBase(BaseModel):
    worker_id: int
    item_id: int
    quantity: int
    date: Optional[datetime] = None
    status: str

class OutwardSlipCreate(OutwardSlipBase):
    pass

class OutwardSlipRead(OutwardSlipBase):
    id: int

    class Config:
        orm_mode = True
arbitrary_types_allowed = True


# === Outward ===
class OutwardBase(BaseModel):
    slip_id: int
    barcode: str
    quantity: int
    date: Optional[datetime]
    status: str

class OutwardCreate(OutwardBase):
    pass

class OutwardRead(OutwardBase):
    id: int
    class Config:
        orm_mode = True


# === OutwardBarcode ===
class OutwardBarcodeBase(BaseModel):
    barcode: str
    quantity: int

class OutwardBarcodeCreate(OutwardBarcodeBase):
    pass

class OutwardBarcodeRead(OutwardBarcodeBase):
    id: int
    class Config:
        orm_mode = True

# === User ===
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = 'staff'
