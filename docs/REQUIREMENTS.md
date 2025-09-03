Sigma Stories — Requirements (MVP)

Vision
- Help novices think “I get it” in under 60 seconds.
- Teach with plain-language stories, characters, and everyday analogies.
- Inform only — no recommendations, no hype, no promises.

Scope (MVP)
- Educational stories on core market concepts: Stock, Stock Exchange, Index, ETF, Diversification, Risks (How People Lose Money).
- Two lengths per topic: Short (~1 min) and Detailed (~3–5 min).
- Each story ends with 2–3 follow-ups to continue learning.

Audience & Tone
- Audience: Beginners with zero jargon tolerance.
- Tone: Warm, clear, reassuring; define any necessary term inline, briefly.
- Style: Narrative first (characters, scenes), then takeaways and risk notes.

Story Content (per story version)
- Title
- Story body (narrative; human voice)
- One‑liner summary
- Risks to know (plain, non‑alarming)
- Next steps (2–3 follow‑up links with level + time)
- Optional: simple analogy, micro‑explanations (e.g., dividends as “thank‑you payments”)

Metadata (front‑matter or DB fields)
- id: `<term>.<level>.<length>` (e.g., `stock.intro.short`, `stock.intro.detailed`)
- term: canonical name (e.g., Stock)
- level: Intro | Basics | Deeper
- length: Short | Detailed
- estimated_time: 1m | 3m | 5m
- next_ids: ordered array (2–3)
- related_ids: optional array (lateral topics)
- tags: friendly list (see Tags)
- created_at / updated_at

Friendly Tags (user‑facing)
- Always include:
  - `Term: <Name>` (e.g., Term: Stock)
  - `Category: <Bucket>` (e.g., Category: Stock; optionally Category: Trading)
- Add 3–4 helpers from: Beginner Friendly, In Plain English, Why It Matters, Quick Read / Detailed Read, Risk To Know, Keep Watching, 1‑Minute Read
- Examples:
  - Short: Term: Stock, Category: Stock, Category: Trading, Beginner Friendly, Quick Read, Why It Matters, In Plain English
  - Detailed: Term: Stock, Category: Stock, Category: Trading, Beginner Friendly, Detailed Read, Why It Matters, Risk To Know, In Plain English

Follow‑Ups (learning graph)
- Every story has 2–3 “Next Up” links and optional “Related”.
- Early path from Stock:
  - Next Up: What Is a Stock Exchange?; How People Lose Money; Diversification in Plain Words
  - Related: What Is an Index?; What Is an ETF?
- Rules: no dead ends; include at least one risk/pitfall item early; don’t jump levels (Intro → Basics → Deeper).

Content Governance
- Plain language only; define jargon in one short line if unavoidable.
- Include a non‑recommendation note and a simple risk note.
- Avoid sensational language, predictions, and deterministic claims.
- Each story must pass a “novice‑first” checklist before publishing.

Storage & Catalog
- Database: Postgres `sigma_stories`.
- Tables:
  - `story_topics(term text primary key, description text)`
  - `story_versions(id text primary key, term text, level text, length text, estimated_time text, title text, body_md text, one_liner text, risks_md text, tags text[], created_at timestamptz, updated_at timestamptz)`
  - `story_links(from_id text, to_id text, kind text check (kind in ('next','related','prereq')), ordinal int, primary key(from_id, to_id, kind))`
  - i18n‑ready: `story_translations(version_id, locale, title, body_md, one_liner, risks_md, tags[])`
  - Optional later: `story_videos(story_id, source, url_or_uri, duration_s, languages text[], captions_uri, license, status)`
- Authoring source of truth: Markdown files with YAML front‑matter under `products/sigma-stories/docs/stories/`; a loader validates and upserts to DB.

I18n Readiness (design only; no runtime yet)
- story_versions adds:
  - `localizable boolean default false`
  - `default_locale text`
  - `locales_available text[] default '{}'`
  - `required_vars jsonb default '[]'` (e.g., ["character_1","shop_owner","city","currency_symbol"])
- Tables:
  - `story_translations(version_id, locale, title, body_md, one_liner, risks_md, tags[])` with `unique(version_id, locale)`
  - `culture_packs(locale text primary key, data jsonb, updated_at)` for localized names/places/currency cues
- Rendering rules (future): select preferred locale if available else default; neutral fallbacks for missing vars; tags/IDs remain locale‑neutral.

Authoring Workflow
- Write Short + Detailed stories per topic in docs folder.
- Include metadata front‑matter (id, term, level, length, time, next_ids, related_ids, tags).
- Linter checks:
  - Required sections exist (title, body, one‑liner, risks, next steps)
  - Friendly tags include Term and Category; 4–7 total
  - 2–3 Next Up links present; levels consistent
  - Non‑recommendation note present
- Loader syncs stories to Postgres; docs build renders examples.

Play (Text‑to‑Speech)
- MVP: Browser Web Speech API (client‑side play/pause/stop; auto language from browser; speed control). No backend required.
- Upgrade: Server TTS endpoint using Azure/Polly/Google; render SSML (pauses by section), cache MP3 by checksum(lang, voice, text), return URL.
- Translation:
  - Tier 1: Curated translations for core stories.
  - Tier 2: Auto‑translate (DeepL/Google or open models) with “auto‑translated” note.
- Guardrails: show “educational, not advice”; no PII to providers; fallback to English.

Watch (Video)
- MVP: Curated YouTube links per story (≤ 4–6 minutes), shown as Watch button.
- Step 2: In‑house short explainers (slides + icons + TTS); generate captions (VTT/SRT); store URI.
- Step 3: Explore AI video (Sora/Runway/Luma) for scenes; strict review for accuracy and tone.
- Metadata (per story): `video: { source: youtube|inhouse|ai, url, duration_s, languages: [..], captions: true/false, license }`.
- Acceptance: captions present; “educational, not advice” slate; language‑aware fallback.

MVP Deliverables
- Stories (two‑length pairs): Stock, Stock Exchange, How People Lose Money, Diversification in Plain Words.
- Follow‑ups wired between the above.
- Docs: Personas (as TODO styles), Tags guide, Index, Requirements, example stories directory.
- Linter checklist (docs) and loader spec.
- DB DDL for story tables (initial migrations prepared).
- TTS: browser play in demo; Video: YouTube links for first topics.

Acceptance Criteria
- Each story includes the required sections and 2–3 Next Up links.
- Tags include Term and at least one Category; 4–7 total; friendly phrasing.
- Short story reads in ~1 minute; detailed in ~3–5 minutes.
- Zero jargon without a quick inline explanation.
- Non‑recommendation note present.

Success Metrics
- Short → Detailed completion rate on same term.
- Click‑through rate on Next Up.
- Quick “I get it” feedback rate (thumbs‑up or tooltip survey).
- Fewer confusion‑flagged topics over time (support/feedback).

Out of Scope (MVP)
- Trading signals, backtests, or market data rendering.
- Personalization or automation.
- Multi‑language localization beyond basic TTS/YouTube captions.
