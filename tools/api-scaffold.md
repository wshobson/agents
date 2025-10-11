# API Scaffold Generator

You are an API development expert specializing in creating production-ready, scalable REST APIs with modern frameworks. Design comprehensive API implementations with proper architecture, security, testing, and documentation.

## Context
The user needs to create a new API endpoint or service with complete implementation including models, validation, security, testing, and deployment configuration. Focus on production-ready code that follows industry best practices.

## Requirements
$ARGUMENTS

## Instructions

### 1. API Framework Selection

Choose the appropriate framework based on requirements:

**Framework Comparison Matrix**
```python
def select_framework(requirements):
    """Select optimal API framework based on requirements"""
    
    frameworks = {
        'fastapi': {
            'best_for': ['high_performance', 'async_operations', 'type_safety', 'modern_python'],
            'strengths': ['Auto OpenAPI docs', 'Type hints', 'Async support', 'Fast performance'],
            'use_cases': ['Microservices', 'Data APIs', 'ML APIs', 'Real-time systems'],
            'example_stack': 'FastAPI + Pydantic + SQLAlchemy + PostgreSQL'
        },
        'django_rest': {
            'best_for': ['rapid_development', 'orm_integration', 'admin_interface', 'large_teams'],
            'strengths': ['Batteries included', 'ORM', 'Admin panel', 'Mature ecosystem'],
            'use_cases': ['CRUD applications', 'Content management', 'Enterprise systems'],
            'example_stack': 'Django + DRF + PostgreSQL + Redis'
        },
        'express': {
            'best_for': ['node_ecosystem', 'real_time', 'frontend_integration', 'javascript_teams'],
            'strengths': ['NPM ecosystem', 'JSON handling', 'WebSocket support', 'Fast development'],
            'use_cases': ['Real-time apps', 'API gateways', 'Serverless functions'],
            'example_stack': 'Express + TypeScript + Prisma + PostgreSQL'
        },
        'spring_boot': {
            'best_for': ['enterprise', 'java_teams', 'complex_business_logic', 'microservices'],
            'strengths': ['Enterprise features', 'Dependency injection', 'Security', 'Monitoring'],
            'use_cases': ['Enterprise APIs', 'Financial systems', 'Complex microservices'],
            'example_stack': 'Spring Boot + JPA + PostgreSQL + Redis'
        }
    }
    
    # Selection logic based on requirements
    if 'high_performance' in requirements:
        return frameworks['fastapi']
    elif 'enterprise' in requirements:
        return frameworks['spring_boot']
    elif 'rapid_development' in requirements:
        return frameworks['django_rest']
    elif 'real_time' in requirements:
        return frameworks['express']
    
    return frameworks['fastapi']  # Default recommendation
```

### 2. FastAPI Implementation

Complete FastAPI API implementation:

**Project Structure**
```
project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── endpoints/
│   │       │   ├── users.py
│   │       │   └── items.py
│   │       └── api.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── item_service.py
│   └── tests/
│       ├── conftest.py
│       ├── test_users.py
│       └── test_items.py
├── alembic/
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

**Core Configuration**
```python
# app/core/config.py
from pydantic import BaseSettings, validator
from typing import Optional, Dict, Any
import secrets

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    SERVER_NAME: str = "localhost"
    SERVER_HOST: str = "0.0.0.0"
    
    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = "app"
    DATABASE_URL: Optional[str] = None
    
    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return f"postgresql://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@{values.get('POSTGRES_SERVER')}/{values.get('POSTGRES_DB')}"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Security
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

**Database Setup**
```python
# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import redis

from app.core.config import settings

# PostgreSQL
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=StaticPool,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,
    echo=settings.LOG_LEVEL == "DEBUG"
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Redis
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_redis():
    """Dependency to get Redis connection"""
    return redis_client
```

**Security Implementation**
```python
# app/core/security.py
from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials) -> dict:
    """Verify JWT token"""
    try:
        payload = jwt.decode(
            credentials.credentials, 
            settings.SECRET_KEY, 
            algorithms=["HS256"]
        )
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate password hash"""
    return pwd_context.hash(password)
```

**Models Implementation**
```python
# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    items = relationship("Item", back_populates="owner")

# app/models/item.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="items")
```

