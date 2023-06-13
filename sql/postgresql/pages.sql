CREATE TABLE IF NOT EXISTS pages (
    id SERIAL PRIMARY KEY NOT NULL,
    case_id INT NOT NULL,
    case_number TEXT NOT NULL,
    raw_text TEXT NOT NULL,
    CONSTRAINT fk_pages_case
      FOREIGN KEY (case_id) REFERENCES cases (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);
