CREATE TABLE IF NOT EXISTS allegations (
    id INTEGER PRIMARY KEY,
    case_id INT NOT NULL,
    code TEXT,
    description TEXT,
    raw_text TEXT NOT NULL,
    CONSTRAINT fk_allegation_case
      FOREIGN KEY (case_id) REFERENCES cases (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);