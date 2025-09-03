-- Sigma Stories — Migration 0001: initial schema
CREATE SCHEMA IF NOT EXISTS ss;

-- Topics: canonical terms (Stock, Stock Exchange, Diversification, etc.)
CREATE TABLE IF NOT EXISTS ss.story_topics (
  term TEXT PRIMARY KEY,
  description TEXT
);

-- Versions: concrete story versions (short/detailed, intro/basics/deeper)
CREATE TABLE IF NOT EXISTS ss.story_versions (
  id TEXT PRIMARY KEY,
  term TEXT REFERENCES ss.story_topics(term) ON UPDATE CASCADE ON DELETE RESTRICT,
  level TEXT CHECK (level IN ('Intro','Basics','Deeper')) NOT NULL,
  length TEXT CHECK (length IN ('Short','Detailed')) NOT NULL,
  estimated_time TEXT,
  title TEXT NOT NULL,
  body_md TEXT NOT NULL,
  one_liner TEXT NOT NULL,
  risks_md TEXT,
  tags TEXT[] DEFAULT '{}'::TEXT[] NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- Links: next/related/prereq between story versions
CREATE TABLE IF NOT EXISTS ss.story_links (
  from_id TEXT REFERENCES ss.story_versions(id) ON UPDATE CASCADE ON DELETE CASCADE,
  to_id   TEXT REFERENCES ss.story_versions(id) ON UPDATE CASCADE ON DELETE CASCADE,
  kind    TEXT CHECK (kind IN ('next','related','prereq')) NOT NULL,
  ordinal INT,
  PRIMARY KEY (from_id, to_id, kind)
);

-- Indexes
CREATE INDEX IF NOT EXISTS story_versions_tags_gin ON ss.story_versions USING GIN (tags);

