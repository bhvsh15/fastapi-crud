from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Worker(Base):
    __tablename__ = 'workers'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    type = Column(String(50))
    contact = Column(String(50))
    image = Column(String(255))

    outward_slips = relationship("OutwardSlip", back_populates="worker")


class Supplier(Base):
    __tablename__ = 'supplier'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    contact = Column(String(50))
    address = Column(String(255))
    delivery_time = Column(Integer)

    inwards = relationship("Inward", back_populates="supplier")


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    price = Column(Integer)
    stock = Column(Integer)
    category = Column(String(50))

    inwards = relationship("Inward", back_populates="item")
    outward_slips = relationship("OutwardSlip", back_populates="item")


class Inward(Base):
    __tablename__ = 'inwards'

    id = Column(Integer, primary_key=True)
    barcode = Column(Integer)
    supplier_id = Column(Integer, ForeignKey('supplier.id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    quantity = Column(Integer)
    date = Column(DateTime, default=datetime.now)

    supplier = relationship("Supplier", back_populates="inwards")
    item = relationship("Item", back_populates="inwards")


# === OutwardSlip ===
class OutwardSlip(Base):
    __tablename__ = 'outward_slips'

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey('workers.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    status = Column(String,default="Complete")

    worker = relationship("Worker", back_populates="outward_slips")
    item = relationship("Item", back_populates="outward_slips")
    outwards = relationship("Outward", back_populates="slip")


# === Outward ===
class Outward(Base):
    __tablename__ = 'outwards'

    id = Column(Integer, primary_key=True, index=True)
    slip_id = Column(Integer, ForeignKey('outward_slips.id'), nullable=False)
    barcode = Column(String(100), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="Complete")
    quantity = Column(Integer, nullable=False)

    slip = relationship("OutwardSlip", back_populates="outwards")
    outward_barcodes = relationship("OutwardBarcode", back_populates="outward")


# === OutwardBarcode ===
class OutwardBarcode(Base):
    __tablename__ = 'outward_barcodes'

    id = Column(Integer, primary_key=True, index=True)
    outward_id = Column(Integer, ForeignKey('outwards.id'), nullable=False)
    barcode = Column(String(100), nullable=False) 
    quantity = Column(Integer, nullable=False)

    outward = relationship("Outward", back_populates="outward_barcodes")

# === User Authentication Table ===
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="staff")  # admin or staff