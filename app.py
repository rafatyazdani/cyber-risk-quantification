import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Cyber Risk Quantification",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ Cyber Risk Quantification Dashboard")
st.caption(
    "Financial risk modeling for cybersecurity — built on FAIR methodology "
    "and Monte Carlo simulation."
)

# ── Helpers ───────────────────────────────────────────────────────────────────

def simulate_ale(tef_range, loss_mean, loss_sigma, n):
    tef  = np.random.triangular(*tef_range, n)
    loss = np.random.lognormal(loss_mean, loss_sigma, n)
    return tef * loss


def apply_control(tef_range, reduction):
    return tuple(x * (1 - reduction) for x in tef_range)


def fmt(value):
    if value >= 1_000_000:
        return f"${value/1_000_000:.1f}M"
    if value >= 1_000:
        return f"${value/1_000:.0f}K"
    return f"${value:,.0f}"


# ── Sidebar — model inputs ────────────────────────────────────────────────────

st.sidebar.header("Model Inputs")

scenario = st.sidebar.selectbox(
    "Threat Scenario",
    ["Ransomware", "Cloud Breach", "AI Misuse"],
)

simulations = st.sidebar.slider(
    "Monte Carlo Simulations", 1_000, 50_000, 10_000, step=1_000
)

control_cost = st.sidebar.number_input(
    "Control Investment Cost ($/yr)", min_value=0, value=1_000_000, step=50_000
)

st.sidebar.markdown("---")
st.sidebar.subheader("Loss Distribution Parameters")

loss_mean  = st.sidebar.slider("Loss Mean (log scale)", 12.0, 16.0, 14.5, step=0.1)
loss_sigma = st.sidebar.slider("Loss Sigma (uncertainty)", 0.3, 1.5, 0.7, step=0.05)

# ── Sidebar — client data mapping (optional) ──────────────────────────────────

st.sidebar.markdown("---")
st.sidebar.subheader("Client Data Mapping (Optional)")
use_client_inputs = st.sidebar.checkbox("Map client operational data to model")

if use_client_inputs:
    incidents_per_year      = st.sidebar.slider("Incidents per Year", 0, 20, 3)
    downtime_cost_per_day   = st.sidebar.slider("Downtime Cost/Day ($)", 10_000, 1_000_000, 250_000, step=10_000)
    avg_days_downtime       = st.sidebar.slider("Avg Downtime (Days)", 1, 10, 3)
    mfa_coverage            = st.sidebar.slider("MFA Coverage (%)", 0, 100, 50)
    edr_maturity            = st.sidebar.selectbox("EDR Maturity", ["Low", "Medium", "High"])
    backup_maturity         = st.sidebar.selectbox("Backup Maturity", ["Low", "Medium", "High"])

    # Map incident history → TEF
    tef_min  = max(0.1, incidents_per_year * 0.5)
    tef_mode = float(incidents_per_year)
    tef_max  = incidents_per_year * 2.0
    base_tef = (tef_min, tef_mode, tef_max)

    # Map downtime costs → loss magnitude
    base_loss  = downtime_cost_per_day * avg_days_downtime
    loss_mean  = np.log(max(base_loss, 1))
    loss_sigma = 0.7

    # Map control maturity → control effectiveness
    edr_scores    = {"Low": 0.10, "Medium": 0.25, "High": 0.40}
    backup_scores = {"Low": 0.05, "Medium": 0.15, "High": 0.30}
    control_score = (mfa_coverage / 100) * 0.30 + edr_scores[edr_maturity] + backup_scores[backup_maturity]
    control_reduction = min(control_score, 0.90)

    st.sidebar.success(f"Control effectiveness mapped to **{control_reduction:.0%}**")

else:
    scenario_tef = {
        "Ransomware":  (1.0, 3.0, 6.0),
        "Cloud Breach": (0.5, 1.0, 2.0),
        "AI Misuse":   (2.0, 4.0, 8.0),
    }
    base_tef          = scenario_tef[scenario]
    control_reduction = st.sidebar.slider("Control Effectiveness (%)", 0.0, 0.90, 0.40, step=0.05)

# ── Run simulation ────────────────────────────────────────────────────────────

np.random.seed(42)

baseline        = simulate_ale(base_tef, loss_mean, loss_sigma, simulations)
controlled_tef  = apply_control(base_tef, control_reduction)
controlled      = simulate_ale(controlled_tef, loss_mean, loss_sigma, simulations)

b_median = np.percentile(baseline, 50)
b_p90    = np.percentile(baseline, 90)
b_p95    = np.percentile(baseline, 95)

c_median = np.percentile(controlled, 50)
c_p90    = np.percentile(controlled, 90)

risk_reduction = b_median - c_median
roi            = (risk_reduction - control_cost) / control_cost if control_cost > 0 else 0
prob_over_10m  = np.mean(baseline > 10_000_000)

# ── Metrics row ───────────────────────────────────────────────────────────────

