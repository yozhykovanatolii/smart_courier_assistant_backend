<div align="center">

# 🚚 Smart Courier Assistant — Backend

**Backend API for courier delivery management, route optimization, ETA analysis and AI-assisted recommendations**

</div>

## 📄 About

Smart Courier Assistant Backend is a REST API built to support the [Smart Courier Assistant mobile application](https://github.com/yozhykovanatolii/smart_courier_assistant_app).
The backend provides authentication, user and order management, route optimization, ETA estimation, delivery risk analysis, proof of delivery, and AI-assisted route recommendations.
It also integrates with external services for route calculation, AI recommendations, and file storage.

## 🛠 Tech Stack

**Core Framework**
- **FastAPI** – Web framework for building the REST API 
- **Python** – Programming language    

**Database**
- **PostgreSQL** – Relational database
- **SQLAlchemy** – ORM and database interaction
- **asyncpg** – Asynchronous PostgreSQL driver

**Validation & Configuration**
- **Pydantic** – Data validation and serialization
- **Pydantic Settings** – Environment-based configuration

**Authentication & Security**
- **JWT** – Access and refresh token authentication
- **pwdlib** – Password hashing

**Infrastructure**
- **Docker** – Containerization
- **Docker Compose** – Multi-container application setup

**External Services**
- **Supabase Storage** – File storage for user uploads and media management

## 🏗️ Project Structure

```text
├── api/
│   ├── routers/              # API route definitions
│   ├── dependencies.py       # FastAPI dependencies
│   └── router.py             # Main API router
├── clients/                  # External service clients
├── exceptions/               # Custom exceptions and error handlers
├── repositories/             # Data access layer
├── schemas/                  # Pydantic schemas
├── services/                 # Business logic
├── .env.example              # Environment variables template
├── config.py                 # Application configuration
├── database.py               # Database configuration
├── docker-compose.yaml       # Docker Compose configuration
├── Dockerfile                # Backend Docker image
├── main.py                   # FastAPI application entry point
├── models.py                 # SQLAlchemy models
├── requirements.txt          # Python dependencies
└── security.py               # Authentication and security
