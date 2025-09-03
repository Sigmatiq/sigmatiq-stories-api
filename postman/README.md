Sigma Stories — Postman

Usage
- Base URL: set `{{baseUrl}}` to your Stories API (e.g., http://localhost:8090).
- Collections:
  - Stories.postman_collection.json: compose (sync) and compose_async (job).

Async WS
- Open a WebSocket tab in Postman to: `ws://localhost:8090/ws/stories/{{story_job_id}}` after running "Compose (async job)".
- Events: `{ type: 'progress'|'complete', ... }`.

Artifacts
- Story artifacts (JSON/Markdown/images) are served from `/stories/{story_id}/...` on the Stories API.
