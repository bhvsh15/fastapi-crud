# Inventory Management System - Proof of Concept (POC)

**Prepared by:** Bhavesh Mandwani  
**Role:** Intern  
**Date:** March 2026

---

## 🚀 Project Overview
The Inventory Management System is a full-stack web app designed to streamline internal inventory operations. It replaces manual or spreadsheet-based tracking with a modern, role-controlled, database-backed system.

---

## 🎯 Objectives
- Centralized platform for items, suppliers, and workers
- Track inward stock (with barcode, supplier, quantity)
- Record outward dispatches (with slips and barcodes)
- Role-based access (Admin: full control, Staff: view-only)
- Clean, modern web interface

---

## 📦 Scope (POC Features)
- User Authentication (JWT-based login/register)
- Item Management (CRUD with stock tracking)
- Supplier Management (CRUD)
- Worker Management (CRUD + image upload)
- Inward Stock Management (CRUD with auto stock updates)
- Outward Slips (CRUD + stock deduction)
- Outward Entries & Barcodes (tracking dispatch flow)

---

## 🛠️ Technology Stack

### Backend
- **FastAPI** (Python): REST API with auto-generated docs
- **SQLAlchemy**: ORM for database interaction
- **MySQL**: Relational DB storage
- **JWT**: Token-based authentication
- **Passlib/Bcrypt**: Secure password hashing
- **Uvicorn**: ASGI server

### Frontend
- **HTML5 / CSS3 / JavaScript (ES6+)**
- **Fetch API**: Async communication with backend
- **localStorage**: JWT storage for session persistence
- **Google Fonts**: Modern UI styling

---

## 🗄️ Database Schema
- **Users**: Login credentials, roles
- **Items**: Inventory stock, categories
- **Suppliers**: Supplier details
- **Workers**: Worker profiles (with image)
- **Inwards**: Incoming stock entries
- **Outward Slips**: Dispatch requests
- **Outwards**: Actual outward transactions
- **Outward Barcodes**: Barcode-level tracking

---

## 🔗 API Endpoints
Base URL: `http://localhost:8000`  
All protected routes require **Bearer Token**

---

### 🔐 Authentication
- `POST /auth/login` → Login (returns JWT)
- `POST /auth/register` → Register user

---

### 📦 Items
- `GET /items/` → Get all items  
- `GET /item/{id}` → Get item by ID  
- `POST /item/create` → Create item  
- `PUT /item/{id}` → Update item  
- `DELETE /item/{id}` → Delete item (**Admin only**)  

---

### 🚚 Suppliers
- `GET /suppliers/` → Get all suppliers  
- `GET /supplier/{id}` → Get supplier  
- `POST /supplier/create` → Create supplier  
- `PUT /supplier/{id}` → Update supplier  
- `DELETE /supplier/{id}` → Delete supplier  

---

### 👷 Workers
- `GET /workers` → Get all workers  
- `GET /worker/{id}` → Get worker  
- `POST /worker/create` → Create worker (**Admin only**)  
- `PUT /worker/{id}` → Update worker  
- `DELETE /worker/{id}` → Delete worker (**Admin only**)  

---

### 📥 Inward Stock
- `GET /inwards/` → Get all inward entries  
- `POST /inward/create` → Add stock (auto-increment item stock)  
- `PUT /inward/{id}` → Update inward  
- `DELETE /inward/{id}` → Delete inward  

---

### 📤 Outward Slips
- `GET /outwardslips/` → Get all slips  
- `POST /outwardslip/create` → Create slip (deduct stock)  
- `PUT /outwardslip/{id}` → Update slip  
- `DELETE /outwardslip/{id}` → Delete slip  

---

### 📦 Outward Entries
- `GET /outwards/` → Get all outward entries  
- `POST /outward/create` → Create outward (marks slip completed)  

---

### 🔍 Outward Barcodes
- `GET /outwardbarcodes/` → Get all barcodes  
- `POST /outwardbarcode/create` → Link barcode to outward entry  

---
