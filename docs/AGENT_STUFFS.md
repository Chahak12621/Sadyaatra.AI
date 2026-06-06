# Deep Dive: Advanced AI Agent Architecture

This document answers the deep technical questions regarding how the Multi-Agent system will operate, what technologies are required, and how the LLMs will be utilized.

---

## 1. Agent Orchestration & Shared Knowledge Base

### The Shared Knowledge Base (RAG)
We **do not** need separate RAG models for the Web App and the Mobile App. 
*   We will have exactly **ONE centralized Vector Database** (Supabase `pgvector`).
*   Both the Web backend and the APK backend will hit the exact same FastAPI endpoints, which in turn query this single source of truth.
*   This ensures that a recommendation made on the web exactly matches a recommendation made on mobile.

### What Agents Run in Parallel?
When a user sends a complex request (e.g., "Plan a trip for my group of 4"), we will use an orchestration framework like **LangGraph** to route the work. For a single request, the following "Sub-Agents" execute:

1.  **The Router Agent (Sequential):** Reads the user prompt and decides what needs to be done.
2.  **The Profile Analysis Agents (Parallel):** If this is a group trip of 4 people, the system will spin up 4 parallel agents. Each agent reads one user's profile and extracts their strict requirements.
3.  **The RAG Retrieval Agent (Parallel):** Simultaneously, an agent queries the vector database for destination facts, hotel prices, and location data.
4.  **The Consensus & Planner Agent (Sequential):** Waits for the Profile Agents and the RAG Agent to finish, merges all the data, resolves conflicts, and outputs the final JSON itinerary.

## 2. Technical Stack & Database Setup

To make this work seamlessly, the Python backend requires a specific stack:

*   **Relational Database:** Supabase PostgreSQL. This stores standard user data, saved trips, and group polls.
*   **Vector Database (Knowledge Base):** Supabase `pgvector`. This stores the text embeddings of travel guides, hotel descriptions, and Wikipedia summaries of locations.
*   **Backend Framework:** FastAPI (Python) for handling asynchronous requests from the Next.js and Expo apps.
*   **Orchestration Framework:** LangChain / LangGraph. This handles the logic of making the agents talk to each other and run in parallel.
*   **Embedding Model:** HuggingFace `all-MiniLM-L6-v2` (Free, runs locally in Python) or OpenAI `text-embedding-3-small`. This converts text documents into numbers (vectors) for the RAG database.

## 3. Do We Need to Train Our Own Model?

**Short Answer:** No, absolutely not.

**Long Answer:** Training an LLM from scratch (or even Fine-Tuning one) is incredibly expensive, time-consuming, and immediately becomes outdated when new places open or close. 
Instead, we use the **RAG (Retrieval-Augmented Generation)** approach. 
*   We use a pre-trained, state-of-the-art open-weights model like **Llama-3-70b**.
*   We treat the LLM as the "Brain" and our Supabase `pgvector` database as the "Memory".
*   When a user asks about Kerala, the backend searches Supabase for facts about Kerala, injects those facts into the prompt, and tells Llama-3 to read the facts and generate an itinerary. This guarantees accurate, up-to-date data without training any models.

## 4. API Usage & Parallel Execution Limits

We will use an external API key (specifically **Groq** for extreme speed, or OpenAI). 

**How many agents run in parallel?**
*   **Per Request:** As mentioned, a complex group request might spawn 3-5 background agents simultaneously (e.g., 4 Profile Agents + 1 RAG Agent).
*   **System-Wide:** FastAPI is entirely asynchronous. If 100 users open the mobile app and ask for an itinerary at the exact same second, the FastAPI server will spin up 100 parallel processing threads.
*   **The Bottleneck:** The only limitation is the **Rate Limit** of our LLM Provider (Groq/OpenAI). API providers limit how many "Tokens per Minute" (TPM) or "Requests per Minute" (RPM) you can send. If we have thousands of users, we simply upgrade to a higher API tier. The Python architecture itself can handle virtually infinite parallel agents.

## 5. API Call Strategy: Do We Need MCP?

**Short Answer:** No, we do not need to build an MCP (Model Context Protocol) server. We will make **different API calls** for each agent using the same underlying model.

### How it Works Under the Hood
1. **No MCP Needed:** MCP is mainly used to connect desktop AI assistants (like Claude) to local tools. Since we are building a production web backend (FastAPI), we don't use MCP. We make standard REST API calls to our LLM provider (Groq).
2. **Different Calls, Same Model:** We do not need to train or host 5 different models for the 5 different agents. We use the exact same underlying model (e.g., `llama3-70b`) for every agent, but we make **separate API calls** using different "System Prompts" (personas).

### Example of an Orchestrated Chain
If a user clicks "Plan Group Trip", the LangGraph backend chains together multiple small, focused API calls rather than one giant confusing one:
*   **Call 1 (Router Agent):** System Prompt: *"You are a router. Analyze this request and tell me what to do next."* Groq replies: *"Analyze group profiles."*
*   **Call 2 (Profile Agent):** Fetches User A's profile from Supabase. System Prompt: *"You are a profile analyst. What does User A like?"*
*   **Call 3 (Planner Agent):** Takes the output from Call 2, grabs facts from the RAG database, and makes a *final* API call. System Prompt: *"You are an expert trip planner. Given these profiles and RAG facts, generate a JSON itinerary."*

---

## 6. Technical Directory Structure

```text
ai_backend/
├── main.py                 # FastAPI server and route definitions
├── models/
│   └── schemas.py          # Pydantic DATA models (JSON structures)
├── core/
│   ├── rag_engine.py       # Handles Supabase pgvector embeddings
│   ├── groq_client.py      # Connects to the LLM API
├── agents/
│   ├── recommender.py      # Logic for Recommendation System
│   ├── planner.py          # Logic for Chat and Trip Planning
│   ├── budget_tracker.py   # Logic for maximizing budget constraints
│   └── group_analyzer.py   # Logic for parsing group polls and shared interests
```
