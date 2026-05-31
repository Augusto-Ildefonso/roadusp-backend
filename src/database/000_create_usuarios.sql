-- Migration 000: Create usuarios table
-- Run this in the Supabase SQL Editor before migration 001

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE usuarios (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT NOT NULL UNIQUE,
  senha TEXT NOT NULL
);
