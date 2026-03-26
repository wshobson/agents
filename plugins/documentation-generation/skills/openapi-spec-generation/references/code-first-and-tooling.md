# OpenAPI Code-First Generation and Tooling

Advanced patterns for generating OpenAPI specs from code (Python/FastAPI, TypeScript/tsoa), validation, linting, and SDK generation.

## Template 2: Code-First Generation (Python/FastAPI)

```python
# FastAPI with automatic OpenAPI generation
from fastapi import FastAPI, HTTPException, Query, Path, Depends
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from enum import Enum

app = FastAPI(
    title="User Management API",
    description="API for managing users and profiles",
    version="2.0.0",
    openapi_tags=[
        {"name": "Users", "description": "User operations"},
        {"name": "Profiles", "description": "Profile operations"},
    ],
    servers=[
        {"url": "https://api.example.com/v2", "description": "Production"},
        {"url": "http://localhost:8000", "description": "Development"},
    ],
)

# Enums
class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"
    pending = "pending"

class UserRole(str, Enum):
    user = "user"
    moderator = "moderator"
    admin = "admin"

# Models
class UserBase(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    name: str = Field(..., min_length=1, max_length=100, description="Display name")

class UserCreate(UserBase):
    role: UserRole = Field(default=UserRole.user)
    metadata: Optional[dict] = Field(default=None, description="Custom metadata")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "user@example.com",
                    "name": "John Doe",
                    "role": "user"
                }
            ]
        }
    }

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    status: Optional[UserStatus] = None
    role: Optional[UserRole] = None
    metadata: Optional[dict] = None

class User(UserBase):
    id: UUID = Field(..., description="Unique identifier")
    status: UserStatus
    role: UserRole
    avatar: Optional[str] = Field(None, description="Avatar URL")
    metadata: Optional[dict] = None
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")

    model_config = {"populate_by_name": True}

class Pagination(BaseModel):
    page: int = Field(..., ge=1)
    limit: int = Field(..., ge=1, le=100)
    total: int = Field(..., ge=0)
    total_pages: int = Field(..., ge=0, alias="totalPages")
    has_next: bool = Field(..., alias="hasNext")
    has_prev: bool = Field(..., alias="hasPrev")

class UserListResponse(BaseModel):
    data: List[User]
    pagination: Pagination

class ErrorDetail(BaseModel):
    field: str
    message: str

class ErrorResponse(BaseModel):
    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    details: Optional[List[ErrorDetail]] = None
    request_id: Optional[str] = Field(None, alias="requestId")

# Endpoints
@app.get(
    "/users",
    response_model=UserListResponse,
    tags=["Users"],
    summary="List all users",
    description="Returns a paginated list of users with optional filtering.",
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
    },
)
async def list_users(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[UserStatus] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, min_length=2, max_length=100),
):
    """
    List users with pagination and filtering.

    - **page**: Page number (1-based)
    - **limit**: Number of items per page (max 100)
    - **status**: Filter by user status
    - **search**: Search by name or email
    """
    # Implementation
    pass

@app.post(
    "/users",
    response_model=User,
    status_code=201,
    tags=["Users"],
    summary="Create a new user",
    responses={
        400: {"model": ErrorResponse},
        409: {"model": ErrorResponse, "description": "Email already exists"},
    },
)
async def create_user(user: UserCreate):
    """Create a new user and send welcome email."""
    pass

@app.get(
    "/users/{user_id}",
    response_model=User,
    tags=["Users"],
    summary="Get user by ID",
    responses={404: {"model": ErrorResponse}},
)
async def get_user(
    user_id: UUID = Path(..., description="User ID"),
):
    """Retrieve a specific user by their ID."""
    pass

@app.patch(
    "/users/{user_id}",
    response_model=User,
    tags=["Users"],
    summary="Update user",
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def update_user(
    user_id: UUID = Path(..., description="User ID"),
    user: UserUpdate = ...,
):
    """Update user attributes."""
    pass

@app.delete(
    "/users/{user_id}",
    status_code=204,
    tags=["Users", "Admin"],
    summary="Delete user",
    responses={404: {"model": ErrorResponse}},
)
async def delete_user(
    user_id: UUID = Path(..., description="User ID"),
):
    """Permanently delete a user."""
    pass

# Export OpenAPI spec
if __name__ == "__main__":
    import json
    print(json.dumps(app.openapi(), indent=2))
```

## Template 3: Code-First (TypeScript/Express with tsoa)

