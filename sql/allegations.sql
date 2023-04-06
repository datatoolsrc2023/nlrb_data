USE `nlrb_data`;
DROP TABLE IF EXISTS `allegations`;
CREATE TABLE `allegations` (
    `id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `case_id` INT NOT NULL,
    `code` VARCHAR(16) NOT NULL,
    `description` VARCHAR(256) NOT NULL,
    CONSTRAINT `fk_allegation_case`
      FOREIGN KEY (case_id) REFERENCES cases (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB CHARSET=utf8mb4;