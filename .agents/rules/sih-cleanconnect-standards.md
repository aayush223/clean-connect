# Clean Connect Workspace Rules

## 1. Code Quality & Standards
* Build the API using FastAPI with full Type Hinting and asynchronous query executors.
* Organize code into separate, modular files: database logic in `db.py`, validation routines in `validators.py`, and endpoint definitions in specialized router packages.
* All code comments and documentation must be written in the third person. Avoid the use of first-person ("we", "I") or second-person ("you") language in code annotations.

## 2. API Security and SLA Mechanics
* Enforce strict authentication via JWTs containing role permissions (CITIZEN, WORKER, ADMIN).
* Verify EXIF headers on uploaded images to confirm geotagging validity.
* Restrict PWA manifest distribution routes based on authenticated scopes to isolate role features.
* Protect all external notification and API logging loops from 429 throttling errors by using randomized exponential backoff structures.
