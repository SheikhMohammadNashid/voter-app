CREATE TABLE IF NOT EXISTS tools (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    votes INTEGER DEFAULT 0
);

-- Seed some initial data
INSERT INTO tools (name, votes) VALUES 
('Ansible', 0),
('Docker', 0),
('Kubernetes', 0),
('Jenkins', 0),
('Terraform', 0)
ON CONFLICT (name) DO NOTHING;