-- Migration 002: Create processamentos_historico table
-- Run this in the Supabase SQL Editor

CREATE TABLE processamentos_historico (
  id UUID PRIMARY KEY,
  id_usuario UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
  status TEXT NOT NULL CHECK (status IN ('processando', 'concluido', 'erro')),
  resultado JSONB,
  erro TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_processamento_id_usuario ON processamentos_historico(id_usuario);
