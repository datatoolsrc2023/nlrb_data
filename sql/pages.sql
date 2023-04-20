USE `nlrb_data`;
CREATE TABLE IF NOT EXISTS `pages` (
    `id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `case_id` INT NOT NULL,
    `case_number` VARCHAR(16) NOT NULL,
    `fetch_error` BOOLEAN NOT NULL,
    `write_error` BOOLEAN NOT NULL,
    CONSTRAINT `fk_pages_case`
      FOREIGN KEY (case_id) REFERENCES cases (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB CHARSET=utf8mb4;
