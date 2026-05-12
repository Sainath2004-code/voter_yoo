-- Enable Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis"; -- For GIS indexing

-- ==========================================
-- 1. GEOGRAPHIC HIERARCHY
-- ==========================================

CREATE TABLE IF NOT EXISTS states (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT UNIQUE NOT NULL,
    code TEXT UNIQUE NOT NULL, -- e.g., 'IN-DL'
    type TEXT, -- 'State' or 'UT'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS districts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    state_id UUID REFERENCES states(id),
    name TEXT NOT NULL,
    code TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS parliamentary_constituencies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    district_id UUID REFERENCES districts(id),
    name TEXT NOT NULL,
    code TEXT UNIQUE NOT NULL,
    is_reserved BOOLEAN DEFAULT FALSE,
    reservation_category TEXT, -- 'SC', 'ST', 'General'
    delimitation_version TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS assembly_constituencies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pc_id UUID REFERENCES parliamentary_constituencies(id),
    name TEXT NOT NULL,
    code TEXT UNIQUE NOT NULL,
    is_reserved BOOLEAN DEFAULT FALSE,
    reservation_category TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS polling_booths (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ac_id UUID REFERENCES assembly_constituencies(id),
    booth_no INTEGER NOT NULL,
    name TEXT NOT NULL,
    address TEXT,
    location GEOGRAPHY(POINT, 4326), -- PostGIS for mapping
    capacity INTEGER DEFAULT 1500,
    voter_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==========================================
-- 2. AUTH & IDENTITY
-- ==========================================

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    full_name TEXT,
    role TEXT NOT NULL DEFAULT 'voter',
    scope_type TEXT, -- 'national', 'state', 'district', 'pc', 'ac', 'booth'
    scope_id UUID, -- References one of the geography tables
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    mfa_enabled BOOLEAN DEFAULT FALSE,
    totp_secret TEXT,
    refresh_token TEXT,
    last_login TIMESTAMP WITH TIME ZONE,
    last_login_ip TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS voter_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    epic_number TEXT UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    father_name TEXT,
    spouse_name TEXT,
    date_of_birth DATE NOT NULL,
    gender TEXT NOT NULL,
    address_line1 TEXT NOT NULL,
    address_line2 TEXT,
    pincode TEXT NOT NULL,
    state_id UUID REFERENCES states(id),
    district_id UUID REFERENCES districts(id),
    pc_id UUID REFERENCES parliamentary_constituencies(id),
    ac_id UUID REFERENCES assembly_constituencies(id),
    polling_booth_id UUID REFERENCES polling_booths(id),
    aadhaar_hash TEXT UNIQUE,
    aadhaar_last4 TEXT,
    encrypted_aadhaar TEXT,
    verification_status TEXT DEFAULT 'pending',
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==========================================
-- 3. ELECTIONS & CANDIDATES
-- ==========================================

CREATE TABLE IF NOT EXISTS political_parties (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT UNIQUE NOT NULL,
    abbreviation TEXT UNIQUE NOT NULL,
    symbol_url TEXT,
    is_national BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS elections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    type TEXT NOT NULL, -- 'lok_sabha', 'vidhan_sabha'
    status TEXT DEFAULT 'notification',
    notification_date DATE,
    polling_date DATE,
    results_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS candidates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    election_id UUID REFERENCES elections(id),
    party_id UUID REFERENCES political_parties(id),
    constituency_id UUID NOT NULL, -- Generic ID mapped by constituency_type
    constituency_type TEXT NOT NULL, -- 'LS' or 'VS'
    voter_profile_id UUID REFERENCES voter_profiles(id),
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==========================================
-- 4. WORKFLOWS & AUDIT
-- ==========================================

CREATE TABLE IF NOT EXISTS grievances (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    category TEXT NOT NULL,
    subject TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT DEFAULT 'submitted', -- submitted, assigned, investigating, resolved, closed
    assigned_officer_id UUID REFERENCES users(id),
    sla_deadline TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    actor_id UUID REFERENCES users(id),
    action TEXT NOT NULL,
    resource TEXT NOT NULL,
    before_state JSONB,
    after_state JSONB,
    ip_address TEXT,
    correlation_id UUID,
    scope_type TEXT,
    scope_id UUID,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==========================================
-- 5. ROW LEVEL SECURITY (RLS)
-- ==========================================

ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE voter_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE voter_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE grievances ENABLE ROW LEVEL SECURITY;

-- Voters: Can only view their own data
CREATE POLICY "Users can view own data" ON users FOR SELECT USING (id = auth.uid());
CREATE POLICY "Voters can view own profile" ON voter_profiles FOR SELECT USING (user_id = auth.uid());

-- BLOs: Can only view profiles in their assigned booth
CREATE POLICY "BLOs can view booth profiles" ON voter_profiles 
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE users.id = auth.uid() 
            AND users.role = 'booth_level_officer' 
            AND users.scope_type = 'booth' 
            AND users.scope_id = voter_profiles.polling_booth_id
        )
    );

-- District Officers: Can only view profiles in their assigned district
CREATE POLICY "DEOs can view district profiles" ON voter_profiles 
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE users.id = auth.uid() 
            AND users.role = 'district_election_officer' 
            AND users.scope_type = 'district' 
            AND users.scope_id = voter_profiles.district_id
        )
    );

-- CEC: Global Access
CREATE POLICY "CECs have global access" ON voter_profiles 
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE users.id = auth.uid() 
            AND users.role = 'chief_election_commissioner'
        )
    );

-- ==========================================
-- 6. PERFORMANCE INDEXES
-- ==========================================

CREATE INDEX IF NOT EXISTS idx_voter_profiles_hierarchy ON voter_profiles (state_id, district_id, pc_id, ac_id, polling_booth_id);
CREATE INDEX IF NOT EXISTS idx_users_scope ON users (scope_type, scope_id);
CREATE INDEX IF NOT EXISTS idx_audit_correlation ON audit_logs (correlation_id);
CREATE INDEX IF NOT EXISTS idx_candidates_constituency ON candidates (constituency_id, constituency_type);
CREATE INDEX IF NOT EXISTS idx_polling_booths_location ON polling_booths USING GIST (location);
