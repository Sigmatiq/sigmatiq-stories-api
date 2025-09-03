# Sigma Stories (Product)

Standalone API for narrative composition and lightweight visuals.

Run
- Dev API: `uvicorn products.sigma-stories.api.app:app --reload --port 8090`
- Static: story artifacts are served at `/stories/{story_id}/...` (JSON/Markdown/images).

Endpoints
- POST `/assistant/stories/compose` — compose a story with `{ context, persona?, data, options? }`.
- POST `/assistant/stories/compose_async` — start an async story job; WS at `/ws/stories/{job_id}`.

Visuals dependency
- Visuals are best‑effort. If you want charts locally, install `matplotlib` (e.g., `pip install matplotlib`).
- Without it, compose returns JSON/Markdown outputs; visuals may be empty.

Postman
- See `products/sigma-stories/postman/Stories.postman_collection.json` for sync + async requests.
