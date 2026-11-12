-- BigQuery Standard SQL: calendar 1 (four fixed days in each year).
-- Parameterize @first_token, @rest_prefix using query_mappings.csv.
-- This matches the timestamp-range form used in the original Colab queries.
-- Before running: execute a dry run and set maximum_bytes_billed.
SELECT EXTRACT(YEAR FROM date) AS year,
       COUNT(*) AS mentions,
       COUNT(DISTINCT url) AS articles
FROM `gdelt-bq.gdeltv2.webngrams`
WHERE (
    (date >= TIMESTAMP('2022-01-15') AND date < TIMESTAMP_ADD(TIMESTAMP('2022-01-15'), INTERVAL 1 DAY)) OR
    (date >= TIMESTAMP('2022-04-15') AND date < TIMESTAMP_ADD(TIMESTAMP('2022-04-15'), INTERVAL 1 DAY)) OR
    (date >= TIMESTAMP('2022-07-15') AND date < TIMESTAMP_ADD(TIMESTAMP('2022-07-15'), INTERVAL 1 DAY)) OR
    (date >= TIMESTAMP('2022-10-15') AND date < TIMESTAMP_ADD(TIMESTAMP('2022-10-15'), INTERVAL 1 DAY)) OR
    (date >= TIMESTAMP('2023-01-15') AND date < TIMESTAMP_ADD(TIMESTAMP('2023-01-15'), INTERVAL 1 DAY)) OR
    (date >= TIMESTAMP('2023-04-15') AND date < TIMESTAMP_ADD(TIMESTAMP('2023-04-15'), INTERVAL 1 DAY)) OR
    (date >= TIMESTAMP('2023-07-15') AND date < TIMESTAMP_ADD(TIMESTAMP('2023-07-15'), INTERVAL 1 DAY)) OR
    (date >= TIMESTAMP('2023-10-15') AND date < TIMESTAMP_ADD(TIMESTAMP('2023-10-15'), INTERVAL 1 DAY))
)
  AND ngram = @first_token
  AND STARTS_WITH(post, @rest_prefix)
  AND lang = 'en'
GROUP BY year ORDER BY year;
-- For calendar 2, replace the eight dates using sampling_dates.csv.
-- These queries are for optional live re-extraction, potentially billable.