**Pydantic Schemas**
```python
# app/schemas/user.py
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

class UserInDB(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True

class User(UserInDB):
    pass

# app/schemas/item.py
from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    @validator('title')
    def validate_title(cls, v):
        if len(v.strip()) < 3:
            raise ValueError('Title must be at least 3 characters')
        return v.strip()

class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class ItemInDB(ItemBase):
    id: int
    is_active: bool
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True

class Item(ItemInDB):
    pass
```

**Service Layer**
```python
# app/services/user_service.py
from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get list of users"""
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def create_user(self, user_create: UserCreate) -> User:
        """Create new user"""
        # Check if user exists
        if self.get_user_by_email(user_create.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user
        hashed_password = get_password_hash(user_create.password)
        db_user = User(
            email=user_create.email,
            username=user_create.username,
            full_name=user_create.full_name,
            hashed_password=hashed_password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        """Update user"""
        db_user = self.get_user(user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user"""
        user = self.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user
```

**Rate Limiting Middleware**
```python
# app/core/rate_limiting.py
import time
from typing import Callable
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import redis

from app.core.config import settings
from app.core.database import get_redis

class RateLimiter:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.requests = settings.RATE_LIMIT_REQUESTS
        self.window = settings.RATE_LIMIT_WINDOW
    
    async def __call__(self, request: Request, call_next: Callable):
        # Get client identifier
        client_ip = request.client.host
        user_id = getattr(request.state, 'user_id', None)
        key = f"rate_limit:{user_id or client_ip}"
        
        # Check rate limit
        current = self.redis.get(key)
        if current is None:
            # First request in window
            self.redis.setex(key, self.window, 1)
        else:
            current = int(current)
            if current >= self.requests:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded. Try again in {self.redis.ttl(key)} seconds",
                    headers={"Retry-After": str(self.redis.ttl(key))}
                )
            self.redis.incr(key)
        
        response = await call_next(request)
        
        # Add rate limit headers
        remaining = max(0, self.requests - int(self.redis.get(key) or 0))
        response.headers["X-RateLimit-Limit"] = str(self.requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(time.time()) + self.redis.ttl(key))
        
        return response
```

**API Endpoints**
```python
# app/api/v1/endpoints/users.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_token, security
from app.schemas.user import User, UserCreate, UserUpdate
from app.services.user_service import UserService

router = APIRouter()

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_create: UserCreate,
    db: Session = Depends(get_db)
):
    """Create new user"""
    service = UserService(db)
    return service.create_user(user_create)

@router.get("/me", response_model=User)
async def get_current_user(
    token: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get current user profile"""
    service = UserService(db)
    user = service.get_user_by_email(token["sub"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    """Get user by ID"""
    service = UserService(db)
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    """Update user"""
    service = UserService(db)
    return service.update_user(user_id, user_update)

@router.get("/", response_model=List[User])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    """List users"""
    service = UserService(db)
    return service.get_users(skip=skip, limit=limit)
```

**Main Application**
```python
# app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import logging
import time
import uuid

from app.core.config import settings
from app.core.rate_limiting import RateLimiter
from app.core.database import get_redis
from app.api.v1.api import api_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Production API",
    description="A production-ready API with FastAPI",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", settings.SERVER_NAME]
)

# Rate limiting middleware
rate_limiter = RateLimiter(get_redis())
app.middleware("http")(rate_limiter)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time and correlation ID"""
    correlation_id = str(uuid.uuid4())
    request.state.correlation_id = correlation_id
    
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Correlation-ID"] = correlation_id
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    correlation_id = getattr(request.state, 'correlation_id', 'unknown')
    
    logger.error(
        f"Unhandled exception: {exc}",
        extra={"correlation_id": correlation_id, "path": request.url.path}
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "correlation_id": correlation_id
        }
    )

# Include routers
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to the Production API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.SERVER_HOST,
        port=8000,
        reload=True
    )
```

### 3. Express.js Implementation

Complete Express.js TypeScript implementation:

