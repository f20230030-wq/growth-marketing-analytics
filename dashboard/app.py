from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / "module_1_criteo/outputs"
B = ROOT / "module_2_google_analytics/outputs"
C = ROOT / "module_3_olist/outputs"

st.set_page_config(page_title="Growth Marketing Analytics", layout="wide")

@st.cache_data
def load(path, idx=True):
    return pd.read_csv(path, index_col=0 if idx else None)

def first_col(df, name):
    df = df.reset_index()
    df.columns = [name] + list(df.columns[1:])
    return df

def kpis(path):
    return pd.read_csv(path, index_col=0).iloc[:, 0]

# ---------- data ----------
ka   = kpis(A / "overall_kpis.csv")
camp = load(A / "campaign_perf_stable.csv", idx=False)
freq = load(A / "frequency_curve.csv", idx=False).sort_values("sort_key")
attr = load(A / "attribution_by_campaign.csv", idx=False)

kb     = kpis(B / "overall_kpis.csv")
ch     = first_col(load(B / "channel_scorecard.csv"), "channel")
funnel = first_col(load(B / "funnel_overall.csv"), "stage")
dev    = first_col(load(B / "device_performance.csv"), "device")
nr     = first_col(load(B / "new_vs_returning.csv"), "visitor_type")
month  = first_col(load(B / "monthly_trend.csv"), "month").iloc[:-1]

origin = first_col(load(C / "origin_scorecard.csv"), "origin")
ltype  = first_col(load(C / "by_lead_type.csv"), "lead_type")
rfm    = first_col(load(C / "rfm_segments.csv"), "segment")
states = first_col(load(C / "top_states.csv"), "state")

camp["ctr_pct"] = camp.ctr * 100
camp["campaign"] = camp.campaign.astype(str)
cpa_spread = camp.cpa.quantile(0.9) / camp.cpa.quantile(0.1)

# ---------- header ----------
st.title("End-to-End Growth Marketing Analytics")
st.caption("Paid Media → Website Funnel → Leads → Customers → Revenue. "
           "Three independent public datasets from different businesses, analysed separately (not row-level joined).")

tab0, tab1, tab2, tab3 = st.tabs(["Overview", "Paid Media (Criteo)",
                                  "Website Funnel (Google Store)", "Leads & Customers (Olist)"])

# ---------- overview ----------
with tab0:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("Paid Media")
        st.metric("Impressions", f"{ka['Impressions']:,.0f}")
        st.metric("CTR", f"{ka['CTR %']:.2f}%")
        st.metric("CPA spread (worst vs best 10%)", f"{cpa_spread:.1f}x")
    with c2:
        st.subheader("Website Funnel")
        st.metric("Sessions", f"{kb['Sessions']:,.0f}")
        st.metric("Conversion rate", f"{kb['Conversion rate %']:.2f}%")
        st.metric("Revenue", f"${kb['Revenue $']:,.0f}")
    with c3:
        st.subheader("Leads & Customers")
        st.metric("Leads → deals", "10.5%")
        st.metric("Deals that activate (fair)", "~52%")
        st.metric("Customer repeat rate", "3.0%")

    st.subheader("Key findings")
    st.markdown(f"""
1. **Paid media:** CPA varies **{cpa_spread:.1f}x** between the best and worst campaigns, and the attribution model changes which campaigns look efficient.
2. **Referral's 42% revenue share is mostly returning visitors** mislabelled by GA (94.5% had no referring site).
3. **86% of website visits never view a product**, the biggest funnel leak. Mobile converts ~4x worse than desktop.
4. **Repeat buyers at the Google store:** 9.7% of buyers, 39.8% of revenue, worth 6x a one-time buyer.
5. **Paid Search is only profitable below ~$0.86 per click** (scenario at 50% margin). Accessories can sustain ~$1.31.
6. **Olist:** Paid Search leads are worth 3x Social leads (R$95 vs R$32). Big online shops are 15% of deals but 46% of revenue.
7. **Olist:** a "high-value, at-risk" segment (18.5% of customers) drove 43.6% of revenue, the top win-back target.
""")

