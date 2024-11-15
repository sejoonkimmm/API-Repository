# Task Management & Health Check API

## Tech Stacks
**Language: Python 3.10**

**Framework: FastAPI**

**Database: PostgreSQL**

**ORM: SQLAlchemy**

## 기술 스택 선정 근거

### FastAPI
* 빠른 개발 속도를 통해 데드라인을 준수
* 자동 API 문서화 (Swagger/OpenAP)
* Kubernetes 환경에 적합한 비동기 처리

### PostgreSQL
* 안정적인 ACID 준수
* 확장성과 신뢰성
* Cloud Native 환경 친화적
* 익숙한 스택 사용으로 데드라인을 준수


### Python
* 인프라 자동화/스크립팅에 최적화
* 풍부한 라이브러리 생태계
* Cloud Engineer 관점에서 필수적인 언어



## API 기능 및 테스트 결과
1. Health Check API

Endpoint: GET /health
기능: 서비스 상태 및 데이터베이스 연결 상태 확인
테스트 결과:

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


3. 환경 설정 예시
```bash
# .env 파일 구성

DATABASE_URL=postgresql://username:password@localhost:5432/health_check

ENVIRONMENT=development  # development/production
```

데이터베이스 초기화 및 서버 실행:

```bash
python dev_init_db.py
```

Swagger UI: http://localhost:8000/docs

프로젝트 구조
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

## CI/CD 파이프라인
### CI 프로세스
   - GitHub Actions를 통한 자동화
   - 코드 테스트 및 lint 검사
   - Docker 이미지 빌드 및 푸시
   - Docker Hub에 이미지 저장

### CD 프로세스
   - ArgoCD를 통한 GitOps 배포
   - Kubernetes manifests 기반 배포
   - 자동 동기화 설정


## 참고사항
### 개발 환경 고려사항
- 개발 환경과 운영 환경의 명확한 분리
- 환경 변수를 통한 설정관리
- Kubernetes 환경을 고려한 Health check
### 운영 환경 고려사항
- 실제 운영 환경에서는 Dockerhub가 아닌 AWS ECR과 같은 프라이빗 컨테이너 레지스트리 사용
- 개인 프로젝트 특성 상 Docker hub 사용
- Minikube 환경에서의 Statefulset DB 구성은 데모 목적, 실제 운영 환경에서는 관리형 DB서비스 사용
### Kubernetes 배포를 고려한 Health Check 구현
- 환경 변수, Github secret을 통한 민감 정보 관리
- GitOps 레포지토리 분리를 통한 보안 강화
