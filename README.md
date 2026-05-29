# Pune House Price Prediction Platform

An enterprise-grade distributed AI platform designed using a **Microservices Architecture**. The platform separates high-throughput business logic from computationally intensive machine learning operations.

The system uses:

* **Java 17 Spring Boot** as the enterprise API gateway
* **Python FastAPI** as the AI prediction engine
* **Scikit-Learn Random Forest Regressor** for house price prediction

---

# System Architecture & Data Flow

The platform is divided into two independent microservices to ensure:

* Independent scalability
* Better fault isolation
* Memory separation
* High system stability

## Data Flow

1. Client sends a JSON request to the Java Spring Boot Gateway.
2. Spring Boot validates and transforms request fields.
3. The gateway forwards the request internally using `RestTemplate`.
4. FastAPI processes the request and executes the ML prediction.
5. The predicted price is returned to Spring Boot.
6. Spring Boot sends an immutable response object back to the client.

---

# Tech Stack

## Enterprise Backend Layer (Java)

* Framework: Spring Boot
* Language: Java 17 (LTS)
* Architecture: REST API + Microservices
* DTO Design: Java Records (Immutable)
* Build Tool: Maven

## AI & Machine Learning Layer (Python)

* Framework: FastAPI
* Server: Uvicorn
* ML Libraries:

  * Scikit-Learn
  * Pandas
  * NumPy
* ML Algorithm: Random Forest Regressor
* Model Serialization: Pickle (`.pkl`)

---

# Machine Learning Model Performance

The dataset preprocessing pipeline removes extreme outliers for better prediction stability.

## Preprocessing Constraints

* Area range: 350 sqft – 5000 sqft
* Price limit: Below 5 Crores

## Performance Metrics

* **Mean Absolute Error (MAE):**

  * 28.44 Lakhs

* **R² Score:**

  * 0.629 (62.9% variance explained)

---

# Installation & Setup

## Prerequisites

Make sure the following are installed:

* Java 17 JDK
* Python 3.7+
* Maven

---

# Setup Python ML Microservice

## Install Dependencies

```bash
pip install pandas numpy scikit-learn fastapi uvicorn
```

## Run Training Pipeline

```bash
python pipeline.py
```

This will:

* Clean the dataset
* Train the model
* Generate `.pkl` model artifacts

## Start FastAPI Server

```bash
python app.py
```

The AI microservice will run on:

```text
http://127.0.0.1:8000
```

---

# Setup Spring Boot Gateway

Import the Maven project into:

* IntelliJ IDEA
* Eclipse

Allow Maven to download dependencies.

Run the main application:

```text
src/main/java/com/demo/DemoApplication.java
```

The Spring Boot gateway will run on:

```text
http://localhost:8080
```

---

# API Testing

## Endpoint

```text
POST http://localhost:8080/api/v1/houses/predict
```

## Headers

```text
Content-Type: application/json
```

## Sample Request

```json
{
  "areaType": "Super built-up  Area",
  "size": 3,
  "totalSqft": 1450.0,
  "bath": 3.0,
  "balcony": 2.0,
  "siteLocation": "Kharadi"
}
```

## Sample Response

```json
{
  "predictedPrice": 84.52418
}
```

---

# Key Architecture Features

## Separation of Concerns

The ML engine is isolated from core business logic to improve system maintainability and scalability.

## Type Safety & Immutability

Java 17 Records enforce immutable and thread-safe data transfer.

## Fault Tolerance

The Spring Boot gateway handles AI service failures gracefully using exception handling and fallback responses.

## Cross-Language Communication

Java and Python services communicate seamlessly using REST APIs.

---

# Project Structure

```text
project-root/
│
├── springboot-gateway/
│   ├── controller/
│   ├── service/
│   ├── dto/
│   └── DemoApplication.java
│
├── python-ml-service/
│   ├── app.py
│   ├── pipeline.py
│   ├── model.pkl
│   └── encoders.pkl
│
├── README.md
└── .gitignore
```

---

# Recommended .gitignore

## Java

```gitignore
target/
*.class
```

## Python

```gitignore
__pycache__/
*.pkl
*.pyc
venv/
```

## Dataset Files

```gitignore
*.csv
```

---

# Future Enhancements

* Docker containerization
* Kubernetes deployment
* CI/CD pipeline integration
* Model monitoring
* JWT authentication
* API Gateway rate limiting
* Cloud deployment (AWS/GCP/Azure)

---

# Author

Developed as a production-style AI microservices platform using Java Spring Boot and Python FastAPI.
