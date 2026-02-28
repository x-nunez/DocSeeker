CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE documentos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR(100) NOT NULL,
    path TEXT NOT NULL UNIQUE,
    extension VARCHAR(10) NOT NULL,
    modified_time TIMESTAMPTZ,
    creation_time TIMESTAMPTZ,
    resume TEXT,
    size BIGINT,
    link TEXT,
    source VARCHAR(50) DEFAULT 'local'
);