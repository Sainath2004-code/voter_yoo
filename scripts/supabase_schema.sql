-- Enable Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. AUTH SERVICE: USERS
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    full_name TEXT,
    role TEXT DEFAULT 'voter',
    state_code TEXT,
    district_code TEXT,
    constituency_id TEXT,
    booth_no INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    has_face_enrolled BOOLEAN DEFAULT FALSE,
    has_fingerprint_enrolled BOOLEAN DEFAULT FALSE,
    last_login TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. VOTER SERVICE: PROFILES & APPLICATIONS
CREATE TABLE IF NOT EXISTS voter_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    epic_id TEXT UNIQUE NOT NULL, -- Voter ID Card Number
    national_id TEXT UNIQUE NOT NULL, -- Aadhaar or similar
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_of_birth DATE NOT NULL,
    gender TEXT,
    address_line1 TEXT,
    address_line2 TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    constituency_id TEXT,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS voter_applications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    application_type TEXT NOT NULL, -- Form 6, 7, 8
    status TEXT DEFAULT 'pending', -- pending, approved, rejected
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    reviewed_at TIMESTAMP WITH TIME ZONE,
    reviewer_id UUID REFERENCES users(id),
    comments TEXT
);

-- 3. ELECTION SERVICE: ELECTIONS & CANDIDATES
CREATE TABLE IF NOT EXISTS elections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    type TEXT NOT NULL, -- lok_sabha, vidhan_sabha, etc.
    status TEXT DEFAULT 'notification',
    polling_date TIMESTAMP WITH TIME ZONE,
    results_date TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS constituencies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    code TEXT UNIQUE NOT NULL,
    state_code TEXT NOT NULL,
    type TEXT, -- LS or VS
    is_reserved BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS candidates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    election_id UUID REFERENCES elections(id),
    constituency_id UUID REFERENCES constituencies(id),
    full_name TEXT NOT NULL,
    party_name TEXT,
    symbol_url TEXT,
    status TEXT DEFAULT 'pending'
);

-- 4. BIOMETRIC SERVICE
CREATE TABLE IF NOT EXISTS biometric_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    type TEXT NOT NULL, -- 'face', 'fingerprint'
    template_hash TEXT NOT NULL, -- Secure hash of template
    enrolled_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. AUDIT SERVICE
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    action TEXT NOT NULL,
    resource TEXT NOT NULL,
    resource_id TEXT,
    ip_address TEXT,
    user_agent TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE voter_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE voter_applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE biometric_data ENABLE ROW LEVEL SECURITY;

-- Policies
-- Users can read their own user record
CREATE POLICY "Users can view own data" ON users 
    FOR SELECT USING (auth.uid() = id);

-- Users can read their own voter profile
CREATE POLICY "Users can view own profile" ON voter_profiles 
    FOR SELECT USING (auth.uid() = user_id);

-- Admins can read all profiles
CREATE POLICY "Admins can view all profiles" ON voter_profiles 
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE users.id = auth.uid() 
            AND users.role IN ('chief_election_commissioner', 'state_chief_electoral_officer')
        )
    );
