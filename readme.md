# 🚀 FastAPI Backend

Backend project menggunakan **FastAPI** dengan struktur yang rapi, modular, dan mudah dijalankan di lingkungan lokal maupun production.

## 📌 Fitur
- Framework FastAPI
- Auto reload dengan Uvicorn
- Struktur folder modular (routers, models, services)
- Environment variables menggunakan `.env`
- Manajemen dependency melalui `requirements.txt`

## 🔧 Cara Install & Menjalankan Project

### 1. Clone Repository
```
git clone <url-repository>
cd project
```

### 2. Buat Virtual Environment
**Windows:**
```
python -m venv venv
venv\Scripts\activate
```
**Mac/Linux:**
```
python -m venv venv
source venv/bin/activate
```
### 3. Install Dependencies
```
pip install -r requirements.txt
```
### 4. Setup Environment Variables
```
cp .env.example .env  
```
Edit isi `.env` sesuai kebutuhan.

### 5. Jalankan Server
```
npm start
```
Akses API:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 📦 Menambah Dependency Baru
```
pip install nama-package  
pip freeze > requirements.txt
```