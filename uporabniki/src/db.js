const { Pool } = require("pg");

const pool = new Pool({
  host: "uporabniki-postgres",
  port: 5432,
  user: "postgres",
  password: "postgres",
  database: "uporabniki_db",
});

async function initializeDatabase() {
  const query = `
    CREATE TABLE IF NOT EXISTS users (
      id SERIAL PRIMARY KEY,
      username VARCHAR(100) NOT NULL,
      email VARCHAR(150) NOT NULL
    );
  `;

  await pool.query(query);
  console.log("PostgreSQL database initialized.");
}

module.exports = {
  pool,
  initializeDatabase,
};