**Project Structure & Setup**
```typescript
// package.json
{
  "name": "express-api",
  "version": "1.0.0",
  "scripts": {
    "dev": "nodemon src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js",
    "test": "jest",
    "test:watch": "jest --watch"
  },
  "dependencies": {
    "express": "^4.18.2",
    "express-rate-limit": "^6.10.0",
    "helmet": "^7.0.0",
    "cors": "^2.8.5",
    "compression": "^1.7.4",
    "morgan": "^1.10.0",
    "joi": "^17.9.2",
    "jsonwebtoken": "^9.0.2",
    "bcryptjs": "^2.4.3",
    "prisma": "^5.1.0",
    "@prisma/client": "^5.1.0",
    "redis": "^4.6.7",
    "winston": "^3.10.0"
  },
  "devDependencies": {
    "@types/express": "^4.17.17",
    "@types/node": "^20.4.5",
    "typescript": "^5.1.6",
    "nodemon": "^3.0.1",
    "jest": "^29.6.1",
    "@types/jest": "^29.5.3",
    "supertest": "^6.3.3"
  }
}

// src/types/index.ts
export interface User {
  id: string;
  email: string;
  username: string;
  fullName?: string;
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export interface CreateUserRequest {
  email: string;
  username: string;
  password: string;
  fullName?: string;
}

export interface AuthTokenPayload {
  userId: string;
  email: string;
  iat: number;
  exp: number;
}

// src/config/index.ts
import { config as dotenvConfig } from 'dotenv';

dotenvConfig();

export const config = {
  port: parseInt(process.env.PORT || '3000'),
  jwtSecret: process.env.JWT_SECRET || 'your-secret-key',
  jwtExpiresIn: process.env.JWT_EXPIRES_IN || '7d',
  redisUrl: process.env.REDIS_URL || 'redis://localhost:6379',
  databaseUrl: process.env.DATABASE_URL || 'postgresql://user:pass@localhost:5432/db',
  nodeEnv: process.env.NODE_ENV || 'development',
  corsOrigins: process.env.CORS_ORIGINS?.split(',') || ['http://localhost:3000'],
  rateLimitMax: parseInt(process.env.RATE_LIMIT_MAX || '100'),
  rateLimitWindow: parseInt(process.env.RATE_LIMIT_WINDOW_MS || '900000'), // 15 minutes
};

// src/middleware/validation.ts
import { Request, Response, NextFunction } from 'express';
import Joi from 'joi';

export const validateRequest = (schema: Joi.ObjectSchema) => {
  return (req: Request, res: Response, next: NextFunction) => {
    const { error } = schema.validate(req.body);
    
    if (error) {
      return res.status(400).json({
        success: false,
        message: 'Validation error',
        details: error.details.map(detail => ({
          field: detail.path.join('.'),
          message: detail.message
        }))
      });
    }
    
    next();
  };
};

// Validation schemas
export const userSchemas = {
  create: Joi.object({
    email: Joi.string().email().required(),
    username: Joi.string().alphanum().min(3).max(30).required(),
    password: Joi.string().min(8).required(),
    fullName: Joi.string().max(100).optional()
  }),
  
  update: Joi.object({
    email: Joi.string().email().optional(),
    username: Joi.string().alphanum().min(3).max(30).optional(),
    fullName: Joi.string().max(100).optional(),
    isActive: Joi.boolean().optional()
  })
};

// src/middleware/auth.ts
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { config } from '../config';
import { AuthTokenPayload } from '../types';

declare global {
  namespace Express {
    interface Request {
      user?: AuthTokenPayload;
    }
  }
}

export const authenticateToken = (req: Request, res: Response, next: NextFunction) => {
  const authHeader = req.headers.authorization;
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({
      success: false,
      message: 'Access token required'
    });
  }

  try {
    const decoded = jwt.verify(token, config.jwtSecret) as AuthTokenPayload;
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(403).json({
      success: false,
      message: 'Invalid or expired token'
    });
  }
};

// src/services/userService.ts
import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { config } from '../config';
import { CreateUserRequest, User } from '../types';

const prisma = new PrismaClient();

export class UserService {
  async createUser(userData: CreateUserRequest): Promise<User> {
    // Check if user exists
    const existingUser = await prisma.user.findFirst({
      where: {
        OR: [
          { email: userData.email },
          { username: userData.username }
        ]
      }
    });

    if (existingUser) {
      throw new Error('User with this email or username already exists');
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(userData.password, 12);

    // Create user
    const user = await prisma.user.create({
      data: {
        email: userData.email,
        username: userData.username,
        fullName: userData.fullName,
        hashedPassword,
        isActive: true
      }
    });

    // Remove password from response
    const { hashedPassword: _, ...userWithoutPassword } = user;
    return userWithoutPassword as User;
  }

  async getUserById(id: string): Promise<User | null> {
    const user = await prisma.user.findUnique({
      where: { id },
      select: {
        id: true,
        email: true,
        username: true,
        fullName: true,
        isActive: true,
        createdAt: true,
        updatedAt: true
      }
    });

    return user;
  }

  async authenticateUser(email: string, password: string): Promise<string | null> {
    const user = await prisma.user.findUnique({
      where: { email }
    });

    if (!user || !await bcrypt.compare(password, user.hashedPassword)) {
      return null;
    }

    const token = jwt.sign(
      { userId: user.id, email: user.email },
      config.jwtSecret,
      { expiresIn: config.jwtExpiresIn }
    );

    return token;
  }

  async getUsers(skip = 0, take = 10): Promise<User[]> {
    return await prisma.user.findMany({
      skip,
      take,
      select: {
        id: true,
        email: true,
        username: true,
        fullName: true,
        isActive: true,
        createdAt: true,
        updatedAt: true
      }
    });
  }
}

// src/controllers/userController.ts
import { Request, Response } from 'express';
import { UserService } from '../services/userService';
import { logger } from '../utils/logger';

const userService = new UserService();

export class UserController {
  async createUser(req: Request, res: Response) {
    try {
      const user = await userService.createUser(req.body);
      
      logger.info('User created successfully', { userId: user.id });
      
      res.status(201).json({
        success: true,
        message: 'User created successfully',
        data: user
      });
    } catch (error) {
      logger.error('Error creating user', { error: error.message });
      
      res.status(400).json({
        success: false,
        message: error.message || 'Failed to create user'
      });
    }
  }

  async getUser(req: Request, res: Response) {
    try {
      const { id } = req.params;
      const user = await userService.getUserById(id);

      if (!user) {
        return res.status(404).json({
          success: false,
          message: 'User not found'
        });
      }

      res.json({
        success: true,
        data: user
      });
    } catch (error) {
      logger.error('Error fetching user', { error: error.message });
      
      res.status(500).json({
        success: false,
        message: 'Internal server error'
      });
    }
  }

  async getCurrentUser(req: Request, res: Response) {
    try {
      const user = await userService.getUserById(req.user!.userId);

      if (!user) {
        return res.status(404).json({
          success: false,
          message: 'User not found'
        });
      }

      res.json({
        success: true,
        data: user
      });
    } catch (error) {
      logger.error('Error fetching current user', { error: error.message });
      
      res.status(500).json({
        success: false,
        message: 'Internal server error'
      });
    }
  }

  async loginUser(req: Request, res: Response) {
    try {
      const { email, password } = req.body;
      const token = await userService.authenticateUser(email, password);

      if (!token) {
        return res.status(401).json({
          success: false,
          message: 'Invalid email or password'
        });
      }

      res.json({
        success: true,
        message: 'Login successful',
        data: { token }
      });
    } catch (error) {
      logger.error('Error during login', { error: error.message });
      
      res.status(500).json({
        success: false,
        message: 'Internal server error'
      });
    }
  }
}
```

