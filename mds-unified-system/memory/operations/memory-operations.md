# MDS Memory Operations

## Overview
The MDS Memory System provides persistent context across agent operations, enabling learning, pattern recognition, and personalized experiences.

## Memory Types

### 1. Project Memory
**Purpose:** Store project-specific context, decisions, and artifacts
**Scope:** Per-project
**Persistence:** Duration of project + archive

### 2. Pattern Library
**Purpose:** Capture successful and failed patterns for learning
**Scope:** Global (across all projects)
**Persistence:** Permanent with versioning

### 3. User Preferences
**Purpose:** Store user customizations and preferences
**Scope:** Per-user
**Persistence:** Permanent

### 4. Domain Knowledge
**Purpose:** Industry and domain-specific knowledge
**Scope:** Global
**Persistence:** Permanent with updates

---

## Operations

### READ Operations

#### Read Project Memory
```json
{
  "operation": "read",
  "type": "project-memory",
  "projectId": "proj_abc123def456",
  "fields": ["techStack", "decisions", "currentPhase"],
  "filters": {
    "decisions.tags": ["architecture"],
    "decisions.reversible": false
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "techStack": {...},
    "decisions": [...],
    "currentPhase": "03-solutioning"
  },
  "metadata": {
    "lastUpdated": "2025-01-15T10:30:00Z",
    "readCount": 42
  }
}
```

#### Read Pattern Library
```json
{
  "operation": "read",
  "type": "pattern-library",
  "query": {
    "category": "architecture",
    "outcome": "success",
    "confidenceScore": {"$gte": 80},
    "applicableWhen": {"$contains": "microservices"}
  },
  "sort": {"confidenceScore": -1},
  "limit": 5
}
```

#### Read User Preferences
```json
{
  "operation": "read",
  "type": "user-preferences",
  "userId": "user_123",
  "fields": ["communication", "development", "workflow"]
}
```

---

### WRITE Operations

#### Create Project Memory
```json
{
  "operation": "create",
  "type": "project-memory",
  "data": {
    "projectName": "E-commerce Platform",
    "projectType": "web-app",
    "techStack": {
      "languages": ["Python", "TypeScript"],
      "frameworks": ["FastAPI", "React"],
      "databases": ["PostgreSQL", "Redis"]
    },
    "currentPhase": "01-analysis",
    "currentTrack": "standard"
  }
}
```

**Response:**
```json
{
  "success": true,
  "projectId": "proj_abc123def456",
  "createdAt": "2025-01-15T10:30:00Z"
}
```

#### Update Project Memory
```json
{
  "operation": "update",
  "type": "project-memory",
  "projectId": "proj_abc123def456",
  "updates": {
    "$set": {
      "currentPhase": "02-planning",
      "status": "in-progress"
    },
    "$push": {
      "decisions": {
        "id": "dec_001",
        "timestamp": "2025-01-15T11:00:00Z",
        "decision": "Use microservices architecture",
        "rationale": "Scalability requirements",
        "madeBy": "architect-review"
      }
    }
  }
}
```

#### Add Pattern to Library
```json
{
  "operation": "create",
  "type": "pattern-library",
  "data": {
    "category": "architecture",
    "name": "Event-Driven Microservices",
    "problem": "Services need loose coupling with async communication",
    "solution": "Implement event bus with message queues",
    "outcome": "success",
    "confidenceScore": 85,
    "applicableWhen": [
      "Multiple services need to communicate",
      "Eventual consistency acceptable",
      "High throughput required"
    ],
    "avoidWhen": [
      "Strong consistency required",
      "Simple CRUD operations only"
    ]
  }
}
```

---

### QUERY Operations

#### Search Patterns
```json
{
  "operation": "query",
  "type": "pattern-library",
  "search": {
    "text": "authentication microservices",
    "fields": ["name", "description", "problem", "solution"]
  },
  "filters": {
    "outcome": "success",
    "confidenceScore": {"$gte": 70}
  }
}
```

#### Find Related Decisions
```json
{
  "operation": "query",
  "type": "project-memory",
  "aggregate": {
    "match": {"decisions.tags": "database"},
    "sort": {"decisions.timestamp": -1},
    "limit": 10
  }
}
```

---

### SYNC Operations

#### Sync Project to Pattern Library
```json
{
  "operation": "sync",
  "source": {
    "type": "project-memory",
    "projectId": "proj_abc123def456"
  },
  "target": {
    "type": "pattern-library"
  },
  "options": {
    "extractPatterns": true,
    "minConfidence": 60,
    "categories": ["architecture", "code"]
  }
}
```

---

## Access Control

### Agent Memory Access Matrix

| Agent Tier | Project Memory | Pattern Library | User Prefs | Domain Knowledge |
|------------|---------------|-----------------|------------|------------------|
| Founder    | Read/Write    | Read/Write      | Read/Write | Read/Write       |
| CEO Agent  | Read/Write    | Read            | Read       | Read             |
| Chief      | Read/Write*   | Read            | Read       | Read             |
| Specialist | Read          | Read            | Read       | Read             |

*Chiefs can only write to their department's projects

---

## Memory Lifecycle

### Project Memory
```
Created → Active → Archived → Deleted (optional)
           ↓
     Patterns extracted to library
```

### Pattern Library
```
Proposed → Validated → Published → Updated → Deprecated
```

### User Preferences
```
Created → Active → Updated → (never deleted, only reset)
```

---

## Memory Tagging Convention

Use consistent tags for easy retrieval:

```
[MDS-MEMORY:project:{projectId}]
[MDS-MEMORY:pattern:{patternId}]
[MDS-MEMORY:decision:{decisionId}]
[MDS-MEMORY:artifact:{artifactId}]
```

---

## Integration with Agents

### Reading Memory in Agent Context
```markdown
## Memory Context
When you receive context tagged with [MDS-MEMORY], treat it as persistent project knowledge.

Example:
[MDS-MEMORY:project:proj_abc123]
- Tech Stack: Python, FastAPI, PostgreSQL
- Current Phase: Implementation
- Key Decision: Using event sourcing for audit trail
```

### Writing to Memory
Agents should output memory updates in structured format:

```markdown
[MDS-MEMORY-UPDATE]
type: decision
data:
  decision: "Implemented rate limiting on API endpoints"
  rationale: "Prevent abuse and ensure fair usage"
  reversible: true
  tags: ["security", "api"]
[/MDS-MEMORY-UPDATE]
```

---

## Error Handling

### Memory Read Failures
- Return cached data if available
- Log error and continue with degraded context
- Never halt operation due to memory read failure

### Memory Write Failures
- Queue write for retry
- Log error with full context
- Notify on repeated failures
