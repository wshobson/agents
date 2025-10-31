---
name: cartridge-framework
description: Master Tarantool Cartridge cluster management framework for building scalable, highly available database applications. Design topology, implement roles, build web APIs, and manage production clusters. Use when developing Cartridge applications.
---

# Tarantool Cartridge Framework

Complete guide to building distributed applications with Tarantool Cartridge.

## Language Support

This skill documentation and all guidance adapt to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

When using this skill, specify your preferred language in your request.

## Purpose

Design and implement highly available distributed database applications using Cartridge framework.

## When to Use This Skill

- Build Cartridge-based applications
- Design cluster topology
- Implement custom roles
- Create web API handlers
- Configure automatic failover
- Manage production clusters

## Core Concepts

### Cartridge Architecture

**Cartridge Cluster Components**
```
Cartridge Cluster
├── Stateful Roles (Data Storage)
│   ├── Storage Role (vshard storage)
│   ├── Custom Roles (your business logic)
│   └── Replica Groups
├── Stateless Roles (API/Router)
│   ├── Router Role (vshard router)
│   ├── Custom API Role
│   └── Can scale independently
└── Control Plane
    └── Cluster Management UI
```

### Cartridge Project Structure

**Standard Layout**
```
cartridge-app/
├── cartridge/
│   ├── roles/
│   │   ├── custom.lua
│   │   ├── storage.lua
│   │   └── router.lua
│   ├── topology.lua
│   ├── init.lua
│   └── app-config.yaml
├── init.lua
├── main.lua
└── rockspec
```

### Role Definition

**Basic Role Structure**
```lua
-- cartridge/roles/custom.lua
local role = {}

function role.init()
    box.cfg({...})
end

function role.stop()
    -- Cleanup
end

function role.validate_config(cfg)
    -- Validate configuration
    return true
end

function role.apply_config(cfg)
    -- Apply configuration
end

return role
```

**Custom Role with Functions**
```lua
local role = {}

function role.init()
    -- Initialize space
    box.schema.space.create('users', {
        format = {
            {name = 'id', type = 'unsigned'},
            {name = 'name', type = 'string'}
        }
    })

    box.space.users:create_index('primary', {
        parts = {'id'}
    })
end

-- Exported function
function role.get_user(user_id)
    return box.space.users:get(user_id)
end

return role
```

### Storage Role

**Storage Configuration**
```yaml
# topologies.yaml
my-topology:
  stateless:
    cartridge-router:
      - server-1
  stateful:
    # Storage group with replica configuration
    storage-group:
      - server-2
      - server-3
      - server-4
```

**Storage Role Setup**
```lua
-- cartridge/roles/storage.lua
local role = {}

function role.init()
    -- Create spaces
    box.schema.space.create('data', {
        format = {
            {name = 'bucket_id', type = 'unsigned'},
            {name = 'key', type = 'string'},
            {name = 'value', type = 'string'}
        }
    })

    box.space.data:create_index('primary', {
        parts = {'bucket_id', 'key'}
    })

    box.space.data:create_index('bucket_id', {
        parts = {'bucket_id'}
    })
end

function role.get_data(bucket_id, key)
    return box.space.data:get({bucket_id, key})
end

return role
```

### Router Role

**Router Configuration**
```lua
-- cartridge/roles/router.lua
local vshard = require('vshard')
local role = {}

function role.init()
    -- Initialize router
    vshard.router.cfg({...})
end

function role.get_data(key)
    local bucket_id = vshard.router.bucket_id(key)
    return vshard.router:call(bucket_id, 'read', 'get_data', {bucket_id, key})
end

return role
```

### HTTP API with Cartridge

**Creating HTTP Endpoints**
```lua
-- cartridge/roles/api.lua
local role = {}

local function get_user_handler(req)
    local user_id = tonumber(req.json.user_id)
    if not user_id then
        return {status = 400, body = 'Invalid user_id'}
    end

    local user = box.space.users:get(user_id)
    if not user then
        return {status = 404, body = 'User not found'}
    end

    return {
        status = 200,
        body = user:totable()
    }
end

function role.init()
    local httpd = require('http.server')
    local server = httpd.new('127.0.0.1', 8081)

    server:route({path = '/user'}, get_user_handler)
    server:start()
end

return role
```

### Cluster Configuration

**Dynamic Configuration**
```yaml
# config.yaml
vshard:
  sharding:
    - replicas:
        storage-1: {uri: 'localhost:3301'}
      bucket_count: 65536

    - replicas:
        storage-2: {uri: 'localhost:3302'}

topology:
  replicasets:
    router:
      master: server-1
      roles: ['vshard-router']

    storage-1:
      master: server-2
      replicas: [server-3]
      roles: ['vshard-storage']

    storage-2:
      master: server-4
      replicas: [server-5]
      roles: ['vshard-storage']
```

### Automatic Failover

**Failover Configuration**
```lua
-- In topology configuration
replicasets = {
    storage_group = {
        leader = 'server-1',  -- Master will failover if down
        instances = {
            server-1 = {...},
            server-2 = {...}  -- Replica, becomes master if needed
        }
    }
}
```

**Health Checks**
```lua
-- Cartridge performs automatic health checks
-- Promotes replica to master if leader is unhealthy
-- No manual intervention needed
```

### Cartridge Admin UI

**UI Features**
- Cluster topology visualization
- Server status monitoring
- Configuration management
- Log viewing
- Role management

**Accessing UI**
```
http://localhost:8081
(Default admin UI port)
```

### Development with Cartridge

**Creating New Project**
```bash
cartridge create --name myapp
cd myapp
cartridge start
```

**Running Tests**
```lua
-- test/integration/api_test.lua
local helper = require('cartridge.test-helpers')

describe('API', function()
    before_each(function()
        cg.cartridge = helper.Cluster:new({
            server_command = _G.TEST_SERVER_COMMAND,
            datadir = _G.TEST_DATADIR,
        })
    end)

    it('should get user', function()
        local result = cg.cartridge:server('router'):call('get_user', {1})
        assert.equals(result.name, 'John')
    end)
end)
```

## Best Practices

1. **Cluster Design**
   - Plan replica groups carefully
   - Use odd number of replicas for quorum
   - Separate stateless and stateful roles

2. **Configuration**
   - Use configuration management for production
   - Version control all configs
   - Test config changes in staging

3. **Scaling**
   - Add stateless routers to scale reads
   - Add storage groups for more capacity
   - Use load balancer for multiple routers

4. **Monitoring**
   - Monitor replica lag
   - Track failover events
   - Monitor application metrics

5. **Deployment**
   - Use containers for consistency
   - Automate with Kubernetes Operator
   - Plan capacity for growth

## Common Pitfalls

- **Uneven Replica Counts**: Affects failover reliability
- **No Load Balancer**: Single router becomes bottleneck
- **Mixing Stateful/Stateless**: Complexity increases
- **Poor Configuration Management**: Hard to reproduce issues
- **Insufficient Monitoring**: Miss problems until critical

## Related Skills

- `tarantool-architecture` - Overall architecture design
- `vshard-sharding` - Sharding within Cartridge
- `lua-development` - Implementing custom roles
- `replication-ha` - Failover configuration
- `tarantool-performance` - Performance optimization