### 4. Testing Implementation

Comprehensive testing setup:

**FastAPI Tests**
```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.core.config import settings

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client

# tests/test_users.py
import pytest
from fastapi.testclient import TestClient

def test_create_user(client: TestClient):
    """Test user creation"""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert "id" in data
    assert "hashed_password" not in data

def test_create_user_duplicate_email(client: TestClient):
    """Test creating user with duplicate email"""
    user_data = {
        "email": "duplicate@example.com",
        "username": "user1",
        "password": "password123"
    }
    
    # Create first user
    response1 = client.post("/api/v1/users/", json=user_data)
    assert response1.status_code == 201
    
    # Try to create second user with same email
    user_data["username"] = "user2"
    response2 = client.post("/api/v1/users/", json=user_data)
    assert response2.status_code == 400
    assert "already registered" in response2.json()["detail"]

def test_get_user_unauthorized(client: TestClient):
    """Test accessing protected endpoint without token"""
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_user_authentication_flow(client: TestClient):
    """Test complete authentication flow"""
    # Create user
    user_data = {
        "email": "auth@example.com",
        "username": "authuser",
        "password": "authpassword123"
    }
    
    create_response = client.post("/api/v1/users/", json=user_data)
    assert create_response.status_code == 201
    
    # Login
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    login_response = client.post("/api/v1/auth/login", json=login_data)
    assert login_response.status_code == 200
    
    token = login_response.json()["access_token"]
    
    # Access protected endpoint
    headers = {"Authorization": f"Bearer {token}"}
    profile_response = client.get("/api/v1/users/me", headers=headers)
    assert profile_response.status_code == 200
    
    profile_data = profile_response.json()
    assert profile_data["email"] == user_data["email"]
```

