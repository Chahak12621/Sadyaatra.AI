# Schema Division: Web App vs. Mobile App (APK)

This document outlines how the database schema (defined in `schema.md`) is divided and utilized across the two primary platforms: the **SadYaatra Web App** (Landing Page & Agent Portal) and the **SadYaatra Mobile App (APK)** (Traveler Companion App).

---

## 1. `user_profiles` Table
**Ownership:** **Mobile App (APK)**

- **Purpose:** Stores the accounts for travelers who want to personalize their trips, generate AI itineraries, and book services.
- **Mobile App Usage:** Fully managed here. Users sign up, manage their profiles, save their trip history, and maintain personalization preferences.
- **Web App Usage:** *None*. The web app is strictly for general exploration and acts as a funnel to download the mobile app. Users do not log in to the web app.

---

## 2. `agent_profiles` Table
**Ownership:** **Web App** (Write) / **Mobile App** (Read)

- **Purpose:** Stores the verified profiles, vehicle details, and KYC documents for local drivers/agents.
- **Web App Usage:** Agents use the web portal to register, upload their documents (Aadhar, PAN, RC, etc.), and access their Agent Dashboard once approved. The web app handles all the `INSERT` and `UPDATE` operations for this table.
- **Mobile App Usage:** Read-only (`SELECT`). Travelers use the mobile app to browse approved agents, view their vehicle details, ratings, and profile photos before initiating a chat or booking.

---

## 3. `chat_messages` Table
**Ownership:** **Shared** (Web & Mobile)

- **Purpose:** Facilitates real-time communication between travelers and agents via Supabase Realtime WebSockets.
- **Mobile App Usage (Traveler):** Travelers open the mobile app, select an agent, and send a message. The mobile app `INSERT`s rows where `sender_role = 'user'`.
- **Web App Usage (Agent):** Agents monitor their Live Chat Inbox on their Web Dashboard. They receive real-time updates and reply to users. The web app `INSERT`s rows where `sender_role = 'agent'`.

---

## Summary of Data Flow
| Table | Web App Action | Mobile App (APK) Action |
|-------|---------------|-------------------------|
| **`user_profiles`** | None | Create, Read, Update |
| **`agent_profiles`**| Create, Read, Update (Agent Dashboard) | Read (Traveler Browsing) |
| **`chat_messages`** | Read, Write (Agent replies) | Read, Write (Traveler queries) |

> **Note:** The Web App's general AI Chatbot (the floating widget on the landing page) does **not** write to any database tables. It strictly communicates statelessly with the `explore-chat` API route.
