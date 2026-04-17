const express = require("express");
const axios = require("axios");

const app = express();
app.use(express.json());

const KNJIGE_SERVICE_URL = "http://localhost:8000";
const IZPOSOJA_SERVICE_URL = "http://localhost:8082";

// Health check
app.get("/", (req, res) => {
  res.json({ message: "Web gateway is running" });
});

// BOOKS - all
app.get("/web/books", async (req, res) => {
  try {
    const response = await axios.get(`${KNJIGE_SERVICE_URL}/books`);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch books" });
  }
});

// BOOKS - by id
app.get("/web/books/:id", async (req, res) => {
  try {
    const response = await axios.get(`${KNJIGE_SERVICE_URL}/books/${req.params.id}`);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch book" });
  }
});

// BORROWINGS - all
app.get("/web/borrowings", async (req, res) => {
  try {
    const response = await axios.get(`${IZPOSOJA_SERVICE_URL}/borrowings`);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch borrowings" });
  }
});

// BORROWINGS - create
app.post("/web/borrowings", async (req, res) => {
  try {
    const response = await axios.post(`${IZPOSOJA_SERVICE_URL}/borrowings`, req.body);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: "Failed to create borrowing" });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Web gateway is running on http://localhost:${PORT}`);
});
