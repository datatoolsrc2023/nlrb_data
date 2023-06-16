USE `nlrb_data`;
CREATE TABLE IF NOT EXISTS `dockets` (
    `id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `case_id` INT NOT NULL,
    `case_number` VARCHAR(16) NOT NULL,
    `date` DATE NOT NULL,
    `document` TEXT NOT NULL,
    `issued_filed_by` TEXT NOT NULL,
    CONSTRAINT `fk_docket_case`
      FOREIGN KEY (case_id) REFERENCES cases (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB CHARSET=utf8mb4;
