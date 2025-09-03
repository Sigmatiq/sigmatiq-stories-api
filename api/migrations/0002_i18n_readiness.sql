-- Sigma Stories — Migration 0002: i18n readiness

-- Localizable fields on story_versions
ALTER TABLE ss.story_versions
  ADD COLUMN IF NOT EXISTS localizable BOOLEAN DEFAULT FALSE NOT NULL,
  ADD COLUMN IF NOT EXISTS default_locale TEXT,
  ADD COLUMN IF NOT EXISTS locales_available TEXT[] DEFAULT '{}'::TEXT[] NOT NULL,
  ADD COLUMN IF NOT EXISTS required_vars JSONB DEFAULT '[]'::JSONB NOT NULL;

-- Translations table (one row per locale for a story version)
CREATE TABLE IF NOT EXISTS ss.story_translations (
  version_id TEXT REFERENCES ss.story_versions(id) ON UPDATE CASCADE ON DELETE CASCADE,
  locale TEXT NOT NULL,
  title TEXT NOT NULL,
  body_md TEXT NOT NULL,
  one_liner TEXT NOT NULL,
  risks_md TEXT,
  tags TEXT[] DEFAULT '{}'::TEXT[] NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
  PRIMARY KEY (version_id, locale)
);

-- Culture packs for templating variables (names, city, currency, cues)
CREATE TABLE IF NOT EXISTS ss.culture_packs (
  locale TEXT PRIMARY KEY,
  data JSONB NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

