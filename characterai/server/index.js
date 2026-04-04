import express from "express";
import cors from "cors";
import mongoose from "mongoose";
import fetch from "node-fetch";
import "dotenv/config";

const app = express();
const PORT = process.env.PORT || 4000;
const FASTAPI_URL = process.env.FASTAPI_URL || "http://localhost:8000";
const CLIENT_URL = process.env.CLIENT_URL || "http://localhost:5173";
const MONGO_URI = process.env.MONGO_URI || "mongodb://localhost:27017/characterai";

app.use(cors({ origin: CLIENT_URL, credentials: true }));
app.use(express.json({ limit: "10mb" }));

mongoose
  .connect(MONGO_URI)
  .then(() => console.log("Connected to MongoDB"))
  .catch((err) => console.error("MongoDB connection error:", err));

const messageSchema = new mongoose.Schema({
  role: { type: String, enum: ["user", "assistant"] },
  content: String,
  timestamp: { type: Date, default: Date.now },
});

const sessionSchema = new mongoose.Schema(
  {
    sessionId: { type: String, required: true, unique: true },
    characterId: String,
    messages: [messageSchema],
  },
  { timestamps: true }
);

const Session = mongoose.model("Session", sessionSchema);

app.get("/api/health", (req, res) => {
  res.json({ status: "ok" });
});

app.get("/api/characters", async (req, res) => {
  try {
    const response = await fetch(`${FASTAPI_URL}/characters`);
    const data = await response.json();
    res.json(data);
  } catch (error) {
    console.error("Failed to fetch characters:", error);
    res.status(500).json({ error: "Failed to fetch characters" });
  }
});

app.post("/api/sessions", async (req, res) => {
  try {
    const { sessionId, characterId } = req.body;

    let session = await Session.findOne({ sessionId });

    if (!session) {
      session = new Session({
        sessionId,
        characterId,
        messages: [],
      });
      await session.save();
    }

    res.json({ sessionId: session.sessionId, characterId: session.characterId });
  } catch (error) {
    console.error("Failed to create session:", error);
    res.status(500).json({ error: "Failed to create session" });
  }
});

app.get("/api/sessions/:sessionId", async (req, res) => {
  try {
    const session = await Session.findOne({ sessionId: req.params.sessionId });

    if (!session) {
      return res.status(404).json({ error: "Session not found" });
    }

    res.json({
      sessionId: session.sessionId,
      characterId: session.characterId,
      messages: session.messages,
    });
  } catch (error) {
    console.error("Failed to fetch session:", error);
    res.status(500).json({ error: "Failed to fetch session" });
  }
});

app.get("/api/sessions/character/:characterId", async (req, res) => {
  try {
    const sessions = await Session.find({ characterId: req.params.characterId })
      .sort({ createdAt: -1 })
      .limit(20)
      .select("sessionId createdAt");

    res.json(sessions);
  } catch (error) {
    console.error("Failed to fetch sessions:", error);
    res.status(500).json({ error: "Failed to fetch sessions" });
  }
});

app.delete("/api/sessions/:sessionId", async (req, res) => {
  try {
    const result = await Session.deleteOne({ sessionId: req.params.sessionId });

    if (result.deletedCount === 0) {
      return res.status(404).json({ error: "Session not found" });
    }

    res.json({ success: true });
  } catch (error) {
    console.error("Failed to delete session:", error);
    res.status(500).json({ error: "Failed to delete session" });
  }
});

app.post("/api/chat/:characterId/stream", async (req, res) => {
  try {
    const { sessionId, message, history } = req.body;
    const { characterId } = req.params;

    let session = await Session.findOne({ sessionId });

    if (!session) {
      session = new Session({
        sessionId,
        characterId,
        messages: [],
      });
      await session.save();
    }

    session.messages.push({ role: "user", content: message });
    await session.save();

    res.setHeader("Content-Type", "text/event-stream");
    res.setHeader("Cache-Control", "no-cache");
    res.setHeader("Connection", "keep-alive");
    res.setHeader("X-Accel-Buffering", "no");

    res.flushHeaders();

    res.write(`data: ${JSON.stringify({ sessionId })}\n\n`);

    const backendResponse = await fetch(`${FASTAPI_URL}/chat/${characterId}/stream`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, history: history || [] }),
    });

    let fullResponse = "";

    for await (const chunk of backendResponse.body) {
      const text = chunk.toString();
      res.write(text);
      fullResponse += text;
    }

    const assistantContent = fullResponse
      .split("\n")
      .filter((line) => line.startsWith("data: ") && !line.includes("[DONE]"))
      .map((line) => {
        try {
          const data = JSON.parse(line.replace("data: ", ""));
          return data.token || "";
        } catch {
          return "";
        }
      })
      .join("");

    session.messages.push({ role: "assistant", content: assistantContent });
    await session.save();

    res.end();
  } catch (error) {
    console.error("Chat stream error:", error);
    if (!res.headersSent) {
      res.status(500).json({ error: "Chat failed" });
    } else {
      res.end();
    }
  }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
