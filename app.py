import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ======================
# PAGE CONFIG
# ======================

st.set_page_config(page_title="Cyber Risk Quant Tool", layout="wide")

st.title("🧠 Cyber Risk Quantification Dashboard")

# ======================
# SIDEBAR INPUTS
# ======================

st.sidebar.header("Model Inputs")

simulations = st.sidebar.slider("Simulations", 1000, 50000, 10000, step=1000)

control_reduction = st.sidebar.slider(
    "Control Effectiveness (%)",
    0.0,
    0.9,
    0.4,
    step=0.05
)

loss_mean = st.sidebar.slider("Loss Mean", 12.0, 16.0, 14.5)
loss_sigma = st.sidebar.slider("Loss Sigma", 0.3, 1.5, 0.7)

scenario = st.sidebar.selectbox(
    "Scenario",
    ["Ransomware", "Cloud Breach", "AI Misuse"]
)

# ======================
# CLIENT DATA MAPPING LAYER
# ======================

st.sidebar.header("Client Data Inputs (Optional)")

use_client_inputs = st.sidebar.checkbox("Use Client Data Mapping")

if use_client_inputs:

    st.sidebar.subheader("Incident Data")

    incidents_per_year = st.sidebar.slider("Incidents per Year", 0, 20, 3)

    st.sidebar.subheader("Financial Impact")

    downtime_cost_per_day = st.sidebar.slider("Downtime Cost per Day ($)", 10000, 1000000, 250000, step=10000)
    avg_days_downtime = st.sidebar.slider("Avg Downtime (Days)", 1, 10, 3)

    st.sidebar.subheader("Security Controls")

    mfa_coverage = st.sidebar.slider("MFA Coverage (%)", 0, 100, 50)
    edr_maturity = st.sidebar.selectbox("EDR Maturity", ["Low", "Medium", "High"])
    backup_maturity = st.sidebar.selectbox("Backup Maturity", ["Low", "Medium", "High"])

    # ======================
    # MAP TO MODEL VARIABLES
    # ======================

    # TEF mapping
    tef_min = max(0.1, incidents_per_year * 0.5)
    tef_mode = incidents_per_year
    tef_max = incidents_per_year * 2

    base_tef = (tef_min, tef_mode, tef_max)

    # Loss mapping
    base_loss = downtime_cost_per_day * avg_days_downtime

    loss_mean = np.log(base_loss)
    loss_sigma = 0.7  # default uncertainty

    # Control effectiveness mapping

    control_score = 0

    # MFA contribution
    control_score += (mfa_coverage / 100) * 0.4

    # EDR contribution
    if edr_maturity == "Low":
        control_score += 0.1
    elif edr_maturity == "Medium":
        control_score += 0.25
    else:
        control_score += 0.4

    # Backup contribution
    if backup_maturity == "Low":
        control_score += 0.1
    elif backup_maturity == "Medium":
        control_score += 0.25
    else:
        control_score += 0.4

    control_reduction = min(control_score, 0.9)

    st.sidebar.success("Client inputs mapped to model variables")

# ======================
# SCENARIO DEFINITIONS
# ======================

scenario_map = {
    "Ransomware": (1, 3, 6),
    "Cloud Breach": (0.5, 1, 2),
    "AI Misuse": (2, 4, 8),
}

base_tef = scenario_map[scenario]

# ======================
# MODEL FUNCTIONS
# ======================

def simulate_ale(tef_range, loss_mean, loss_sigma, n):
    tef = np.random.triangular(*tef_range, n)
    loss = np.random.lognormal(loss_mean, loss_sigma, n)
    return tef * loss

def apply_control(tef_range, reduction):
    return tuple(x * (1 - reduction) for x in tef_range)

# ======================
# RUN MODEL
# ======================

baseline = simulate_ale(base_tef, loss_mean, loss_sigma, simulations)

controlled_tef = apply_control(base_tef, control_reduction)
controlled = simulate_ale(controlled_tef, loss_mean, loss_sigma, simulations)

# ======================
# METRICS
# ======================

baseline_median = np.percentile(baseline, 50)
controlled_median = np.percentile(controlled, 50)

baseline_95 = np.percentile(baseline, 95)
controlled_95 = np.percentile(controlled, 95)

risk_reduction = baseline_median - controlled_median

CONTROL_COST = 1_000_000
roi = (risk_reduction - CONTROL_COST) / CONTROL_COST

# ======================
# DISPLAY METRICS
# ======================

col1, col2, col3 = st.columns(3)

col1.metric("Median Loss (Baseline)", f"${baseline_median:,.0f}")
col2.metric("Median Loss (Controlled)", f"${controlled_median:,.0f}")
col3.metric("Risk Reduction", f"${risk_reduction:,.0f}")

col4, col5 = st.columns(2)

col4.metric("95th Percentile (Baseline)", f"${baseline_95:,.0f}")
col5.metric("ROI", f"{roi:.2f}")

# ======================
# SHOW MAPPED INPUTS
# ======================

if use_client_inputs:
    st.subheader("Mapped Model Inputs")

    col1, col2, col3 = st.columns(3)

    col1.metric("TEF (min, mode, max)", f"{round(base_tef[0],1)}, {round(base_tef[1],1)}, {round(base_tef[2],1)}")
    col2.metric("Loss Mean ($)", f"${base_loss:,.0f}")
    col3.metric("Control Effectiveness", f"{control_reduction:.2f}")
    
# ======================
# HISTOGRAM
# ======================

st.subheader("Loss Distribution")

fig, ax = plt.subplots()
ax.hist(baseline, bins=50, alpha=0.5, label="Baseline")
ax.hist(controlled, bins=50, alpha=0.5, label="Controlled")
ax.legend()

st.pyplot(fig)

# ======================
# INSIGHT
# ======================

st.subheader("Key Insight")

if roi > 0:
    st.success("Control investment is financially justified.")
else:
    st.warning("Control investment may not be justified based on current assumptions.")
