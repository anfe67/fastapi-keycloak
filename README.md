# FastAPI Keycloak Integration

A FastAPI application demonstrating integration with Keycloak for authentication and authorization.

## Overview

This project provides a complete example of integrating FastAPI with Keycloak, including:
- JWT token validation using Keycloak public keys
- Role-based access control (RBAC)
- Protected endpoints with role guards
- CORS configuration for frontend integration
- A Vue 3 demo frontend application

## Features

- **FastAPI Backend**: Modern Python web framework with automatic OpenAPI documentation
- **Keycloak Integration**: Secure authentication and authorization using Keycloak
- **JWT Validation**: Token verification using Keycloak's public keys
- **Role-Based Access Control**: Protect endpoints based on user roles
- **Vue 3 Demo Frontend**: Complete frontend example with Keycloak-js integration

## Prerequisites

- Python 3.13+
- Docker and Docker Compose (for Keycloak)
- Node.js ^22.18.0 || >=24.12.0 (for the Vue demo)

## Project Structure

```
.
├── fastapi_keycloak/          # Main FastAPI application
│   ├── api.py                # API endpoints and routes
│   ├── keycloak_integration.py # Keycloak authentication logic
│   ├── main.py               # FastAPI app factory
│   └── settings.py           # Configuration settings
├── vue-keycloak-demo/        # Vue 3 frontend demo
├── keycloak/                 # Keycloak realm configuration
├── docker-compose.yml        # Keycloak container setup
├── pyproject.toml           # Python dependencies
└── tests/                   # Test suite
```

## Quick Start

### 1. Start Keycloak

Start Keycloak using Docker Compose:

```sh
docker-compose up -d
```

Keycloak will be available at `http://localhost:8090`

- **Admin Console**: http://localhost:8090/auth/admin
- **Username**: `admin`
- **Password**: `admin`

### 2. Install Python Dependencies

```sh
uv sync
# or
pip install -e .
```

### 3. Configure Environment

Create a `.env` file in the project root (see `.env.example` if available):

```env
KEYCLOAK_URL=http://localhost:8090/auth
KEYCLOAK_REALM=example
KEYCLOAK_CLIENT_ID=example-client
KEYCLOAK_CLIENT_SECRET=your-client-secret
CORS_ALLOW_ORIGINS=http://localhost:5173
```

### 4. Run the FastAPI Backend

```sh
python -m fastapi_keycloak.main
```

The API will be available at `http://localhost:8000`

- **API Documentation**: http://localhost:8000/docs
- **Alternative Documentation**: http://localhost:8000/redoc

### 5. Run the Vue Demo Frontend (Optional)

```sh
cd vue-keycloak-demo
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`

## API Endpoints

### Public Endpoints

- `GET /public` - Accessible without authentication

### Protected Endpoints

- `GET /user` - Requires `user` role
- `GET /me/roles` - Returns user roles for the current context (requires `user` role)

## Authentication Flow

1. User authenticates through Keycloak (via the Vue frontend)
2. Keycloak returns a JWT access token
3. Frontend includes the token in the `Authorization` header
4. FastAPI validates the token using Keycloak's public keys
5. Access is granted or denied based on the token's roles

## Development

### Running Tests

```sh
pytest
```

### Code Style

The project uses:
- Type hints throughout
- Pydantic for data validation
- Structured logging with Loguru

## Keycloak Configuration

The project includes a pre-configured Keycloak realm in `keycloak/realms/import/example.json`. This realm is automatically imported when Keycloak starts via Docker Compose.

To customize:
1. Export your realm configuration from Keycloak Admin Console
2. Replace the JSON file in `keycloak/realms/import/`
3. Restart the Keycloak container

## Dependencies

### Core Dependencies

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `python-jose` - JWT token handling
- `pydantic-settings` - Configuration management
- `requests` - HTTP client for Keycloak API
- `loguru` - Logging
- `arrow` - Date/time handling

### Development Dependencies

- `pytest` - Testing framework
- `pytest-asyncio` - Async test support
- `httpx` - HTTP client for testing
- `pytest-mock` - Mocking support

### API Testing 
I've used [Bruno](https://www.usebruno.com/) for API testing, it is a serious competitor to [Postman](https://www.postman.com/).  

## License

Add your license information here.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
