USE `nlrb_data`;
CREATE TABLE IF NOT EXISTS `cases_raw` (
    `case_type` VARCHAR(8),
    `region` VARCHAR(32),
    `case_number` VARCHAR(64),
    `case_name` VARCHAR(128),
    `case_status` VARCHAR(64),
    `date_filed` VARCHAR(64),
    `date_closed` VARCHAR(64),
    `reason_closed` VARCHAR(128),
    `city` VARCHAR(128),
    `states_and_territories` VARCHAR(512),
    `employees_involved` VARCHAR(512),
    `allegations` VARCHAR(1024),
    `participants` VARCHAR(1024),
    `union_name` VARCHAR(512),
    `unit_sought` VARCHAR(512),
    `voters` INT
) ENGINE=InnoDB CHARSET=utf8mb4
