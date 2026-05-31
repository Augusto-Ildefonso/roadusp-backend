-- Migration 001: Create historico_disciplinas table
-- Run this in the Supabase SQL Editor

CREATE TABLE historico_disciplinas (
  id SERIAL PRIMARY KEY,
  id_usuario UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
  codigo_disciplina TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('aprovada', 'cursando')),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_historico_id_usuario ON historico_disciplinas(id_usuario);
