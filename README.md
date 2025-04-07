# 🍞 Bakery Management System

A full-stack bakery management system with FastAPI backend and React frontend, featuring user management, product catalog, shopping cart, and order system with RabbitMQ integration.

![Project Structure](https://via.placeholder.com/800x400.png?text=Bakery+Management+System+Diagram) <!-- Add actual screenshot/diagram later -->

## ✨ Features

### **Backend (FastAPI)**
- 🔐 **User Management**: Registration, login, and role-based access (admin/user)
- 🍰 **Product Catalog**: CRUD operations for bakery products
- 🛒 **Shopping Cart**: Add/remove products, quantity management
- 📦 **Order System**: Place orders with stock management
- ⚡ **Asynchronous Tasks**: RabbitMQ integration for background processing
- 📚 **API Docs**: Interactive Swagger/ReDoc documentation
- 🛡️ **Security**: JWT token authentication
- 🐘 **Database**: PostgreSQL with SQLAlchemy ORM

### **Frontend (React)**

The React-based interface focuses on user experience with:
1 . Interactive product browsing/cart management
2 . JWT-based session handling
3 . Responsive design via Tailwind CSS
4 . Real-time API communication with Axios
5 . Role-specific views (user/admin)
6 . Implements client-side routing with React Router and state management via Context API.

- 👨💻 User authentication (login/registration)
- 🎨 Product browsing interface
- 🛍️ Shopping cart functionality
- 📜 Order history tracking
- ⚙️ Admin dashboard (basic CRUD operations)


### **Docker**
- Containerization system that packages the application with:
- Isolated environments for backend/frontend
- PostgreSQL and RabbitMQ services
- Network configuration for cross-service communication
- Dependency management via Docker images
- Enables consistent deployment across development/staging/production environments.

### **RabbitMQ**

- Message broker handling asynchronous operations:
- Decouples main API from background tasks
- Manages queues for user events, order notifications, and system logs
- Enables horizontal scaling of task workers
- Provides fail-safety through message persistence
- Used for non-critical path operations (email alerts, analytics, audit logs).

## 🛠️ Technologies

**Backend Stack**  
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/rabbitmq-%23FF6600.svg?style=for-the-badge&logo=rabbitmq&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

**Frontend Stack**  
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![Tailwind CSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Vite](https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white)

## 📂 Project Structure

```bash
CONTAINER-ASSIGNMENT/
├── backend/
│   ├── src/
│   │   ├── app.py             # Main FastAPI application
│   │   ├── database.py        # DB configuration
│   │   ├── models/            # Database models
│   │   ├── routes/            # API endpoints
│   │   ├── schemas/           # Pydantic schemas
│   │   └── rabbitmq/          # RabbitMQ configurations
│   ├── alembic/               # Database migrations
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── services/          # API services
│   │   └── ...                # React application files
└── docker-compose.yml         # Docker configuration

🚀 Getting Started
Prerequisites
Python 3.10+
Node.js 16+
PostgreSQL 14+
RabbitMQ
Docker 

Installation
1. Backend Setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Update .env with your credentials

# Run migrations
alembic upgrade head

# Start server
uvicorn src.app:app --reload

2. Frontend Setup
cd frontend
npm install
npm run dev

🐳 Docker Setup
# Start all services
docker-compose up -d

# Access endpoints:
# - API: http://localhost:8000
# - Frontend: http://localhost:5173
# - RabbitMQ: http://localhost:15672 (guest/guest)

🔄 RabbitMQ Integration
The system uses RabbitMQ for handling background tasks:

User Events: Track registrations and logins

Order Events: Process order notifications

System Logs: Async logging operations

Access RabbitMQ dashboard at http://localhost:15672 to monitor queues.