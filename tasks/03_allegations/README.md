# Allegations task

Running `make` in this directory locally will:

* Read each case's `allegations_raw`, when not null or empty
* Attempt to parse any allegations within the text
* Populate the `allegations` table for each allegation found
* Set the `error_log` table's `allegations_parse_error` to `1`/`true` if one or more allegations failed to parse.