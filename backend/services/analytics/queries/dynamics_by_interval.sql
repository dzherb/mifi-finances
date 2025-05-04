WITH intervals AS (
  SELECT generate_series(
    date_trunc(:interval_unit, (:start_date)::date),
    date_trunc(:interval_unit, (:end_date)::date),
    (:interval_value)::interval
  )::date AS interval_start
),
transactions_per_interval AS (
  SELECT
    date_trunc(:interval_unit, occurred_at)::date AS interval_start,
    COUNT(*) AS transactions_count
  FROM
    transactions
  WHERE user_id = :user_id
  GROUP BY
    date_trunc(:interval_unit, occurred_at)
)

SELECT
  i.interval_start AS timestamp,
  COALESCE(t.transactions_count, 0) AS count
FROM
  intervals i
LEFT JOIN
  transactions_per_interval t ON i.interval_start = t.interval_start
ORDER BY
  i.interval_start;