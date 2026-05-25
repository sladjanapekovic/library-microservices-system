const express = require("express");
const axios = require("axios");

const fs = require("fs");
const path = require("path");

const app = express();
app.use(express.json());

const KNJIGE_SERVICE_URL = process.env.KNJIGE_SERVICE_URL || "http://localhost:8000";
const IZPOSOJA_SERVICE_URL = process.env.IZPOSOJA_SERVICE_URL || "http://localhost:8082";

function writeLog(message) {
  const logPath = path.join(__dirname, "../../logs/gateway.log");
  const logMessage = `${new Date().toISOString()} - ${message}\n`;

  fs.appendFileSync(logPath, logMessage);
}

// Health check
app.get("/", (req, res) => {
  writeLog("GET / called");
  res.json({ message: "Web gateway is running" });
});

// BOOKS - all
app.get("/web/books", async (req, res) => {
  writeLog("GET /web/books called");

  try {
    const response = await axios.get(`${KNJIGE_SERVICE_URL}/books`);
    writeLog("Successfully fetched books");
    res.json(response.data);
  } catch (error) {
    writeLog("Error while fetching books");
    res.status(500).json({ error: "Failed to fetch books" });
  }
});

// BOOKS - by id
app.get("/web/books/:id", async (req, res) => {
  writeLog(`GET /web/books/${req.params.id} called`);

  try {
    const response = await axios.get(`${KNJIGE_SERVICE_URL}/books/${req.params.id}`);
    writeLog(`Successfully fetched book with id=${req.params.id}`);
    res.json(response.data);
  } catch (error) {
    writeLog(`Error while fetching book with id=${req.params.id}`);
    res.status(500).json({ error: "Failed to fetch book" });
  }
});

// BORROWINGS - all
app.get("/web/borrowings", async (req, res) => {
  writeLog("GET /web/borrowings called");

  try {
    const response = await axios.get(`${IZPOSOJA_SERVICE_URL}/borrowings`);
    writeLog("Successfully fetched borrowings");
    res.json(response.data);
  } catch (error) {
    writeLog("Error while fetching borrowings");
    res.status(500).json({ error: "Failed to fetch borrowings" });
  }
});

// BORROWINGS - create
app.post("/web/borrowings", async (req, res) => {
  writeLog("POST /web/borrowings called");

  try {
    const response = await axios.post(`${IZPOSOJA_SERVICE_URL}/borrowings`, req.body);
    writeLog("Successfully created borrowing");
    res.json(response.data);
  } catch (error) {
    writeLog("Error while creating borrowing");
    res.status(500).json({ error: "Failed to create borrowing" });
  }
});

// USERS - all
app.get("/web/users", async (req, res) => {
  writeLog("GET /web/users called");

  res.json([
    {
      id: 1,
      name: "Ana",
      email: "ana@example.com"
    },
    {
      id: 2,
      name: "Marko",
      email: "marko@example.com"
    }
  ]);
});

// USERS - create
app.post("/web/users", async (req, res) => {
  writeLog("POST /web/users called");

  res.json({
    message: "User created",
    user: req.body
  });
});

const PORT = 3000;
app.listen(PORT, () => {
  writeLog(`Web gateway started on port ${PORT}`);
  console.log(`Web gateway is running on http://localhost:${PORT}`);
});
