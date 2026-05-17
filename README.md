# Clean Connect ♻️

**Clean Connect** is an integrated, role-based cyber-physical platform designed to optimize municipal waste management. Originally conceptualized for the Smart India Hackathon, it seamlessly connects Citizens, Sanitation Workers, and Administrators into a unified, responsive ecosystem with strict SLA deadlines.

## 🌟 Key Features & Architectures

- **Role-based PWA Framework**: Unified platform that offers distinct Progressive Web App interfaces for Citizens, Workers, and Admins.
- **Strict SLA Enforcement**: A rigid 36-hour resolution window for citizen complaints, automatically managed and monitored.
- **Geospatial Intelligence**: Verification of GPS EXIF data from uploaded complaint images, displayed instantly on Leaflet-powered maps.
- **Offline-First PWA & Real-time Notifications**: Utilizes Firebase Cloud Messaging (FCM) Service Workers for offline capabilities and prompt job assignments.
- **Telemetry & AI Auditing**: Deep integration with the Antigravity Nexus API for asynchronous telemetry audits and AI-driven system health checks.

## 🧠 Core Logics

- **Location Parsing & Verification**: Extracting and validating EXIF metadata directly from base64 encoded photo uploads to verify the authenticity of a complaint's location.
- **SLA Management (`SLAManager`)**: Time-series monitoring that enforces the 36-hour resolution timeline and tags complaints as compliant or non-compliant.
- **Resilient AI Telemetry Client**: A custom API client (`AntigravityAPIClient`) for telemetry streaming that implements token normalization, streaming Server-Sent Events (SSE) parsing, and robust error handling.

## 🧮 Mathematical Implementations

- **Geospatial Boundaries**: Enforcing strict mathematical constraints on GPS coordinates via Pydantic (`latitude: float = Field(..., ge=-90.0, le=90.0)`, `longitude: float = Field(..., ge=-180.0, le=180.0)`).
- **Time Delta Arithmetic**: Calculating SLA deadlines dynamically (`deadline = now + timedelta(hours=36)`).
- **Exponential Backoff with Jitter**: Network retry logic for HTTP 429 Too Many Requests, calculating sleep time as `backoff + random.uniform(0.1, 0.5)` and multiplying `backoff *= 2.0`.

## 🔑 API Keys & Configurations

- **Antigravity API Credentials**: Requires an OAuth credential/token file at `~/.config/opencode/antigravity-accounts.json`. It securely extracts the `access_token` to interact with Claude/Gemini telemetry endpoints.
- **Firebase Configuration**: Relies on FCM integration (`firebase-messaging-sw.js` & Firebase SDK) to enable push notifications and offline caching.

## 🛠️ Modules & Libraries

**Backend (Python/FastAPI):**
- `fastapi` - High performance async API framework
- `pydantic` (V2) - Data validation and settings management using python type annotations
- `urllib` - Native HTTP request handling for the Antigravity Client
- `datetime`, `time`, `random`, `json` - Standard Python libraries for timing, math, and parsing
- Mock Database State utilizing Python `Dict` and `List` objects for rapid prototyping without overhead.

**Frontend:**
- `Vanilla JS`, `HTML5`, `CSS3` - Featuring modern Glassmorphism aesthetics
- `Leaflet.js` - Open-source JavaScript library for mobile-friendly interactive maps
- `Firebase SDK (Compat 10.4.0)` - For PWA service worker and messaging capabilities

## 🚀 Running Locally

1. Setup a Python virtual environment (`python -m venv .venv`).
2. Activate the environment.
3. Install dependencies (`pip install fastapi uvicorn pydantic`).
4. Run the API: `uvicorn backend.main:app --reload`.
5. Serve the `frontend/` directory using any local web server (e.g., Live Server or `python -m http.server`).
