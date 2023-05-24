CREATE TABLE IF NOT EXISTS error_log (
    id INTEGER PRIMARY KEY NOT NULL,
    case_id INT NOT NULL,
    allegations_parse_error TINYINT,
    participants_parse_error TINYINT,
    docket_activity_parse_error TINYINT,
    CONSTRAINT fk_error_log_case
        FOREIGN KEY (case_id) REFERENCES cases (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);