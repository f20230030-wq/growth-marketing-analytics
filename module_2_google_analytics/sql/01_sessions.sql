-- One row per session, with funnel-stage flags
SELECT
  PARSE_DATE('%Y%m%d', date)                     AS date,
  fullVisitorId                                  AS visitor_id,
  visitId                                        AS visit_id,
  visitNumber                                    AS visit_number,
  channelGrouping                                AS channel,
  trafficSource.source                           AS source,
  trafficSource.medium                           AS medium,
  trafficSource.campaign                         AS campaign,
  device.deviceCategory                          AS device,
  geoNetwork.country                             AS country,
  IFNULL(totals.pageviews, 0)                    AS pageviews,
  IFNULL(totals.bounces, 0)                      AS bounce,
  IFNULL(totals.transactions, 0)                 AS transactions,
  IFNULL(totals.transactionRevenue, 0) / 1e6     AS revenue,
  (SELECT COUNTIF(h.eCommerceAction.action_type = '2') FROM UNNEST(hits) h) > 0 AS product_view,
  (SELECT COUNTIF(h.eCommerceAction.action_type = '3') FROM UNNEST(hits) h) > 0 AS add_to_cart,
  (SELECT COUNTIF(h.eCommerceAction.action_type = '5') FROM UNNEST(hits) h) > 0 AS checkout,
  (SELECT COUNTIF(h.eCommerceAction.action_type = '6') FROM UNNEST(hits) h) > 0 AS purchase
FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`
WHERE _TABLE_SUFFIX BETWEEN '20160801' AND '20170801'
