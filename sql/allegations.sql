CREATE TABLE IF NOT EXISTS allegations (
    id SERIAL PRIMARY KEY NOT NULL,
    case_id INT NOT NULL,
    code TEXT NOT NULL,
    description TEXT NOT NULL,
    parse_error BOOLEAN NOT NULL,
    raw_text TEXT NOT NULL,
    CONSTRAINT fk_allegation_case
      FOREIGN KEY (case_id) REFERENCES cases (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);
