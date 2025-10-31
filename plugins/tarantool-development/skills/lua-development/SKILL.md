---
name: lua-development
description: Master Lua programming for Tarantool applications, stored procedures, triggers, and business logic implementation. Use when developing Tarantool Lua code, creating stored procedures, or implementing application logic.
---

# Lua Development for Tarantool

Complete guide to Lua programming for Tarantool database applications.

## Language Support

This skill documentation and all guidance adapt to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

When using this skill, specify your preferred language in your request.

## Purpose

Write efficient, reliable Lua code for Tarantool applications, stored procedures, and business logic.

## When to Use This Skill

- Develop Tarantool stored procedures
- Create triggers for automatic data processing
- Implement business logic in Lua
- Optimize performance with Lua functions
- Create Tarantool modules and extensions
- Build HTTP API handlers

## Core Concepts

### Tarantool Lua Environment

**Tarantool Lua Version**
- Lua 5.1 compatible
- LuaJIT compilation available
- Fiber-based concurrency model
- Integrated with Tarantool box module

### Box Module - Database Operations

**Basic CRUD Operations**
```lua
-- Insert
local space = box.space.users
space:insert({1, 'John', 'john@example.com'})

-- Select
local user = space:get(1)
local all_users = space:select()

-- Update
space:update(1, {{'=', 2, 'Jane'}})

-- Delete
space:delete(1)
```

**Bulk Operations**
```lua
-- Batch insert
local users = {
    {1, 'John'},
    {2, 'Jane'},
    {3, 'Bob'}
}
for _, user in ipairs(users) do
    box.space.users:insert(user)
end
```

### Transactions

**Basic Transaction**
```lua
box.begin()
try
    -- Multiple operations
    box.space.users:insert({1, 'John'})
    box.space.orders:insert({101, 1, 100})
    box.commit()
catch e
    box.rollback()
end
```

**Savepoints for Complex Logic**
```lua
box.begin()
box.space.users:insert({1, 'John'})

box.savepoint()
if condition then
    box.space.orders:insert({101, 1, 100})
else
    box.rollback_to_savepoint()
end

box.commit()
```

### Stored Procedures

**Function Definition**
```lua
local function process_order(user_id, items, amount)
    box.begin()

    -- Validate user exists
    local user = box.space.users:get(user_id)
    if not user then
        box.rollback()
        return nil, "User not found"
    end

    -- Create order
    local order = box.space.orders:insert({
        box.NULL, user_id, amount, os.time()
    })

    -- Insert order items
    for _, item in ipairs(items) do
        box.space.order_items:insert({
            box.NULL, order[1], item.product_id, item.quantity
        })
    end

    box.commit()
    return order
end

-- Register as stored procedure
box.schema.func.create('process_order', {if_not_exists = true})
_G.process_order = process_order
```

### Triggers

**On Insert Trigger**
```lua
local function audit_insert(space, tuple)
    box.space.audit_log:insert({
        box.NULL,
        space.name,
        'INSERT',
        tuple,
        os.time()
    })
    return tuple
end

box.space.users:on_replace(audit_insert)
```

**On Update Trigger**
```lua
local function audit_update(space, old_tuple, new_tuple)
    if old_tuple ~= new_tuple then
        box.space.audit_log:insert({
            box.NULL,
            space.name,
            'UPDATE',
            new_tuple,
            os.time()
        })
    end
    return new_tuple
end

box.space.users:on_replace(audit_update)
```

### Fiber-Based Concurrency

**Creating Fibers**
```lua
local fiber = require('fiber')

-- Create fiber
local function worker()
    for i = 1, 10 do
        print("Working... " .. i)
        fiber.sleep(1)
    end
end

local f = fiber.create(worker)
```

**Fiber Synchronization**
```lua
local fiber = require('fiber')
local cond = fiber.cond()

local function producer()
    for i = 1, 5 do
        fiber.sleep(1)
        print("Produced " .. i)
        cond:broadcast()
    end
end

local function consumer()
    while true do
        cond:wait()
        print("Consumed")
    end
end

fiber.create(producer)
fiber.create(consumer)
```

### Indexing & Performance

**Using Indexes in Queries**
```lua
-- Efficient index-based selection
local emails = box.space.users.index.email
local user = emails:get('john@example.com')

-- Range queries
local users = emails:select('john', {limit = 10})

-- All-index operations
local range = box.space.users.index.id:select({}, {
    limit = 100,
    offset = 0
})
```

**Composite Index Queries**
```lua
-- Create composite index
box.space.orders:create_index('user_date', {
    parts = {{'user_id'}, {'created_at'}}
})

-- Query with composite key
local orders = box.space.orders.index.user_date:select({1})
```

### Error Handling

**Try-Catch Pattern**
```lua
local function safe_operation(user_id)
    local status, result = pcall(function()
        return box.space.users:get(user_id)
    end)

    if not status then
        return nil, result  -- error
    end

    return result, nil
end
```

### Module Development

**Creating a Module**
```lua
-- users_module.lua
local module = {}

function module.get_user(user_id)
    return box.space.users:get(user_id)
end

function module.create_user(name, email)
    return box.space.users:insert({box.NULL, name, email})
end

function module.delete_user(user_id)
    return box.space.users:delete(user_id)
end

return module
```

**Using the Module**
```lua
local users = require('users_module')

local user = users.get_user(1)
users.create_user('Jane', 'jane@example.com')
```

## Best Practices

1. **Transactions**
   - Keep transactions short and simple
   - Minimize transaction scope
   - Avoid user interaction in transactions

2. **Stored Procedures**
   - Return meaningful results
   - Handle errors appropriately
   - Log important operations

3. **Triggers**
   - Keep trigger logic simple
   - Avoid recursion
   - Monitor trigger performance

4. **Code Organization**
   - Use modules for code reuse
   - Separate business logic from DB operations
   - Maintain clear naming conventions

5. **Performance**
   - Use indexes for filtering
   - Batch operations when possible
   - Profile with `fprofile` module

## Common Pitfalls

- **Long Transactions**: Block concurrent operations
- **Unindexed Queries**: Full table scans are slow
- **Complex Triggers**: Slow down write performance
- **Memory Leaks**: Unbounded data structures
- **Not Using Fibers**: Blocking in single-threaded code

## Related Skills

- `tarantool-architecture` - Database design and architecture
- `vshard-sharding` - Using Lua with sharded clusters
- `tarantool-performance` - Performance optimization
- `replication-ha` - Working with replicated clusters
