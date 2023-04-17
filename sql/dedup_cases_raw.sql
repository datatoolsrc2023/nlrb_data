DROP TABLE IF EXISTS cases_raw_deduped;
CREATE TABLE cases_raw_deduped AS
WITH dedup as (
    SELECT *, row_number() OVER (PARTITION BY case_number ORDER BY case_number DESC) as dup FROM cases_raw    
)
SELECT * FROM dedup WHERE dup=1;

ALTER TABLE cases_raw_deduped DROP COLUMN dup;