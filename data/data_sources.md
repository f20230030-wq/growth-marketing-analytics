# Data Sources

> These datasets represent different businesses and are analyzed independently. They are not row-level joined. The project uses them as complementary case studies to demonstrate an end-to-end growth analytics framework.

## 1. Criteo Attribution Modeling for Bidding
- **Source:** https://huggingface.co/datasets/criteo/criteo-attribution-dataset (Criteo AI Lab)
- **Original company:** Criteo (display advertising)
- **Time period:** 30 days of live traffic (relative timestamps, no calendar dates)
- **Rows / columns:** 16,468,027 impressions / 22 columns
- **Grain:** one row = one ad impression
- **Key fields:** timestamp, uid, campaign, click, conversion, conversion_id, conversion_timestamp, attribution, cost, cpo
- **License:** CC BY-NC-SA 4.0. Citation: Diemert, Meynet, Galland, Lefortier (2017), "Attribution Modeling Increases Efficiency of Bidding in Display Advertising", AdKDD & TargetAd Workshop, KDD 2017
- **Metrics possible:** impressions, clicks, CTR, spend, CPC, CPM, conversions, CVR, CPA, frequency, time-to-conversion, attribution models
- **Metrics NOT possible:** revenue, AOV, ROAS, ROMI, LTV, retention
- **Caveats:** cost and cpo are transformed values (not real currency), so use them for relative comparison only

## 2. Google Analytics Sample (Google Merchandise Store)
- **Source:** bigquery-public-data.google_analytics_sample.ga_sessions_* (Google BigQuery Public Datasets)
- **Original company:** Google Merchandise Store (e-commerce)
- **Time period:** 2016-08-01 to 2017-08-01
- **Rows:** 903,653 sessions (verified via BigQuery)
- **Grain:** one row = one session (hits and products nested)
- **Key fields:** fullVisitorId, visitId, visitNumber, channelGrouping, trafficSource.*, device.*, geoNetwork.*, totals.*, hits.eCommerceAction
- **License:** Google Cloud public dataset terms; obfuscated data
- **Metrics possible:** sessions, users, new vs returning, bounce rate, pages/session, funnel stages, CVR, orders, revenue, AOV, revenue/session, channel and campaign performance, cohorts
- **Metrics NOT possible:** impressions, ad spend, CPC, CAC, ROAS, ROMI (scenario analysis only)
- **Caveats:** revenue stored x10^6; obfuscated data

## 3. Olist E-Commerce + Marketing Funnel
- **Source:** https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce and https://www.kaggle.com/datasets/olistbr/marketing-funnel-olist
- **Original company:** Olist (Brazilian marketplace)
- **Time period:** Orders 2016-2018; MQLs Jun 2017 - Jun 2018
- **Rows (verified):**
  - MQLs: 8,000 rows, 4 columns
  - Closed deals: 842 rows, 14 columns
  - Orders: 99,441 rows, 8 columns
  - Order items: 112,650 rows, 7 columns
  - Customers: 99,441 rows, 5 columns
  - Payments: 103,886 rows, 5 columns
- **Join keys:** mql_id (MQL -> deal), seller_id (deal -> order items), order_id, customer_id; use customer_unique_id for repeat customers
- **License:** CC BY-NC-SA 4.0 (confirm on the Kaggle page)
- **Metrics possible:** MQLs by origin, lead->deal CVR, days to close, seller activation, revenue per seller, orders, revenue, AOV, RFM, cohort retention
- **Metrics NOT possible:** impressions, clicks, spend, CPL, CAC, ROAS
- **Caveats:** funnel data is sampled (8k MQLs); very low repeat purchase rate