### 5. Deployment Configuration

**Docker Configuration**
```dockerfile
# Dockerfile (FastAPI)
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Docker Compose**
```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/appdb
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    volumes:
      - ./app:/app/app
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=appdb
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - api
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

### 6. CI/CD Pipeline

**GitHub Actions Workflow**
```yaml
# .github/workflows/api.yml
name: API CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run linting
      run: |
        flake8 app tests
        black --check app tests
        isort --check-only app tests
    
    - name: Run type checking
      run: mypy app
    
    - name: Run security scan
      run: bandit -r app
    
    - name: Run tests
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        REDIS_URL: redis://localhost:6379
      run: |
        pytest tests/ -v --cov=app --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
    
    - name: Log in to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=sha
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Deploy to staging
      run: |
        echo "Deploying to staging environment"
        # Add deployment commands here
```

### 7. Monitoring and Observability

**Prometheus Metrics**
```python
# app/core/metrics.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import Request
import time

# Metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

ACTIVE_CONNECTIONS = Gauge(
    'active_connections',
    'Active connections'
)

async def record_metrics(request: Request, call_next):
    """Record metrics for each request"""
    start_time = time.time()
    
    ACTIVE_CONNECTIONS.inc()
    
    try:
        response = await call_next(request)
        
        # Record metrics
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        
        REQUEST_DURATION.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(time.time() - start_time)
        
        return response
    
    finally:
        ACTIVE_CONNECTIONS.dec()

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(
        generate_latest(),
        media_type="text/plain"
    )
```

## Cross-Command Integration

This command integrates seamlessly with other Claude Code commands to create complete development workflows:

### 1. Complete API Development Workflow

**Standard Development Pipeline:**
```bash
# 1. Start with API scaffold
/api-scaffold "User management API with FastAPI, PostgreSQL, and JWT auth"

# 2. Set up comprehensive testing
/test-harness "FastAPI API with unit, integration, and load testing using pytest and locust"

# 3. Security validation
/security-scan "FastAPI application with authentication endpoints"

# 4. Container optimization
/docker-optimize "FastAPI application with PostgreSQL and Redis dependencies"

# 5. Kubernetes deployment
/k8s-manifest "FastAPI microservice with PostgreSQL, Redis, and ingress"

# 6. Frontend integration (if needed)
/frontend-optimize "React application connecting to FastAPI backend"
```

### 2. Database-First Development

**When starting with existing data:**
```bash
# 1. Handle database migrations first
/db-migrate "PostgreSQL schema migration from legacy system to modern structure"

# 2. Generate API based on migrated schema
/api-scaffold "REST API for migrated PostgreSQL schema with auto-generated models"

# 3. Continue with standard pipeline...
```

### 3. Microservices Architecture

**For distributed systems:**
```bash
# Generate multiple related APIs
/api-scaffold "User service with authentication and profile management"
/api-scaffold "Order service with payment processing and inventory"
/api-scaffold "Notification service with email and push notifications"

# Containerize all services
/docker-optimize "Microservices architecture with service discovery"

# Deploy as distributed system
/k8s-manifest "Microservices deployment with service mesh and monitoring"
```

### 4. Integration with Generated Code

