-- alter_existing.sql
-- Safely ADD columns to tables that may have been created before our new schema.
-- Uses "IF NOT EXISTS" (PostgreSQL 9.6+) to be idempotent.

-- ── users ────────────────────────────────────────────────────────────────────
ALTER TABLE users ADD COLUMN IF NOT EXISTS phone TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS scope_type TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS scope_id UUID;
ALTER TABLE users ADD COLUMN IF NOT EXISTS has_face_enrolled BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS has_fingerprint_enrolled BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS failed_login_attempts INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN IF NOT EXISTS locked_until TIMESTAMPTZ;
ALTER TABLE users ADD COLUMN IF NOT EXISTS refresh_token TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login TIMESTAMPTZ;
ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login_ip TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT NOW();
ALTER TABLE users ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMPTZ;

-- ── voter_profiles ────────────────────────────────────────────────────────────
ALTER TABLE voter_profiles ADD COLUMN IF NOT EXISTS state_id UUID REFERENCES states(id);
ALTER TABLE voter_profiles ADD COLUMN IF NOT EXISTS district_id UUID REFERENCES districts(id);
ALTER TABLE voter_profiles ADD COLUMN IF NOT EXISTS pc_id UUID REFERENCES parliamentary_constituencies(id);
ALTER TABLE voter_profiles ADD COLUMN IF NOT EXISTS ac_id UUID REFERENCES assembly_constituencies(id);
ALTER TABLE voter_profiles ADD COLUMN IF NOT EXISTS polling_booth_id UUID REFERENCES polling_booths(id);
ALTER TABLE voter_profiles ADD COLUMN IF NOT EXISTS aadhaar_hash TEXT;
ALTER TABLE voter_profiles ADD COLUMN IF NOT EXISTS aadhaar_last4 TEXT;
ALTER TABLE voter_profiles ADD COLUMN IF NOT EXISTS encrypted_aadhaar TEXT;
ALTER TABLE voter_profiles ADD COLUMN IF NOT EXISTS verification_status TEXT DEFAULT 'pending';
ALTER TABLE voter_profiles ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT NOW();

-- ── voter_applications ────────────────────────────────────────────────────────
ALTER TABLE voter_applications ADD COLUMN IF NOT EXISTS state_id UUID REFERENCES states(id);
ALTER TABLE voter_applications ADD COLUMN IF NOT EXISTS district_id UUID REFERENCES districts(id);
ALTER TABLE voter_applications ADD COLUMN IF NOT EXISTS ac_id UUID REFERENCES assembly_constituencies(id);
ALTER TABLE voter_applications ADD COLUMN IF NOT EXISTS booth_id UUID REFERENCES polling_booths(id);
ALTER TABLE voter_applications ADD COLUMN IF NOT EXISTS form_data JSONB;
ALTER TABLE voter_applications ADD COLUMN IF NOT EXISTS current_task_id UUID;
ALTER TABLE voter_applications ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT NOW();

-- ── grievances ────────────────────────────────────────────────────────────────
ALTER TABLE grievances ADD COLUMN IF NOT EXISTS state_id UUID REFERENCES states(id);
ALTER TABLE grievances ADD COLUMN IF NOT EXISTS district_id UUID REFERENCES districts(id);
ALTER TABLE grievances ADD COLUMN IF NOT EXISTS ac_id UUID REFERENCES assembly_constituencies(id);
ALTER TABLE grievances ADD COLUMN IF NOT EXISTS priority TEXT DEFAULT 'medium';
ALTER TABLE grievances ADD COLUMN IF NOT EXISTS resolution_notes TEXT;
ALTER TABLE grievances ADD COLUMN IF NOT EXISTS attachment_urls JSONB DEFAULT '[]';
ALTER TABLE grievances ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT NOW();

-- ── audit_logs ────────────────────────────────────────────────────────────────
ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS actor_role TEXT;
ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS resource_id TEXT;
ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS correlation_id TEXT;
ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS user_agent TEXT;
ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS scope_type TEXT;
ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS scope_id TEXT;
ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT NOW();

-- Rename timestamp -> created_at if legacy column exists
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'audit_logs' AND column_name = 'timestamp'
    ) AND NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'audit_logs' AND column_name = 'created_at'
    ) THEN
        ALTER TABLE audit_logs RENAME COLUMN "timestamp" TO created_at;
    END IF;
END $$;

-- ── Now create indexes that depend on the added columns ───────────────────────
CREATE INDEX IF NOT EXISTS idx_voter_profiles_hierarchy
    ON voter_profiles (state_id, district_id, pc_id, ac_id, polling_booth_id);

CREATE INDEX IF NOT EXISTS idx_users_scope
    ON users (scope_type, scope_id);

CREATE INDEX IF NOT EXISTS idx_audit_correlation
    ON audit_logs (correlation_id);

CREATE INDEX IF NOT EXISTS idx_audit_created_at
    ON audit_logs (created_at DESC);

CREATE INDEX IF NOT EXISTS idx_voter_applications_status
    ON voter_applications (status, booth_id);

CREATE INDEX IF NOT EXISTS idx_notifications_user
    ON notifications (user_id, is_read, created_at DESC);

-- ── RLS: drop old policies, recreate with corrected column references ─────────
DROP POLICY IF EXISTS "BLOs can view booth profiles" ON voter_profiles;
DROP POLICY IF EXISTS "DEOs can view district profiles" ON voter_profiles;
DROP POLICY IF EXISTS "CECs have global access" ON voter_profiles;

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

CREATE POLICY "CECs have global access" ON voter_profiles
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM users u
            WHERE u.id = auth.uid()::uuid
            AND u.role = 'chief_election_commissioner'
        )
    );

DROP POLICY IF EXISTS "Voters see own applications" ON voter_applications;
CREATE POLICY "Voters see own applications" ON voter_applications
    FOR SELECT USING (user_id = auth.uid()::uuid);

DROP POLICY IF EXISTS "Voters see own grievances" ON grievances;
CREATE POLICY "Voters see own grievances" ON grievances
    FOR SELECT USING (user_id = auth.uid()::uuid);

DROP POLICY IF EXISTS "Voters see own notifications" ON notifications;
CREATE POLICY "Voters see own notifications" ON notifications
    FOR ALL USING (user_id = auth.uid()::uuid);
