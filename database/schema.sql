CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    skills TEXT,
    preferred_location TEXT
);

CREATE TABLE IF NOT EXISTS internships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT NOT NULL,
    location TEXT NOT NULL,
    stipend TEXT,
    skills_required TEXT,
    hiring_status TEXT
);
