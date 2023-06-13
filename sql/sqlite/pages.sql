CREATE TABLE IF NOT EXISTS pages (
    id INTEGER PRIMARY KEY NOT NULL,
    case_id INT NOT NULL,
    case_number TEXT UNIQUE NULL,
    raw_text TEXT NOT NULL,
    CONSTRAINT fk_pages_case
      FOREIGN KEY (case_id) REFERENCES cases (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);
