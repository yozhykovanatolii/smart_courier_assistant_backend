<div align="center">

# 🚚 Smart Courier Assistant — Backend

**Backend API for courier delivery management, route optimization, ETA analysis and AI-assisted recommendations**

</div>

## 📄 About

Smart Courier Assistant Backend is a REST API built to support the [Smart Courier Assistant mobile application](https://github.com/yozhykovanatolii/smart_courier_assistant_app).
The backend provides authentication, user and order management, route optimization, ETA estimation, delivery risk analysis, proof of delivery, and AI-assisted route recommendations.
It also integrates with external services for route calculation, AI recommendations, and file storage.

## ✨ Features

- 🔐 **Authentication & Profile** – User registration, login, JWT-based authentication, profile management 
- 📦 **Order Management** – Create, update, delete and retrieve delivery orders, manage delivery statuses
- 📍 **Routes & ETA** – Optimize delivery routes, calculate estimated arrival times and analyze delivery risks  
- 📜 **Route History** – Store and retrieve completed delivery routes
- 🧠 **AI Recommendations** – Generate personalized route recommendations when delivery delays are likely
- 📸 **Proof of Delivery (POD)** – Store delivery confirmation data, including photos and notes  
- 🗄️ **Database** – PostgreSQL database for persistent application data
- 📁 **File Storage** – Supabase Storage for user-uploaded media
- 🔒 **Security** – Password hashing and JWT-based access and refresh tokens

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

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- Docker

### Installation
1. Clone the repository
```
git clone https://github.com/yozhykovanatolii/smart_courier_assistant_backend.git
```

2. Configure environment variables

This project uses external services to provide routing and AI-assisted features, as well as file storage.
- **OpenRouteService** — route calculation and ETA estimation
- **OpenAI API** — AI-assisted route recommendations
- **Supabase Storage** — file storage for user uploads and media management

To configure these services: 
- Create an account at https://openrouteservice.org and generate an API key
- Create an account at https://platform.openai.com and generate an API key
- Create a project in Supabase at https://supabase.com and get your project credentials(URL and anon key)

For creating SECRET_KEY and using for access and refresh tokens, you have to execute this code:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Use .env.example for creating the .env file in the project root and set the following values:

```env
# Security
SECRET_KEY=

# Supabase
SUPABASE_PROJECT_URL=
SUPABASE_ANON_KEY=

# External APIs
OPENAI_API_KEY=
OPENROUTE_API_KEY=

# PostgreSQL
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=smart_courier_assistant
POSTGRES_USER=postgres
```

3. Run the application
```
docker compose up --build
```
The API and API documentation will be available at: http://localhost:8000 and http://localhost:8000/docs



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
```

## 📡 API Endpoints

The API provides endpoints for:

- Authentication and user management
- Order management
- Route optimization and ETA estimation
- Route history
- AI-assisted recommendations
- Proof of delivery
- File uploads

For the complete API reference, see the interactive [Swagger UI](http://localhost:8000/docs).

