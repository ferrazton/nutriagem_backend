# Nutriagem - Nutritional Assessment Platform

<!-- ![Project Banner](doc/banner.png) Add actual image path later -->

## Project Description

A web application developed for the Software Development course at CIn/UFPE (2024.2). NutriAgem helps nutrition professionals collect patient health data and generate AI-powered nutritional assessments. The system provides qualitative feedback through email integration and recommends appropriate professional follow-up when needed.

**Key Features**:

- Patient health data processing
- AI-powered nutritional deficiency analysis
- Professional referral recommendations
- Email integration for report delivery

## Table of Contents

- [Technologies Used](#technologies-used)
- [System Requirements](#system-requirements)
- [Installation Guide](#installation-guide)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Technologies Used

### Backend

- **Python 3.12**
- FastAPI (REST API framework)
- Pydantic (Data validation)
- Google Generative AI (AI analysis)
- Uvicorn (ASGI server)
- Docker (Containerization)

### Frontend

- React (UI framework)
- Axios (HTTP client)
- HTML5/CSS3
- EsLint (Code quality)
- Vite (Build tool)

## System Requirements

- Python 3.12+
- Node.js 19+
- Docker 20+
- Docker Compose 1.29+
- npm 9+
- Google API Key (for Gemini integration)

## Installation Guide

### 1. Clone Repository

```bash
  git clone https://github.com/lucasmoraismt/nutriagem.git
  cd nutriagem
```

### 2. Backend Setup

```bash
cd backend

# Build and start the Docker containers
docker-compose up --build
```

### 3. Frontend Setup

```bash
  cd ../frontend
  npm install
```

## Configuration

### 1. Create .env file in backend folder

```env
  GEMINI_API_KEY=your_google_api_key_here
```

### 2. Enable CORS in frontend (update src/config.js)

```javascript
export const API_BASE_URL = 'http://localhost:8000'
```

## Running the Application

### Start Backend (from backend folder)

```bash
# Ensure Docker containers are running
docker-compose up
```

### Start Frontend (from frontend folder)

```bash
  npm run dev
```

## API Documentation

Access Swagger UI at <http://localhost:8000/docs> after starting the backend.

Key Endpoints:

- POST /forms/: Submit patient data
- GET /health: Service status check

## Project Structure

```txt
nutriagem/
├── .github/
│   ├── workflows/       # GitHub Actions
│   ├── pull_request_template.md
├── backend/
│   ├── app/
│   │   ├── models/      # Data models
│   │   ├── routes/      # API endpoints
│   │   ├── utils/       # Helper functions
│   │   ├── main.py      # FastAPI initialization
│   ├── tests/
│   │   ├── formsTest.py # Test cases
│   ├── .env             # Environment variables
│   ├── Dockerfile       # Docker configuration
│   ├── docker-compose.yml # Docker Compose configuration
│   ├── Makefile         # Makefile for common tasks
│   ├── requirements.txt # Python dependencies
└── doc/                 # ADRs, diagrams, and other documentation
├── frontend/
│   ├── public/          # Static assets
│   └── src/             # React components
```

## Contributing

We welcome contributions! Please follow these guidelines:

- Create a new branch for your feature
- Maintain coding standards
- Write tests for new functionality
- Update documentation accordingly
- Submit a pull request for review

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For technical issues contact:

Project Maintainer: Lucas de Morais

Email: <lucasmoraismt@gmail.com>

Issue Tracker: <https://github.com/lucasmoraismt/nutriagem/issues>
