USE `nlrb_data`;
CREATE TABLE IF NOT EXISTS `pages` (
    `id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `case_id` INT NOT NULL,
    `case_number` VARCHAR(16) NOT NULL,
    `error` BOOLEAN NOT NULL,
    `raw_text` TEXT NOT NULL,
    CONSTRAINT `fk_pages_case`
      FOREIGN KEY (case_id) REFERENCES cases (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB CHARSET=utf8mb4;
