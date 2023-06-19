CREATE TABLE IF NOT EXISTS participants (
    id SERIAL PRIMARY KEY,
    case_id INT NOT NULL,
    p_type TEXT,
    p_role TEXT,
    p_name TEXT,
    p_organization TEXT,
    p_address TEXT,
    p_phone TEXT,
    raw_participant TEXT NOT NULL,
    CONSTRAINT fk_participant_case
      FOREIGN KEY (case_id) REFERENCES cases (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);