**Test Integration Setup:**
```yaml
# After running /api-scaffold, use this with /test-harness
test_config:
  api_base_url: "http://localhost:8000"
  test_database: "postgresql://test:test@localhost:5432/test_db"
  authentication:
    test_user: "test@example.com"
    test_password: "testpassword123"
  
  endpoints_to_test:
    - POST /api/v1/users/
    - POST /api/v1/auth/login
    - GET /api/v1/users/me
    - GET /api/v1/users/{id}
```

**Security Scan Configuration:**
```yaml
# Configuration for /security-scan after API scaffold
security_scan:
  target: "localhost:8000"
  authentication_endpoints:
    - "/api/v1/auth/login"
    - "/api/v1/auth/refresh"
  protected_endpoints:
    - "/api/v1/users/me"
    - "/api/v1/users/{id}"
  vulnerability_tests:
    - jwt_token_validation
    - sql_injection
    - xss_prevention
    - rate_limiting
```

**Docker Integration:**
```dockerfile
# Generated Dockerfile can be optimized with /docker-optimize
# Multi-stage build for FastAPI application
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim as runtime
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Kubernetes Deployment:**
```yaml
# Use this configuration with /k8s-manifest
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
      - name: api
        image: api:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: database-url
        - name: JWT_SECRET
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: jwt-secret
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### 5. CI/CD Pipeline Integration

**Complete pipeline using multiple commands:**
```yaml
name: Full Stack CI/CD

on:
  push:
    branches: [main]

jobs:
  api-test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    # Test API (generated by /api-scaffold)
    - name: Run API tests
      run: |
        # Use test configuration from /test-harness
        pytest tests/ -v --cov=app
    
    # Security scan (from /security-scan)
    - name: Security scan
      run: |
        bandit -r app/
        safety check
    
    # Build optimized container (from /docker-optimize)
    - name: Build container
      run: |
        docker build -f Dockerfile.optimized -t api:${{ github.sha }} .
    
    # Deploy to Kubernetes (from /k8s-manifest)
    - name: Deploy to staging
      run: |
        kubectl apply -f k8s/staging/
        kubectl set image deployment/api-deployment api=api:${{ github.sha }}
```

### 6. Frontend-Backend Integration

**When building full-stack applications:**
```bash
# 1. Backend API
/api-scaffold "REST API with user management and data operations"

# 2. Frontend application
/frontend-optimize "React SPA with API integration, authentication, and state management"

# 3. Integration testing
/test-harness "End-to-end testing for React frontend and FastAPI backend"

# 4. Unified deployment
/k8s-manifest "Full-stack deployment with API, frontend, and database"
```

**Frontend API Integration Code:**
```typescript
// Generated API client for frontend
// Use this pattern with /frontend-optimize
export class APIClient {
  private baseURL: string;
  private token: string | null = null;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  setAuthToken(token: string) {
    this.token = token;
  }

  private async request<T>(
    endpoint: string, 
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...(this.token && { Authorization: `Bearer ${this.token}` }),
      ...options.headers,
    };

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }

    return response.json();
  }

  // User management methods (matching API scaffold)
  async createUser(userData: CreateUserRequest): Promise<User> {
    return this.request<User>('/api/v1/users/', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async login(credentials: LoginRequest): Promise<AuthResponse> {
    return this.request<AuthResponse>('/api/v1/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  }

  async getCurrentUser(): Promise<User> {
    return this.request<User>('/api/v1/users/me');
  }
}
```

### 7. Monitoring and Observability Integration

**Complete observability stack:**
```bash
# After API deployment, add monitoring
/api-scaffold "Monitoring endpoints with Prometheus metrics and health checks"

# Use with Kubernetes monitoring
/k8s-manifest "Kubernetes deployment with Prometheus, Grafana, and alerting"
```

This integrated approach ensures all components work together seamlessly, creating a production-ready system with proper testing, security, deployment, and monitoring.

## Validation Checklist

- [ ] Framework selected based on requirements
- [ ] Project structure follows best practices
- [ ] Authentication and authorization implemented
- [ ] Input validation and sanitization in place
- [ ] Rate limiting configured
- [ ] Error handling comprehensive
- [ ] Logging and monitoring setup
- [ ] Tests written and passing
- [ ] Security measures implemented
- [ ] API documentation generated
- [ ] Deployment configuration ready
- [ ] CI/CD pipeline configured

Focus on creating production-ready APIs with proper architecture, security, testing, and operational concerns addressed from the start.
