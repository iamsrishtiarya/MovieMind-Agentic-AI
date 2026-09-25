# 🎬 MovieMind — An Agentic AI Movie Decision Assistant

MovieMind is an **Agentic AI movie assistant** built using **Python, LangChain, Groq LLM, OMDb API, and Streamlit**.

The application allows users to interact with an AI movie assistant using natural language. Instead of simply generating responses, the AI agent can understand the user's request, select the appropriate tool, execute it, process the result, and generate a final response.

---

## 🚀 Project Overview

MovieMind was built to explore how **Large Language Models (LLMs), tool calling, APIs, and AI agents** can work together to create an interactive AI application.

The agent can perform different movie-related tasks based on the user's query, such as:

- 🔎 Search for movies
- ⭐ Retrieve movie ratings
- ⏱️ Retrieve movie runtime
- 🎭 Recommend movies based on genre
- 💬 Answer movie-related questions through a conversational interface

---

## 🧠 How It Works

The application follows an agentic workflow:

```text
                User Query
                    │
                    ▼
           Streamlit Interface
                    │
                    ▼
             LangChain Agent
                    │
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
    Movie Search Tool    Rating/Runtime Tool
          │                   │
          └─────────┬─────────┘
                    ▼
                OMDb API
                    │
                    ▼
               Tool Result
                    │
                    ▼
             LangChain Agent
                    │
                    ▼
              Final Response
