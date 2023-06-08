CREATE TABLE IF NOT EXISTS error_log (
    id SERIAL PRIMARY KEY NOT NULL,
    case_id INT NOT NULL,
    allegations_parse_error BOOLEAN,
    participants_parse_error BOOLEAN,
    docket_activity_parse_error BOOLEAN,
    CONSTRAINT fk_error_log_case
        FOREIGN KEY (case_id) REFERENCES cases (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);