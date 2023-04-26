CREATE TABLE IF NOT EXISTS nlrb_data.allegations (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    case_id INT NOT NULL,
    code VARCHAR(16) NOT NULL,
    description VARCHAR(256) NOT NULL,
    parse_error BOOLEAN NOT NULL,
    raw_text VARCHAR(256) NOT NULL,
    CONSTRAINT fk_allegation_case
      FOREIGN KEY (case_id) REFERENCES cases (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);
