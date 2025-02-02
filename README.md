# Golf Society Backend

This is the backend API for managing a golf society, built using FastAPI and SQLite.

## Features
- Player management
- Course management
- Competitions and rounds tracking
- Score tracking and leaderboards

## Installation

### Prerequisites
Ensure you have **Python 3.8+** installed.

### Clone the Repository
```sh
git clone <your-repo-url>
cd golf_society_backend
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

### Run the Server
```sh
uvicorn backend.main:app --reload
```

### API Endpoints
Once running, you can access the **interactive API documentation** at:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## License
This project is licensed under the MIT License.
