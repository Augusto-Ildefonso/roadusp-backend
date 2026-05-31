-- Migration 003: Create preferencias_usuario table
-- Run this in the Supabase SQL Editor

CREATE TABLE preferencias_usuario (
  id_usuario UUID PRIMARY KEY REFERENCES usuarios(id) ON DELETE CASCADE,
  unidade TEXT,
  curso TEXT,
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_preferencias_id_usuario ON preferencias_usuario(id_usuario);