```typescript
// tsoa generates OpenAPI from TypeScript decorators

import {
  Controller,
  Get,
  Post,
  Patch,
  Delete,
  Route,
  Path,
  Query,
  Body,
  Response,
  SuccessResponse,
  Tags,
  Security,
  Example,
} from "tsoa";

// Models
interface User {
  /** Unique identifier */
  id: string;
  /** User email address */
  email: string;
  /** Display name */
  name: string;
  status: UserStatus;
  role: UserRole;
  /** Avatar URL */
  avatar?: string;
  /** Custom metadata */
  metadata?: Record<string, unknown>;
  createdAt: Date;
  updatedAt?: Date;
}

enum UserStatus {
  Active = "active",
  Inactive = "inactive",
  Suspended = "suspended",
  Pending = "pending",
}

enum UserRole {
  User = "user",
  Moderator = "moderator",
  Admin = "admin",
}

interface CreateUserRequest {
  email: string;
  name: string;
  role?: UserRole;
  metadata?: Record<string, unknown>;
}

interface UpdateUserRequest {
  name?: string;
  status?: UserStatus;
  role?: UserRole;
  metadata?: Record<string, unknown>;
}

interface Pagination {
  page: number;
  limit: number;
  total: number;
  totalPages: number;
  hasNext: boolean;
  hasPrev: boolean;
}

interface UserListResponse {
  data: User[];
  pagination: Pagination;
}

interface ErrorResponse {
  code: string;
  message: string;
  details?: { field: string; message: string }[];
  requestId?: string;
}

@Route("users")
@Tags("Users")
export class UsersController extends Controller {
  /**
   * List all users with pagination and filtering
   * @param page Page number (1-based)
   * @param limit Items per page (max 100)
   * @param status Filter by user status
   * @param search Search by name or email
   */
  @Get()
  @Security("bearerAuth")
  @Response<ErrorResponse>(400, "Invalid request")
  @Response<ErrorResponse>(401, "Unauthorized")
  @Example<UserListResponse>({
    data: [
      {
        id: "550e8400-e29b-41d4-a716-446655440000",
        email: "john@example.com",
        name: "John Doe",
        status: UserStatus.Active,
        role: UserRole.User,
        createdAt: new Date("2024-01-15T10:30:00Z"),
      },
    ],
    pagination: {
      page: 1,
      limit: 20,
      total: 1,
      totalPages: 1,
      hasNext: false,
      hasPrev: false,
    },
  })
  public async listUsers(
    @Query() page: number = 1,
    @Query() limit: number = 20,
    @Query() status?: UserStatus,
    @Query() search?: string,
  ): Promise<UserListResponse> {
    // Implementation
    throw new Error("Not implemented");
  }

  /**
   * Create a new user
   */
  @Post()
  @Security("bearerAuth")
  @SuccessResponse(201, "Created")
  @Response<ErrorResponse>(400, "Invalid request")
  @Response<ErrorResponse>(409, "Email already exists")
  public async createUser(@Body() body: CreateUserRequest): Promise<User> {
    this.setStatus(201);
    throw new Error("Not implemented");
  }

  /**
   * Get user by ID
   * @param userId User ID
   */
  @Get("{userId}")
  @Security("bearerAuth")
  @Response<ErrorResponse>(404, "User not found")
  public async getUser(@Path() userId: string): Promise<User> {
    throw new Error("Not implemented");
  }

  /**
   * Update user attributes
   * @param userId User ID
   */
  @Patch("{userId}")
  @Security("bearerAuth")
  @Response<ErrorResponse>(400, "Invalid request")
  @Response<ErrorResponse>(404, "User not found")
  public async updateUser(
    @Path() userId: string,
    @Body() body: UpdateUserRequest,
  ): Promise<User> {
    throw new Error("Not implemented");
  }

  /**
   * Delete user
   * @param userId User ID
   */
  @Delete("{userId}")
  @Tags("Users", "Admin")
  @Security("bearerAuth")
  @SuccessResponse(204, "Deleted")
  @Response<ErrorResponse>(404, "User not found")
  public async deleteUser(@Path() userId: string): Promise<void> {
    this.setStatus(204);
  }
}
```

## Template 4: Validation & Linting

```bash
# Install validation tools
npm install -g @stoplight/spectral-cli
npm install -g @redocly/cli

# Spectral ruleset (.spectral.yaml)
cat > .spectral.yaml << 'EOF'
extends: ["spectral:oas", "spectral:asyncapi"]

rules:
  # Enforce operation IDs
  operation-operationId: error

  # Require descriptions
  operation-description: warn
  info-description: error

  # Naming conventions
  operation-operationId-valid-in-url: true

  # Security
  operation-security-defined: error

  # Response codes
  operation-success-response: error

  # Custom rules
  path-params-snake-case:
    description: Path parameters should be snake_case
    severity: warn
    given: "$.paths[*].parameters[?(@.in == 'path')].name"
    then:
      function: pattern
      functionOptions:
        match: "^[a-z][a-z0-9_]*$"

  schema-properties-camelCase:
    description: Schema properties should be camelCase
    severity: warn
    given: "$.components.schemas[*].properties[*]~"
    then:
      function: casing
      functionOptions:
        type: camel
EOF

# Run Spectral
spectral lint openapi.yaml

# Redocly config (redocly.yaml)
cat > redocly.yaml << 'EOF'
extends:
  - recommended

rules:
  no-invalid-media-type-examples: error
  no-invalid-schema-examples: error
  operation-4xx-response: warn
  request-mime-type:
    severity: error
    allowedValues:
      - application/json
  response-mime-type:
    severity: error
    allowedValues:
      - application/json
      - application/problem+json

theme:
  openapi:
    generateCodeSamples:
      languages:
        - lang: curl
        - lang: python
        - lang: javascript
EOF

# Run Redocly
redocly lint openapi.yaml
redocly bundle openapi.yaml -o bundled.yaml
redocly preview-docs openapi.yaml
```

## SDK Generation

```bash
# OpenAPI Generator
npm install -g @openapitools/openapi-generator-cli

# Generate TypeScript client
openapi-generator-cli generate \
  -i openapi.yaml \
  -g typescript-fetch \
  -o ./generated/typescript-client \
  --additional-properties=supportsES6=true,npmName=@myorg/api-client

# Generate Python client
openapi-generator-cli generate \
  -i openapi.yaml \
  -g python \
  -o ./generated/python-client \
  --additional-properties=packageName=api_client

# Generate Go client
openapi-generator-cli generate \
  -i openapi.yaml \
  -g go \
  -o ./generated/go-client
```