st.markdown("### Financial Risk Summary")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Median Loss (Baseline)",    fmt(b_median))
col2.metric("90th Percentile (Baseline)", fmt(b_p90))
col3.metric("Median Loss (Controlled)",  fmt(c_median), delta=f"-{fmt(risk_reduction)}", delta_color="inverse")
col4.metric("Annual Risk Reduction",     fmt(risk_reduction))
col5.metric("Control ROI",               f"{roi:.1f}x", delta="positive" if roi > 0 else "negative", delta_color="normal")

st.markdown("---")

# ── Charts ────────────────────────────────────────────────────────────────────

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Loss Distribution")

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(baseline,   bins=60, alpha=0.55, color="#A100FF", label="Baseline",   density=True)
    ax.hist(controlled, bins=60, alpha=0.55, color="#00C4B4", label="Controlled", density=True)

    ax.axvline(b_median, color="#A100FF", linestyle="--", linewidth=1.2, label=f"Baseline Median {fmt(b_median)}")
    ax.axvline(b_p95,    color="#FF4B4B", linestyle=":",  linewidth=1.2, label=f"95th Pct (Tail) {fmt(b_p95)}")
    ax.axvline(c_median, color="#00C4B4", linestyle="--", linewidth=1.2, label=f"Controlled Median {fmt(c_median)}")

    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: fmt(x)))
    ax.set_xlabel("Annual Loss")
    ax.set_ylabel("Probability Density")
    ax.set_title(f"{scenario} — Annual Loss Distribution ({simulations:,} simulations)")
    ax.legend(fontsize=7)
    fig.tight_layout()
    st.pyplot(fig)

with col_b:
    st.subheader("Loss Exceedance Curve")

    sorted_ale = np.sort(baseline)[::-1]
    exceedance = np.arange(1, len(sorted_ale) + 1) / len(sorted_ale)

    fig2, ax2 = plt.subplots(figsize=(7, 4))
    ax2.plot(sorted_ale, exceedance, color="#A100FF", linewidth=1.8, label="Probability of exceedance")
    ax2.axhline(0.10, color="#FF4B4B", linestyle=":", linewidth=1, label="10% exceedance (VaR-90)")
    ax2.axhline(0.05, color="#FFA500", linestyle=":", linewidth=1, label="5% exceedance (VaR-95)")
    ax2.fill_between(sorted_ale, exceedance, alpha=0.08, color="#A100FF")

    ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: fmt(x)))
    ax2.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    ax2.set_xlabel("Annual Loss")
    ax2.set_ylabel("Probability of Exceeding")
    ax2.set_title("Loss Exceedance Curve")
    ax2.legend(fontsize=7)
    fig2.tight_layout()
    st.pyplot(fig2)

# ── Control ROI table ─────────────────────────────────────────────────────────

st.markdown("---")
st.subheader("Control Effectiveness Sensitivity")

levels  = [0.0, 0.20, 0.40, 0.60, 0.80]
rows    = []
np.random.seed(42)
b_med_fixed = np.percentile(simulate_ale(base_tef, loss_mean, loss_sigma, simulations), 50)

for lvl in levels:
    np.random.seed(42)
    c_ale  = simulate_ale(apply_control(base_tef, lvl), loss_mean, loss_sigma, simulations)
    c_med  = np.percentile(c_ale, 50)
    red    = b_med_fixed - c_med
    r      = (red - control_cost) / control_cost if control_cost > 0 else 0
    rows.append({
        "Control Effectiveness": f"{lvl:.0%}",
        "Controlled Median Loss": fmt(c_med),
        "Annual Risk Reduction":  fmt(red),
        "ROI":                    f"{r:.2f}x",
        "Justified?":             "✅ Yes" if r > 0 else "❌ No",
    })

import pandas as pd
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ── Insight ───────────────────────────────────────────────────────────────────

st.markdown("---")
st.subheader("Strategic Insight")

prob_str = f"{prob_over_10m:.1%}"

if roi > 1.0:
    st.success(
        f"**The control investment is strongly justified.** "
        f"At {control_reduction:.0%} effectiveness, a {fmt(control_cost)}/yr investment "
        f"returns **{roi:.1f}x ROI** by reducing median annual exposure from "
        f"**{fmt(b_median)}** to **{fmt(c_median)}** — a saving of **{fmt(risk_reduction)}/yr**. "
        f"There is a **{prob_str}** probability of a single-year loss exceeding $10M without controls."
    )
elif roi > 0:
    st.info(
        f"**The control investment is marginally justified.** "
        f"At {control_reduction:.0%} effectiveness, the {fmt(control_cost)}/yr investment "
        f"yields a {roi:.2f}x ROI. Consider whether higher-effectiveness controls "
        f"or a lower-cost implementation could improve the return."
    )
else:
    st.warning(
        f"**The control investment is not financially justified at current assumptions.** "
        f"At {control_reduction:.0%} effectiveness and {fmt(control_cost)}/yr cost, "
        f"the expected risk reduction ({fmt(risk_reduction)}) does not offset the investment. "
        f"Increase control effectiveness or reduce cost to achieve positive ROI."
    )

st.markdown(
    """
    ---
    **Key principle:** Cyber risk is a financial distribution, not a point estimate.
    Security investments should be evaluated the same way as any capital allocation decision —
    by expected return, downside exposure, and probability of loss.
    """
)
