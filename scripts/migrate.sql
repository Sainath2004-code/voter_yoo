-- ============================================================
-- National Voter Management System — Canonical DB Migration
-- Idempotent: safe to run multiple times (CREATE IF NOT EXISTS)
-- Target: Supabase PostgreSQL (pgvector + PostGIS enabled)
-- ============================================================

-- Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";         -- fast LIKE/ILIKE searches
-- CREATE EXTENSION IF NOT EXISTS "postgis";      -- only if PostGIS add-on is enabled

-- ============================================================
-- 1. GEOGRAPHIC HIERARCHY
-- ============================================================

CREATE TABLE IF NOT EXISTS states (
    id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name          TEXT UNIQUE NOT NULL,
    code          TEXT UNIQUE NOT NULL,               -- e.g. 'IN-DL'
    type          TEXT DEFAULT 'State',               -- 'State' | 'UT'
    created_at    TIMESTAMPTZ DEFAULT NOW(),
    updated_at    TIMESTAMPTZ DEFAULT NOW(),
    deleted_at    TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS districts (
    id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    state_id      UUID NOT NULL REFERENCES states(id) ON DELETE CASCADE,
    name          TEXT NOT NULL,
    code          TEXT NOT NULL,
    created_at    TIMESTAMPTZ DEFAULT NOW(),
    deleted_at    TIMESTAMPTZ,
    UNIQUE (state_id, code)
);

CREATE TABLE IF NOT EXISTS parliamentary_constituencies (
    id                   UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    district_id          UUID NOT NULL REFERENCES districts(id) ON DELETE CASCADE,
    name                 TEXT NOT NULL,
    code                 TEXT UNIQUE NOT NULL,
    is_reserved          BOOLEAN DEFAULT FALSE,
    reservation_category TEXT,                        -- 'SC' | 'ST' | 'General'
    delimitation_version TEXT DEFAULT '2008',
    created_at           TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS assembly_constituencies (
    id                   UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pc_id                UUID NOT NULL REFERENCES parliamentary_constituencies(id) ON DELETE CASCADE,
    name                 TEXT NOT NULL,
    code                 TEXT UNIQUE NOT NULL,
    is_reserved          BOOLEAN DEFAULT FALSE,
    reservation_category TEXT,
    created_at           TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS polling_booths (
    id           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ac_id        UUID NOT NULL REFERENCES assembly_constituencies(id) ON DELETE CASCADE,
    booth_no     INTEGER NOT NULL,
    name         TEXT NOT NULL,
    address      TEXT,
    capacity     INTEGER DEFAULT 1500,
    voter_count  INTEGER DEFAULT 0,
    latitude     DOUBLE PRECISION,
    longitude    DOUBLE PRECISION,
    created_at   TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (ac_id, booth_no)
);

-- ============================================================
-- 2. AUTH & IDENTITY
-- ============================================================

CREATE TABLE IF NOT EXISTS users (
    id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email                 TEXT UNIQUE NOT NULL,
    hashed_password       TEXT NOT NULL,
    full_name             TEXT,
    phone                 TEXT,
    role                  TEXT NOT NULL DEFAULT 'voter',
    scope_type            TEXT,        -- 'national' | 'state' | 'district' | 'pc' | 'ac' | 'booth'
    scope_id              UUID,        -- FK to the appropriate geography table
    is_active             BOOLEAN DEFAULT TRUE,
    is_verified           BOOLEAN DEFAULT FALSE,
    has_face_enrolled     BOOLEAN DEFAULT FALSE,
    has_fingerprint_enrolled BOOLEAN DEFAULT FALSE,
    mfa_enabled           BOOLEAN DEFAULT FALSE,
    totp_secret           TEXT,
    refresh_token         TEXT,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until          TIMESTAMPTZ,
    last_login            TIMESTAMPTZ,
    last_login_ip         TEXT,
    created_at            TIMESTAMPTZ DEFAULT NOW(),
    updated_at            TIMESTAMPTZ DEFAULT NOW(),
    deleted_at            TIMESTAMPTZ
);

-- ============================================================
-- 3. VOTER PROFILES
-- ============================================================

CREATE TABLE IF NOT EXISTS voter_profiles (
    id               UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id          UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    epic_number      TEXT UNIQUE,
    first_name       TEXT NOT NULL,
    last_name        TEXT NOT NULL,
    father_name      TEXT,
    spouse_name      TEXT,
    date_of_birth    DATE NOT NULL,
    gender           TEXT NOT NULL CHECK (gender IN ('male', 'female', 'third_gender')),
    address_line1    TEXT NOT NULL,
    address_line2    TEXT,
    pincode          TEXT NOT NULL,
    state_id         UUID REFERENCES states(id),
    district_id      UUID REFERENCES districts(id),
    pc_id            UUID REFERENCES parliamentary_constituencies(id),
    ac_id            UUID REFERENCES assembly_constituencies(id),
    polling_booth_id UUID REFERENCES polling_booths(id),
    aadhaar_hash     TEXT UNIQUE,       -- SHA-256 for dedup
    aadhaar_last4    TEXT,
    encrypted_aadhaar TEXT,             -- Fernet-encrypted
    verification_status TEXT DEFAULT 'pending',
    is_verified      BOOLEAN DEFAULT FALSE,
    created_at       TIMESTAMPTZ DEFAULT NOW(),
    updated_at       TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- 4. VOTER APPLICATIONS (Form 6 / 7 / 8)
-- ============================================================

CREATE TABLE IF NOT EXISTS voter_applications (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID NOT NULL REFERENCES users(id),
    type            TEXT NOT NULL CHECK (type IN ('form_6', 'form_7', 'form_8')),
    status          TEXT NOT NULL DEFAULT 'submitted',
    state_id        UUID REFERENCES states(id),
    district_id     UUID REFERENCES districts(id),
    ac_id           UUID REFERENCES assembly_constituencies(id),
    booth_id        UUID REFERENCES polling_booths(id),
    form_data       JSONB,
    current_task_id UUID,               -- FK added after verification_tasks
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- 5. WORKFLOW ENGINE
-- ============================================================

CREATE TABLE IF NOT EXISTS verification_tasks (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    type                TEXT NOT NULL,
    priority            TEXT DEFAULT 'medium',
    entity_id           UUID NOT NULL,
    entity_type         TEXT NOT NULL,
    assigned_officer_id UUID REFERENCES users(id),
    scope_type          TEXT,
    scope_id            UUID,
    status              TEXT DEFAULT 'pending',
    due_date            TIMESTAMPTZ,
    comments            TEXT,
    verification_payload JSONB,
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    updated_at          TIMESTAMPTZ DEFAULT NOW()
);

-- NOTE: current_task_id FK is applied via alter_existing.sql after column is added.

CREATE TABLE IF NOT EXISTS approval_history (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_id       UUID NOT NULL,
    entity_type     TEXT NOT NULL,
    action          TEXT NOT NULL,
    previous_status TEXT,
    new_status      TEXT,
    officer_id      UUID NOT NULL REFERENCES users(id),
    comments        TEXT,
    ip_address      TEXT,
    user_agent      TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS workflow_transitions (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_name   TEXT NOT NULL,
    from_status     TEXT NOT NULL,
    to_status       TEXT NOT NULL,
    required_role   TEXT,
    is_active       BOOLEAN DEFAULT TRUE,
    UNIQUE (workflow_name, from_status, to_status)
);

-- Seed canonical transitions
INSERT INTO workflow_transitions (workflow_name, from_status, to_status, required_role) VALUES
  ('voter_registration', 'submitted',        'blo_verification',  'booth_level_officer'),
  ('voter_registration', 'blo_verification', 'ero_review',        'electoral_registration_officer'),
  ('voter_registration', 'ero_review',       'approved',          'electoral_registration_officer'),
  ('voter_registration', 'ero_review',       'rejected',          'electoral_registration_officer'),
  ('voter_registration', 'approved',         'epic_generated',    'system'),
  ('election_lifecycle', 'notification',     'nomination',        'chief_election_commissioner'),
  ('election_lifecycle', 'nomination',       'scrutiny',          'chief_election_commissioner'),
  ('election_lifecycle', 'scrutiny',         'withdrawal',        'chief_election_commissioner'),
  ('election_lifecycle', 'withdrawal',       'campaign',          'chief_election_commissioner'),
  ('election_lifecycle', 'campaign',         'polling',           'chief_election_commissioner'),
  ('election_lifecycle', 'polling',          'counting',          'chief_election_commissioner'),
  ('election_lifecycle', 'counting',         'results',           'chief_election_commissioner'),
  ('election_lifecycle', 'results',          'archived',          'chief_election_commissioner')
ON CONFLICT DO NOTHING;

-- ============================================================
-- 6. ELECTIONS & CANDIDATES
-- ============================================================

CREATE TABLE IF NOT EXISTS political_parties (
    id           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name         TEXT UNIQUE NOT NULL,
    abbreviation TEXT UNIQUE NOT NULL,
    symbol_url   TEXT,
    is_national  BOOLEAN DEFAULT FALSE,
    created_at   TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS elections (
    id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title             TEXT NOT NULL,
    type              TEXT NOT NULL,      -- 'lok_sabha' | 'vidhan_sabha' | 'by_election'
    status            TEXT DEFAULT 'notification',
    notification_date DATE,
    polling_date      DATE,
    results_date      DATE,
    created_at        TIMESTAMPTZ DEFAULT NOW(),
    updated_at        TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS candidates (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    election_id         UUID NOT NULL REFERENCES elections(id),
    party_id            UUID REFERENCES political_parties(id),
    constituency_id     UUID NOT NULL,
    constituency_type   TEXT NOT NULL,
    voter_profile_id    UUID REFERENCES voter_profiles(id),
    affidavit_url       TEXT,
    status              TEXT DEFAULT 'pending',
    created_at          TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- 7. GRIEVANCE REDRESSAL
-- ============================================================

CREATE TABLE IF NOT EXISTS grievances (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id             UUID NOT NULL REFERENCES users(id),
    category            TEXT NOT NULL,
    status              TEXT DEFAULT 'submitted',
    subject             TEXT NOT NULL,
    description         TEXT NOT NULL,
    state_id            UUID REFERENCES states(id),
    district_id         UUID REFERENCES districts(id),
    ac_id               UUID REFERENCES assembly_constituencies(id),
    assigned_officer_id UUID REFERENCES users(id),
    priority            TEXT DEFAULT 'medium',
    sla_deadline        TIMESTAMPTZ,
    resolution_notes    TEXT,
    attachment_urls     JSONB DEFAULT '[]',
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    updated_at          TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- 8. BIOMETRIC VAULT
-- ============================================================

CREATE TABLE IF NOT EXISTS biometric_templates (
    id                        UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id                   UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    face_embedding_encrypted  BYTEA,
    fingerprint_template_encrypted BYTEA,
    algorithm_version         TEXT NOT NULL,
    embedding_dimension       INTEGER DEFAULT 128,
    encryption_metadata       JSONB,
    confidence_score          DOUBLE PRECISION,
    liveness_status           TEXT DEFAULT 'verified',
    liveness_metadata         JSONB,
    last_verified_at          TIMESTAMPTZ,
    verification_count        INTEGER DEFAULT 0,
    is_revoked                BOOLEAN DEFAULT FALSE,
    revocation_reason         TEXT,
    created_at                TIMESTAMPTZ DEFAULT NOW(),
    updated_at                TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- 9. AUDIT LOGS
-- ============================================================

CREATE TABLE IF NOT EXISTS audit_logs (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    actor_id        TEXT NOT NULL,         -- TEXT (not FK) to allow system actors
    actor_role      TEXT,
    action          TEXT NOT NULL,
    resource        TEXT NOT NULL,
    resource_id     TEXT,
    before_state    JSONB,
    after_state     JSONB,
    correlation_id  TEXT,
    ip_address      TEXT,
    user_agent      TEXT,
    scope_type      TEXT,
    scope_id        TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- In-app notifications table (for Supabase Realtime)
CREATE TABLE IF NOT EXISTS notifications (
    id         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title      TEXT NOT NULL,
    body       TEXT NOT NULL,
    category   TEXT DEFAULT 'general',
    is_read    BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- 10. PERFORMANCE INDEXES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_voter_profiles_hierarchy
    ON voter_profiles (state_id, district_id, pc_id, ac_id, polling_booth_id);

CREATE INDEX IF NOT EXISTS idx_users_scope
    ON users (scope_type, scope_id);

CREATE INDEX IF NOT EXISTS idx_audit_correlation
    ON audit_logs (correlation_id);

CREATE INDEX IF NOT EXISTS idx_audit_created_at
    ON audit_logs (created_at DESC);

CREATE INDEX IF NOT EXISTS idx_verification_tasks_officer
    ON verification_tasks (assigned_officer_id, status);

CREATE INDEX IF NOT EXISTS idx_grievances_status
    ON grievances (status, sla_deadline);

CREATE INDEX IF NOT EXISTS idx_voter_applications_status
    ON voter_applications (status, booth_id);

CREATE INDEX IF NOT EXISTS idx_notifications_user
    ON notifications (user_id, is_read, created_at DESC);

-- Trigram index for fast voter name search
CREATE INDEX IF NOT EXISTS idx_voter_name_trgm
    ON voter_profiles USING GIN (first_name gin_trgm_ops, last_name gin_trgm_ops);

-- ============================================================
-- 11. ROW LEVEL SECURITY
-- ============================================================

ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE voter_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE voter_applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE grievances ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;

-- Drop existing to avoid conflicts, then recreate
DROP POLICY IF EXISTS "Users can view own data" ON users;
DROP POLICY IF EXISTS "Voters can view own profile" ON voter_profiles;
DROP POLICY IF EXISTS "BLOs can view booth profiles" ON voter_profiles;
DROP POLICY IF EXISTS "DEOs can view district profiles" ON voter_profiles;
DROP POLICY IF EXISTS "CECs have global access" ON voter_profiles;

-- Users see their own row
CREATE POLICY "Users can view own data" ON users
    FOR SELECT USING (id = auth.uid()::uuid);

-- Voters see own profile
CREATE POLICY "Voters can view own profile" ON voter_profiles
    FOR SELECT USING (user_id = auth.uid()::uuid);

-- BLOs see their booth
CREATE POLICY "BLOs can view booth profiles" ON voter_profiles
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM users u
            WHERE u.id = auth.uid()::uuid
            AND u.role = 'booth_level_officer'
            AND u.scope_type = 'booth'
            AND u.scope_id = voter_profiles.polling_booth_id
        )
    );

-- DEOs see their district
CREATE POLICY "DEOs can view district profiles" ON voter_profiles
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM users u
            WHERE u.id = auth.uid()::uuid
            AND u.role = 'district_election_officer'
            AND u.scope_type = 'district'
            AND u.scope_id = voter_profiles.district_id
        )
    );

-- CEC has global access
CREATE POLICY "CECs have global access" ON voter_profiles
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM users u
            WHERE u.id = auth.uid()::uuid
            AND u.role = 'chief_election_commissioner'
        )
    );

-- Voters see own applications
DROP POLICY IF EXISTS "Voters see own applications" ON voter_applications;
CREATE POLICY "Voters see own applications" ON voter_applications
    FOR SELECT USING (user_id = auth.uid()::uuid);

-- Voters see own grievances
DROP POLICY IF EXISTS "Voters see own grievances" ON grievances;
CREATE POLICY "Voters see own grievances" ON grievances
    FOR SELECT USING (user_id = auth.uid()::uuid);

-- Voters see own notifications
DROP POLICY IF EXISTS "Voters see own notifications" ON notifications;
CREATE POLICY "Voters see own notifications" ON notifications
    FOR ALL USING (user_id = auth.uid()::uuid);
