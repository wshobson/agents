# database-migration — additional patterns and templates

## Zero-Downtime Migrations

### Blue-Green Deployment Strategy

```javascript
// Phase 1: Make changes backward compatible
module.exports = {
  up: async (queryInterface, Sequelize) => {
    // Add new column (both old and new code can work)
    await queryInterface.addColumn("users", "email_new", {
      type: Sequelize.STRING,
    });
  },
};

// Phase 2: Deploy code that writes to both columns

// Phase 3: Backfill data
module.exports = {
  up: async (queryInterface) => {
    await queryInterface.sequelize.query(`
      UPDATE users
      SET email_new = email
      WHERE email_new IS NULL
    `);
  },
};

// Phase 4: Deploy code that reads from new column

// Phase 5: Remove old column
module.exports = {
  up: async (queryInterface) => {
    await queryInterface.removeColumn("users", "email");
  },
};
```

## Cross-Database Migrations

### PostgreSQL to MySQL

```javascript
// Handle differences
module.exports = {
  up: async (queryInterface, Sequelize) => {
    const dialectName = queryInterface.sequelize.getDialect();

    if (dialectName === "mysql") {
      await queryInterface.createTable("users", {
        id: {
          type: Sequelize.INTEGER,
          primaryKey: true,
          autoIncrement: true,
        },
        data: {
          type: Sequelize.JSON, // MySQL JSON type
        },
      });
    } else if (dialectName === "postgres") {
      await queryInterface.createTable("users", {
        id: {
          type: Sequelize.INTEGER,
          primaryKey: true,
          autoIncrement: true,
        },
        data: {
          type: Sequelize.JSONB, // PostgreSQL JSONB type
        },
      });
    }
  },
};
```
