# End-to-End Growth Marketing Analytics: Paid Media, Customer Funnels & Revenue

**Live dashboard:** https://growth-marketing-analytics-9mhkajtxntavbkqxcdst59.streamlit.app  ·  **Recommendations memo:** [recommendations/growth_recommendations.md](recommendations/growth_recommendations.md)

An end-to-end growth analytics framework applied to three real, public datasets, covering the full journey from ad impression to repeat customer:

**Paid Media → Website Funnel → Leads → Customers → Revenue → Retention**

> **Data integrity note:** These datasets represent different businesses and are analyzed independently. They are not row-level joined. The project uses them as complementary case studies to demonstrate an end-to-end growth analytics framework.

---

## Datasets

| Module | Dataset | Business | Size | Grain |
|---|---|---|---|---|
| A. Paid Media | [Criteo Attribution Modeling for Bidding](https://huggingface.co/datasets/criteo/criteo-attribution-dataset) | Display advertising | 16.5M impressions, 675 campaigns, 30 days | Impression |
| B. Website Funnel | [Google Analytics Sample](https://console.cloud.google.com/marketplace/product/obfuscated-ga360-data/obfuscated-ga360-data) (BigQuery) | Google Merchandise Store | 903,653 sessions, Aug 2016 – Aug 2017 | Session |
| C. Leads & Customers | [Olist E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) + [Olist Marketing Funnel](https://www.kaggle.com/datasets/olistbr/marketing-funnel-olist) | Brazilian marketplace | 8,000 leads, 842 deals, 96,211 orders | Lead / order |

Full documentation (sources, row counts, licenses, possible and impossible metrics): [`data/data_sources.md`](data/data_sources.md)

---

## Module A: Paid Media (Criteo)

**Question:** Which campaigns acquire customers efficiently, and does the attribution model change the answer?

**Methods:** DuckDB + SQL on 16.5M rows · data quality checks · campaign-level CTR, CPC, CPM, CVR, CPA, frequency · volume filter (≥10k impressions, ≥20 conversions) · user-journey reconstruction · first-touch, last-touch, linear and time-decay attribution

**Key findings**
- **CPA varies 13.0x** between the best and worst 10% of campaigns (346 campaigns with stable volume).
- **Half of buyers convert within 2.7 days** of their first ad and within 0.9 days of their last. 75% convert within 12 days, which caps useful retargeting windows.
- **30.8% of conversions involve 2+ campaigns.** Switching from last- to first-touch moves **188 of 346 campaigns by 10+ CPA-rank places** (max 113), though the overall ranking stays highly correlated (0.97). Attribution mainly changes decisions for mid-ranked and journey-starting campaigns.

*Caveats: costs are transformed by Criteo (relative comparison only). CTR (36%) is inflated by sub-sampling and is used only to compare campaigns.*

---

## Module B: Website Funnel (Google Merchandise Store)

**Question:** Where do visitors come from, where do they drop off, and who buys?

**Methods:** BigQuery SQL (UNNEST of nested hits) · session-level funnel flags · channel scorecard · funnel by channel and device · source-level deep dives · cohort retention · repeat-buyer analysis · break-even CPC scenario model (Excel)

**Key findings**
- **Referral appears to drive 42% of revenue from 12% of traffic, but 94.5% of it had no referring site.** Those sessions skew heavily toward returning visitors (44% new vs 78% site-wide), so this is a GA attribution effect, not a scalable channel.
- **Social = 25% of traffic, 0.3% of revenue.** 94% of it is YouTube (67% bounce), acting as awareness, not sales.
- **86% of sessions never view a product**, the largest funnel leak. **Mobile converts ~4x worse** than desktop (0.41% vs 1.58%).
- **Repeat buyers are 9.7% of buyers but 39.8% of revenue**, worth $631 vs $102 for one-time buyers.
- Display's apparent strength is driven by **5 orders (61% of its revenue)**. Median order $74.
- With no ad-cost data, a scenario model shows **Paid Search breaks even at ~$0.86 CPC** (50% margin). The Accessories campaign can sustain ~$1.31.

---

## Module C: Leads & Customers (Olist)

**Question:** Which sources bring leads that turn into revenue, not just leads?

**Methods:** Multi-table joins (lead → deal → seller → orders) · origin scorecard · activation adjusted for observation window · seller-type and sales-rep analysis with mix-effect and outlier checks · RFM segmentation · cohort retention

**Key findings**
- **Most leads ≠ most valuable leads.** Social brings 17% of leads but 6.5% of revenue (R$32 per lead). Paid Search brings 20% of leads and 23% of revenue (**R$95 per lead**).
- **Untracked leads are the most valuable (R$182 per lead, 32% of revenue)**, a lead-source tracking gap.
- After adjusting for sellers with <90 days of sales data, **~52% of new sellers activate**. Differences between sources come mainly from lead→deal conversion and seller size.
- **Big online shops: ~15% of deals, 46% of revenue**, 12x the revenue per deal of offline sellers.
- The **11x revenue-per-deal gap between sales reps is not skill.** It's uncorrelated with lead mix (−0.42), and the top 3 reps' results are each driven by one seller (64–83% of their revenue, median deal R$0).
- **Only 3.0% of customers repurchase**, yet a "high-value, at-risk" segment (18.5% of customers) drove **43.6% of revenue**, the top win-back target (5% reactivation ≈ R$335k, scenario).

---

## Recommendations (summary)

1. **Scale** Paid Search (esp. Accessories), big/medium online seller acquisition, and email/deal-site partnerships.
2. **Reframe** Social/YouTube as awareness and retarget those visitors. **Cut** the affiliate promo.
3. **Fix leaks:** product-first landing pages, mobile checkout, seller onboarding, Olist win-back campaign.
4. **Fix measurement first:** campaign tagging (3.1% tagged), lead-source capture, channel rules, beyond-last-click attribution.

Full memo: [recommendations/growth_recommendations.md](recommendations/growth_recommendations.md)

---

## Tech stack

**SQL** (BigQuery, DuckDB) · **Python** (pandas, matplotlib, plotly) · **Streamlit** (dashboard) · **Excel** (scenario model) · **Git/GitHub**

## Repository structure
├── data/ # data_sources.md (raw data not committed)
├── module_1_criteo/ # sql/, python/ notebooks, outputs/
├── module_2_google_analytics/ # sql/, python/ notebooks, outputs/ (incl. roas_scenario.xlsx)
├── module_3_olist/ # python/ notebooks, outputs/
├── dashboard/ # Streamlit app
└── recommendations/ # growth recommendations memo


## Reproduce

1. `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
2. Download Criteo from Hugging Face into `data/raw/criteo/`, and both Olist datasets from Kaggle into `data/raw/olist/`.
3. Google Analytics: set your Google Cloud project ID in `module_2_google_analytics/python/01_extract.ipynb` (BigQuery Sandbox is free).
4. Run notebooks in order within each module, then `streamlit run dashboard/app.py`.

## Licenses & citations

- **Criteo:** CC BY-NC-SA 4.0. Diemert, Meynet, Galland, Lefortier (2017), *Attribution Modeling Increases Efficiency of Bidding in Display Advertising*, AdKDD & TargetAd Workshop, KDD.
- **Olist:** CC BY-NC-SA 4.0 (Kaggle).
- **Google Analytics Sample:** Google Cloud public dataset (obfuscated).

Non-commercial portfolio project.

---

**Author:** Madhumitha
