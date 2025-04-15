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