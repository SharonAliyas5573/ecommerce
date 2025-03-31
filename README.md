# E-Commerce Backend API

## Overview
This project is a scalable e-commerce backend API built using Django REST Framework. It includes features such as user authentication, product management, cart management, order processing, and a discount/coupon system. The API is designed to be high-performance and secure, with considerations for scalability and efficiency.

## Features
- **User Authentication**: JWT authentication for customers and admins.
- **Product Management**: APIs to add, edit, delete, and fetch products with support for categories, stock availability, and images.
- **Cart System**: Persistent cart management allowing users to add/remove items.
- **Order Processing**: Customers can place orders and track their status (Pending, Shipped, Delivered).
- **Discount & Coupon System**: Apply discount codes during checkout with restrictions based on expiry and user eligibility.
- **Caching**: Redis caching for faster product retrieval.
- **Rate Limiting**: Prevent API abuse through rate limiting.
- **Background Tasks**: Order notifications handled by Celery.
- **Dockerized Deployment**: Fully containerized setup using Docker and Docker Compose.

## Technologies Used
- **Framework**: Django REST Framework
- **Database**: MongoDB
- **Caching**: Redis
- **Task Queue**: Celery
- **Containerization**: Docker and Docker Compose
- **Deployment**: Render with CI/CD setup #TODO

---

## Installation

### Prerequisites
- Docker and Docker Compose installed on your system.
- Python 3.11+ installed (for local development without Docker).

### Steps to Run the Project

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd ecommerce-backend
```

#### 2. Set Up Environment Variables
Create a `.env` file in the root directory with the following variables:
```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
MONGO_URI=mongodb://mongo:27017/ecommerce
REDIS_URL=redis://redis:6379/0
```

#### 3. Build and Run the Docker Containers
Run the following commands to start the application using Docker:
```bash
docker-compose build
docker-compose up
```

This will start the following services:
- **web**: The Django application running with Gunicorn.
- **db**: MongoDB database.
- **redis**: Redis for caching and Celery message broker.
- **celery**: Celery worker for background tasks.

#### 4. Access the Application
- The API will be available at: `http://localhost:8000/`
- MongoDB will be available at: `localhost:27017`
- Redis will be available at: `localhost:6379`

---

## Running the Project Locally (Without Docker)

If you prefer to run the project locally without Docker, follow these steps:

1. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Start MongoDB and Redis services on your local machine.

3. Run database migrations:
   ```bash
   python manage.py migrate
   ```

4. Start the development server:
   ```bash
   python manage.py runserver
   ```

---

## API Documentation
API endpoints and usage can be found in the [Postman collection](https://www.postman.com/galactic-zodiac-39647/workspace/personal-workspace/collection/28324271-0d597754-1071-47fb-9e29-e9517b48ec64?action=share&creator=28324271).

---

## Security
- Input validation is implemented to prevent injection attacks.
- Rate limiting is enforced to protect against abuse.
- Sensitive data is encrypted.


---

## License
This project is licensed under the MIT License.