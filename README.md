# Task Management & Health Check API

## Tech Stacks
**Language: Python 3.10**

**Framework: FastAPI**

**Database: PostgreSQL**

**ORM: SQLAlchemy**

## Technology Stack Selection Rationale

### FastAPI
* Meeting deadlines through rapid development
* Automatic API documentation (Swagger/OpenAPI)
* Asynchronous processing suitable for Kubernetes environments

### PostgreSQL
* Reliable ACID compliance
* Scalability and reliability
* Cloud Native environment friendly
* Meeting deadlines by using familiar stack

### Python
* Optimized for infrastructure automation/scripting
* Rich library ecosystem
* Essential language from a Cloud Engineer's perspective



## API Features and Test Results
1. Health Check API

Endpoint: GET /health
Function: Check service status and database connection status

Test Results:

2. Todo CRUD API

Create: POST /todos
<img width="1339" alt="image" src="https://github.com/user-attachments/assets/2745a945-7797-4567-8543-9ae53cf116c2">


Read: GET /todos
      GET /todos/{todo_id}
<img width="1347" alt="image" src="https://github.com/user-attachments/assets/a83e0985-ffe8-4483-a997-3c7c332fd039">
<img width="1353" alt="image" src="https://github.com/user-attachments/assets/e3a3bffa-df2a-4c77-984c-8b6ee8eb0421">



Update: PATCH /todos/{todo_id}
<img width="1351" alt="image" src="https://github.com/user-attachments/assets/46b2ff2f-b6eb-4874-bfe2-0b4e51df5b4a">


Delete: DELETE /todos/{todo_id}
<img width="1345" alt="image" src="https://github.com/user-attachments/assets/1f41e936-042d-4666-a951-dd4dcab3d4b2">


3. Environment Configuration Example
```bash
# .env file configure

DATABASE_URL=postgresql://username:password@localhost:5432/health_check

ENVIRONMENT=development  # development/production
```

Database initialization and server startup:

```bash
python dev_init_db.py
```

Swagger UI: http://localhost:8000/docs

Project Structure
```
├── app/                    # API 서버 애플리케이션
│   ├── __init__.py
│   ├── main.py            # FastAPI application
│   ├── database.py        # Database configuration
│   └── models.py          # SQLAlchemy models
├── .github/workflows/     # GitHub Actions CI/CD
│   └── ci.yaml
├── dev_init_db.py         # DB 초기화 및 서버 실행 스크립트
├── requirements.txt
├── Dockerfile
└── .env
```

## CI/CD Pipeline
### CI Process
- Automation through GitHub Actions
- Code testing and lint checks
- Docker image build and push
- Image storage in Docker Hub

### CD Process
- GitOps deployment through ArgoCD
- Kubernetes manifests-based deployment
- Automatic synchronization setup


## Additional Notes
### Development Environment Considerations

- Clear separation between development and production environments
- Configuration management through environment variables
- Health check considering Kubernetes environment

### Production Environment Considerations

- Use of private container registry like AWS ECR instead of Dockerhub in actual production environment
- Using Docker hub due to personal project characteristics
- Statefulset DB configuration in Minikube environment is for demo purposes, managed DB services should be used in actual production environment

### Health Check Implementation Considering Kubernetes Deployment

- Sensitive information management through environment variables and Github secrets
- Enhanced security through GitOps repository separation