# ---------- paid media ----------
with tab1:
    st.caption("Criteo: 30 days, 16.5M impressions. Cost values are transformed by Criteo, so compare campaigns relatively only.")
    c1, c2 = st.columns(2)
    with c1:
        fig = px.scatter(camp, x="ctr_pct", y="cpa", size="spend", hover_name="campaign", log_y=True,
                         labels={"ctr_pct": "CTR %", "cpa": "CPA (log scale)"},
                         title="High CTR ≠ low CPA (bubble = spend)")
        fig.add_vline(x=camp.ctr_pct.median(), line_dash="dash", line_color="grey")
        fig.add_hline(y=camp.cpa.median(), line_dash="dash", line_color="grey")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        top = camp.nlargest(15, "spend").sort_values("spend")
        fig = px.bar(top, x="spend", y="campaign", orientation="h", color="cpa",
                     color_continuous_scale="RdYlGn_r", title="Top 15 campaigns by spend (colour = CPA)")
        st.plotly_chart(fig, use_container_width=True)
    c3, c4 = st.columns(2)
    with c3:
        fig = px.line(freq, x="bucket", y="conv_rate_pct", markers=True,
                      labels={"bucket": "Impressions per user", "conv_rate_pct": "Conversion rate %"},
                      title="Conversion rate by ad frequency (correlation, not causation)")
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        ranks = ["rank_first_touch", "rank_linear", "rank_time_decay", "rank_last_touch"]
        t = attr.nlargest(15, "spend")[["campaign"] + ranks].copy()
        t["campaign"] = t.campaign.astype(str)
        long = t.melt(id_vars="campaign", var_name="model", value_name="CPA rank")
        long["model"] = long.model.str.replace("rank_", "").str.replace("_", " ").str.title()
        fig = px.line(long, x="model", y="CPA rank", color="campaign", markers=True,
                      title="CPA rank under each attribution model (top 15 by spend)")
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)

# ---------- website funnel ----------
with tab2:
    k = st.columns(5)
    k[0].metric("Sessions", f"{kb['Sessions']:,.0f}")
    k[1].metric("Conversion rate", f"{kb['Conversion rate %']:.2f}%")
    k[2].metric("Revenue", f"${kb['Revenue $']:,.0f}")
    k[3].metric("AOV", f"${kb['AOV $']:.0f}")
    k[4].metric("Revenue / session", f"${kb['Revenue per session $']:.2f}")

    c1, c2 = st.columns(2)
    with c1:
        long = ch.melt(id_vars="channel", value_vars=["session_share_%", "revenue_share_%"],
                       var_name="metric", value_name="percent")
        long["metric"] = long.metric.map({"session_share_%": "Share of traffic", "revenue_share_%": "Share of revenue"})
        fig = px.bar(long, x="percent", y="channel", color="metric", barmode="group", orientation="h",
                     title="Traffic share vs revenue share by channel")
        st.plotly_chart(fig, use_container_width=True)
        st.info("Referral looks like the star, but 94.5% of its revenue had no referring site. "
                "These are mostly returning visitors (44% new vs 78% site-wide). Social is 94% YouTube.")
    with c2:
        fig = px.funnel(funnel, x="count", y="stage", title="86% of visits never view a product")
        st.plotly_chart(fig, use_container_width=True)
    c3, c4, c5 = st.columns(3)
    with c3:
        st.plotly_chart(px.bar(dev, x="device", y="conversion_rate_%", text_auto=".2f",
                               title="Conversion rate by device"), use_container_width=True)
    with c4:
        st.plotly_chart(px.bar(nr, x="visitor_type", y="conversion_rate_%", text_auto=".2f",
                               title="New vs returning conversion"), use_container_width=True)
    with c5:
        st.plotly_chart(px.line(month, x="month", y="revenue", markers=True,
                                title="Monthly revenue"), use_container_width=True)

# ---------- leads & customers ----------
with tab3:
    k = st.columns(5)
    k[0].metric("Leads (MQLs)", "8,000")
    k[1].metric("Closed deals", "842 (10.5%)")
    k[2].metric("Activated sellers", "376")
    k[3].metric("Customers", "93,104")
    k[4].metric("Repeat rate", "3.0%")

    big = origin[origin.leads >= 100]
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.bar(big.sort_values("leads"), x="leads", y="origin", orientation="h",
                               title="Most leads…"), use_container_width=True)
    with c2:
        st.plotly_chart(px.bar(big.sort_values("revenue_per_lead"), x="revenue_per_lead", y="origin",
                               orientation="h", title="…vs most valuable leads (revenue per lead, R$)"),
                        use_container_width=True)
    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(px.bar(ltype.sort_values("revenue_per_deal"), x="revenue_per_deal", y="lead_type",
                               orientation="h", color="fair_activation_%", color_continuous_scale="Blues",
                               title="Revenue per deal by seller type (colour = activation %)"),
                        use_container_width=True)
    with c4:
        long = rfm.melt(id_vars="segment", value_vars=["customer_share_%", "revenue_share_%"],
                        var_name="metric", value_name="percent")
        long["metric"] = long.metric.map({"customer_share_%": "Share of customers", "revenue_share_%": "Share of revenue"})
        st.plotly_chart(px.bar(long, x="percent", y="segment", color="metric", barmode="group",
                               orientation="h", title="RFM segments: customers vs revenue"),
                        use_container_width=True)
    st.info("Sales-rep revenue varies 11x, but the top 3 reps' numbers are each driven by one seller "
            "(64–83% of their revenue, median deal R$0). SR_5 is the most consistent performer.")
    st.plotly_chart(px.bar(states, x="state", y="revenue_share_%", title="Top 10 states by revenue share"),
                    use_container_width=True)
