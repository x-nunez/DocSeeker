-- SPDX-License-Identifier: Apache-2.0

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE documentos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR(100) NOT NULL,
    path TEXT NOT NULL UNIQUE,
    extension VARCHAR(10) NOT NULL,
    modified_time TIMESTAMPTZ,
    creation_time TIMESTAMPTZ,
    uploaded_at TIMESTAMPTZ DEFAULT NOW(),
    size BIGINT,
    link TEXT,
    source VARCHAR(50) DEFAULT 'local'
);