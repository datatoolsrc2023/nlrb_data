CREATE TABLE IF NOT EXISTS participants (
    id INTEGER PRIMARY KEY,
    case_id INT NOT NULL,
    case_number TEXT NOT NULL,
    p_kind TEXT,
    p_role TEXT,
    p_name TEXT,
    p_org TEXT,
    p_address TEXT,
    p_phone TEXT,
    raw_participant TEXT NOT NULL,
    CONSTRAINT fk_allegation_case
      FOREIGN KEY (case_id) REFERENCES cases (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);