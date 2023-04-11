#!/bin/bash

set -x

echo "Emptying tables"
# Can't truncate cases due to foreign key from allegations
mysql -u nlrb -p nlrb_data -Be 'TRUNCATE allegations; DELETE FROM cases;'

echo "Reloading data"
./ingest.py case_files/nlrb-tesla_cases.csv
pushd allegations
make || exit 1
popd

echo "Summarizing"
mysql -u nlrb -p nlrb_data -Be 'SELECT COUNT(*) FROM cases; SELECT COUNT(*) FROM allegations;'
