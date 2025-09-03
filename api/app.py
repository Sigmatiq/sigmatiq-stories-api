from __future__ import annotations

from typing import Any, Dict, Optional, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from pathlib import Path
import json
import uuid
import asyncio

app = FastAPI(title="Sigma Stories API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _stories_dir() -> Path:
    base = Path(__file__).resolve().parents[1] / 'data_dumps' / 'stories'
    base.mkdir(parents=True, exist_ok=True)
    return base


try:
    app.mount('/stories', StaticFiles(directory=str(_stories_dir())), name='stories')
except Exception:
    pass


def _compose_local(payload: Dict[str, Any]) -> Dict[str, Any]:
    context = (payload.get('context') or 'screener').lower()
    persona = (payload.get('persona') or 'novice').lower()
    data = payload.get('data') or {}
    options = payload.get('options') or {}
    visuals_enabled = bool(options.get('visuals'))
    max_symbols = int(options.get('max_symbols') or 5)
    core_res = data.get('core_result') or data.get('result') or {}
    matched = []
    try:
        if isinstance(core_res, dict):
            if isinstance(core_res.get('matched'), list):
                matched = list(core_res.get('matched'))
            elif isinstance(core_res.get('sample'), list):
                matched = list(core_res.get('sample'))
    except Exception:
        matched = []
    story_id = str(uuid.uuid4())
    sections: List[Dict[str, Any]] = []
    wh = [f"Found {min(len(matched), max_symbols)} preview matches." if matched else "Preview data loaded."]
    wim = [
        "Previews use caps and run fast; full runs are async.",
        "Signals need context (trend, volume) and risk framing.",
    ]
    risks = [
        "This is educational; not financial advice.",
        "Small previews can miss items; confirm with full runs.",
    ]
    sections.append({'title': 'What Happened', 'body': wh})
    sections.append({'title': 'Why It Matters', 'body': wim})
    sections.append({'title': 'Risks & Watch-outs', 'body': risks})
    evidence = []
    if matched:
        evidence.append({'metric': 'matched_count', 'value': len(matched)})
    confidence = 0.5 if matched else 0.3
    visuals: List[Dict[str, Any]] = []
    if visuals_enabled and matched:
        try:
            import matplotlib.pyplot as plt  # type: ignore
            outdir = _stories_dir() / story_id
            outdir.mkdir(parents=True, exist_ok=True)
            fig, ax = plt.subplots(figsize=(4, 2.2))
            m = matched[:max_symbols]
            ax.bar(range(len(m)), [1] * len(m), color="#4C78A8")
            ax.set_xticks(range(len(m)))
            ax.set_xticklabels(m, rotation=45, ha='right', fontsize=8)
            ax.set_yticks([])
            ax.set_title('Top matches (preview)', fontsize=10)
            out_path = outdir / 'matches.png'
            fig.tight_layout()
            fig.savefig(out_path)
            plt.close(fig)
            visuals.append({'kind': 'image', 'url': f"/stories/{story_id}/matches.png", 'desc': 'Top preview matches'})
        except Exception:
            pass
    out = {
        'ok': True,
        'meta': { 'provider': 'sigma-stories', 'version': 'v1', 'story_id': story_id, 'confidence': confidence, 'evidence': evidence },
        'title': 'Novice Story — Preview',
        'tldr': 'Quick, safe summary with next steps. Not advice.',
        'sections': sections,
        'visuals': visuals,
        'next_actions': [
            { 'label': 'Run Full (Async)', 'action': 'run_full' },
            { 'label': 'Export Results', 'action': 'export' }
        ],
    }
    try:
        outdir = _stories_dir() / story_id
        outdir.mkdir(parents=True, exist_ok=True)
        (outdir / 'story.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
        md = [f"# {out['title']}", f"\n> {out['tldr']}\n"]
        for s in out['sections']:
            md.append(f"\n## {s.get('title')}")
            for b in (s.get('body') or []):
                md.append(f"- {b}")
        (outdir / 'story.md').write_text("\n".join(md), encoding='utf-8')
    except Exception:
        pass
    return out


@app.post('/assistant/stories/compose')
def stories_compose(payload: Dict[str, Any]):
    return _compose_local(payload)


_JOBS: Dict[str, Dict[str, Any]] = {}


@app.post('/assistant/stories/compose_async')
async def stories_compose_async(payload: Dict[str, Any]):
    job_id = str(uuid.uuid4())
    _JOBS[job_id] = { 'status': 'queued', 'progress': 0, 'result': None }
    async def _work():
        _JOBS[job_id].update(status='running', progress=5)
        await asyncio.sleep(0.1)
        _JOBS[job_id]['progress'] = 25
        await asyncio.sleep(0.1)
        res = _compose_local(payload)
        _JOBS[job_id].update(status='completed', progress=100, result=res)
    asyncio.create_task(_work())
    return { 'ok': True, 'job_id': job_id, 'status': 'queued', 'meta': { 'ws': [ f"/ws/stories/{job_id}" ] } }


@app.websocket('/ws/stories/{job_id}')
async def ws_stories(ws: WebSocket, job_id: str):
    await ws.accept()
    last_status = None
    try:
        while True:
            st = _JOBS.get(job_id)
            if not st:
                await ws.send_json({ 'type': 'error', 'message': 'job not found' })
                break
            if st.get('status') != last_status:
                await ws.send_json({ 'type': 'progress', 'progress': st.get('progress'), 'status': st.get('status') })
                last_status = st.get('status')
            if st.get('status') == 'completed':
                await ws.send_json({ 'type': 'complete', 'result': st.get('result') })
                break
            await asyncio.sleep(0.25)
    except WebSocketDisconnect:
        return


@app.get('/healthz')
def healthz():
    return { 'ok': True }

