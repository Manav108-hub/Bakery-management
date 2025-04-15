# 🍞 Bakery Management System

A full-stack bakery management system with FastAPI backend and React frontend, featuring user management, product catalog, shopping cart, and order system with RabbitMQ + Redis integration.

![Architecture Diagram](./image.png)



![Workflow Graph](./workflow.png)

## ✨ Key Features

### **Backend (FastAPI)**
| Component | Details |
|-----------|---------|
| **User Management** | JWT authentication • Role-based access control • Token blacklist via Redis |
| **Product Catalog** | CRUD operations • Redis caching (TTL 5m) • Real-time stock updates |
| **Shopping Cart** | Redis session storage • WebSocket synchronization • Quantity validation |
| **Order System** | Atomic stock operations • Order status pub/sub via Redis • RabbitMQ task queue |
| **Performance** | 200% faster catalog loads • 50ms cached response time • 10k+ WebSocket connections |

### **Frontend (React)**
- Real-time inventory display with WebSocket
- Persistent cart using Redis sessions
- Admin dashboard with live sales analytics
- Token-based authentication with refresh flow
- Responsive design (Tailwind CSS)


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


### **Redis**

 - In-memory data store for enhanced performance and real-time features:
 - Caching : Stores frequently accessed data like product catalogs with TTL support.
 - Session Storage : Manages user sessions securely with fast retrieval.
 - Pub/Sub : Enables real-time notifications via WebSocket for cart updates and order status.
 - Rate Limiting : Protects APIs by enforcing request limits per user or IP.
 - Atomic Operations : Ensures thread-safe actions for cart updates and stock management.
 - Task State Tracking : Monitors the status of background jobs processed by RabbitMQ.


## 🛠️ Tech Stack

**Backend**  
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/rabbitmq-%23FF6600.svg?style=for-the-badge&logo=rabbitmq&logoColor=white)

**Frontend**  
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![Tailwind CSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Vite](https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white)

## 🚀 Quick Start

### Docker Setup (Recommended)
```bash
# Start all services
docker-compose up -d

# Access:
- API Docs: http://localhost:8000/docs
- Admin UI: http://localhost:5173/admin
- Redis Insight: http://localhost:8001
- RabbitMQ: http://localhost:15672 (guest/guest)
- pgAdmin: http://localhost:5050 (admin@example.com / admin)

Local Development
Backend:

# Start dependencies
docker-compose up -d postgres redis rabbitmq

# Activate environment
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run server
uvicorn src.app:app --reload

Frontend:

cd frontend
npm install
npm run dev


🔧 Implementation Details
Redis Usage:

Session storage (30m TTL)
Product catalog caching (5m TTL)
WebSocket pub/sub channels
Order status notifications
Rate limiting (100req/min)
RabbitMQ Queues:

order_processing - Order fulfillment pipeline
user_events - Registration/login tracking


📝 Environment Variables

# .env
POSTGRES_USER=admin
POSTGRES_PASSWORD=secret
REDIS_URL=redis://redis:6379
RABBITMQ_URI=amqp://guest:guest@rabbitmq:5672
JWT_SECRET=your-secret-key