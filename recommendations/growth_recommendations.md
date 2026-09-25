# Growth Recommendations Memo

**Project:** End-to-End Growth Marketing Analytics
**Scope:** Three independent public datasets. Criteo (paid media, 16.5M impressions), Google Merchandise Store (903,653 web sessions), Olist (8,000 leads, 96,211 orders). Each is a different business, analysed separately. Recommendations are made per business; cross-dataset patterns are noted as patterns, not as combined results.

---

## 1. What to scale

- **Paid Search is the strongest known acquisition source in both businesses where it appears.**
  - *Olist:* Paid Search leads are worth **R$95 each** vs R$32 for Social, with the best lead→deal rate among large sources (12.3%) and the highest fair activation (59%).
  - *Google Store:* Paid Search converts at 1.85% vs 1.28% site-wide. The **Accessories** campaign earns $2.63 per session and stays profitable up to **~$1.31 CPC** (vs ~$0.86 for Paid Search overall, at a 50% margin assumption), so it's the first place to add budget.
- **Target big and medium online sellers (Olist).** "online_big" sellers are ~15% of deals but **46% of revenue**, with 72% activation and **12x** the revenue per deal of offline sellers.
- **Email and deal-site referrals (Google Store).** The genuine referral sources convert far above average: email 4.3%, coupon site 7.6%.
- **Paid media (Criteo):** CPA varies **13.0x** between the best and worst 10% of campaigns. Shift budget from the worst-decile campaigns to the low-CPA / high-CTR quadrant.

## 2. What appears inefficient

- **Social brings volume, not value, in both businesses.**
  - *Google Store:* 25% of traffic, **0.3% of revenue**. 94% of it is YouTube, with a 67% bounce rate.
  - *Olist:* 17% of leads, 6.5% of revenue. Only **5.6% of leads become deals**, and they take the longest to close (30 days).
  - Treat Social/YouTube as awareness and judge it on assisted and returning conversions, not last-touch sales.
- **Affiliates ("Data Share Promo")** at the Google Store: 16,403 sessions, 0.05% conversion, $0.04 per session.
- **Display leads at Olist:** R$8 per lead, the lowest of any source.
- **Display at the Google Store is not proven.** Its high revenue per session comes from 5 orders (61% of Display revenue; median order $74).

## 3. Where the biggest leaks are

| Business | Leak | Size |
|---|---|---|
| Google Store | Visits that never view a product | **86%** of sessions |
| Google Store | Mobile vs desktop conversion | 0.41% vs 1.58% (~4x gap) |
| Olist (sellers) | Signed sellers who never make a sale | ~48% (fair, ≥90 days observed) |
| Olist (buyers) | Customers who never buy again | **97%** (3.0% repeat rate) |

## 4. What to test next

| # | Test | Hypothesis | Primary metric |
|---|---|---|---|
| 1 | **Product-first homepage and landing pages** (A/B test) | Showing bestsellers above the fold increases product views | Product-view rate (baseline 13.7%) |
| 2 | **Mobile checkout simplification** | Fewer steps and saved payment close part of the 4x mobile gap | Mobile conversion rate (baseline 0.41%) |
| 3 | **Olist win-back campaign** for the "high-value, at-risk" segment (17,189 customers, 43.6% of revenue), with a 10% holdout group | A targeted offer reactivates past big spenders | Reactivation rate. Scenario: 5% reactivation ≈ **R$335k** extra revenue |
| 4 | **Retarget YouTube visitors** with a dedicated landing page | Returning visitors convert 5.5x better, so bringing YouTube traffic back lifts its value | Return-visit and conversion rate of YouTube cohort |
| 5 | **Lead scoring and seller onboarding (Olist)**: prioritise online big/medium leads, add a 30-day first-sale programme | Better-fit leads and early support raise activation | Lead→deal rate, fair activation rate |

## 5. Measurement fixes (do these first)

- **Tag campaigns.** Only **3.1%** of Google Store sessions carry a campaign tag.
- **Capture lead source.** 14.5% of Olist leads have no origin, yet they are the **most valuable (R$182 per lead)**.
- **Fix channel rules.** 94.5% of "Referral" revenue at the Google Store had no referring site. Report returning/direct visitors separately.
- **Move beyond last-click.** In the Criteo data, [X] campaigns change CPA rank by ≥10 places between first- and last-touch attribution.
- **Judge sales reps on median deal value and activation, not averages.** The top three Olist reps' results were each driven by one seller (64–83% of their revenue).

---

*Caveats: Criteo costs are transformed (relative comparison only). Google Store ad spend is not in the data, so ROAS/CAC figures are scenario-based. Olist activation is adjusted for sellers with <90 days of observable sales.*
