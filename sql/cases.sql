USE `nlrb_data`;
DROP TABLE IF EXISTS `cases`;
CREATE TABLE `cases` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `case_type` VARCHAR(16),
    `region` VARCHAR(128),
    `case_number` VARCHAR(64) NOT NULL,
    `case_name` VARCHAR(128),
    `case_status` VARCHAR(32),
    `date_filed` DATE,
    `date_closed` DATE,
    `reason_closed` VARCHAR(128),
    `city` VARCHAR(256),
    `states_and_territories` VARCHAR(32),
    `employees_involved` VARCHAR(16),
    `allegations_raw` VARCHAR(4096),
    `participants_raw` VARCHAR(4096),
    `docket_activity_raw` VARCHAR(4096),
    `union_name` VARCHAR(512),
    `unit_sought` VARCHAR (512),
    `voters` INT,
    `allegations_parse_error` BOOLEAN NOT NULL DEFAULT TRUE,
    `participants_parse_error` BOOLEAN NOT NULL DEFAULT TRUE,
    `docket_activity_parse_error` BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (`id`),
    KEY (`case_number`)
) ENGINE=InnoDB CHARSET=utf8mb4
