USE `nlrb_data`;
CREATE TABLE IF NOT EXISTS `cases` (
    `id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `case_type` VARCHAR(8),
    `region` VARCHAR(32),
    `case_number` VARCHAR(64) UNIQUE NOT NULL,
    `case_name` VARCHAR(128),
    `case_status` VARCHAR(64),
    `date_filed` DATE,
    `date_closed` DATE,
    `reason_closed` VARCHAR(128),
    `city` VARCHAR(128),
    `states_and_territories` VARCHAR(512),
    `employees_involved` VARCHAR(512),
    `allegations_raw` VARCHAR(1024),
    `participants_raw` VARCHAR(1024),
    `docket_activity_raw` VARCHAR(1024),
    `union_name` VARCHAR(512),
    `unit_sought` VARCHAR(512),
    `voters` INT,
    `allegations_parse_error` BOOLEAN,
    `participants_parse_error` BOOLEAN,
    `docket_activity_parse_error` BOOLEAN
) ENGINE=InnoDB CHARSET=utf8mb4
