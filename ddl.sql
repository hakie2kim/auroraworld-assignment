-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Links table
CREATE TABLE links (
    id SERIAL PRIMARY KEY,
    created_by INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    url TEXT NOT NULL,
    category VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX idx_links_name ON links(name);
CREATE INDEX idx_links_category ON links(category);

-- Link sharing table
CREATE TABLE link_shares (
    id SERIAL PRIMARY KEY,
    link_id INTEGER NOT NULL,
    shared_with INTEGER NOT NULL,
    can_write BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (link_id) REFERENCES links(id) ON DELETE CASCADE,
    FOREIGN KEY (shared_with) REFERENCES users(id) ON DELETE CASCADE
);

-- Unique constraint to prevent duplicate shares
CREATE UNIQUE INDEX idx_unique_link_share ON link_shares(link_id, shared_with);
