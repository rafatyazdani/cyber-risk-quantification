# Cyber Risk Quantification & Financial Modeling

## Overview

This project models cybersecurity risk in financial terms using probabilistic simulation and scenario-based analysis. It translates technical cyber risk into expected financial exposure and investment decision metrics.

The goal is to bridge the gap between cybersecurity operations and capital allocation decision-making.

---

## Why This Matters

Most cybersecurity discussions focus on:
- number of incidents
- compliance posture
- qualitative risk ratings

This project reframes cyber risk as a financial distribution of potential losses under uncertainty

This enables decision-making based on:
- expected annual loss
- tail risk exposure
- ROI of security investments

---

## Methodology

The analysis is built on three core components:

### 1. Loss Modeling (FAIR-inspired)
- Threat Event Frequency (TEF)
- Loss Magnitude (LM)
- Monte Carlo simulation (10,000+ iterations)

### 2. Scenario Analysis
Models multiple threat types:
- Ransomware
- Cloud Data Breach
- AI Misuse

Each scenario has unique frequency and severity assumptions.

### 3. Control ROI Analysis
Evaluates security investment impact by:
- Reducing expected loss
- Measuring financial benefit of controls
- Calculating ROI
- Performing sensitivity analysis

---

## Key Outputs

### Annualized Loss Exposure (ALE)
- Median loss
- 90th percentile loss
- 95th percentile (tail risk)

### Scenario Insights
- Ransomware drives highest tail risk exposure
- Cloud breaches have lower frequency but higher severity
- AI misuse shows higher variability

### Control Effectiveness
- Example result: ~$2.5M annual risk reduction
- Example ROI: ~1.5x under baseline assumptions

---

## Key Insight

Cybersecurity should be evaluated as a financial risk problem, not just a technical control problem.

This means:
- Risks are distributions, not single values
- Controls should be evaluated by economic impact
- Investment decisions should be based on expected value and ROI

---

## Architecture Overview

```mermaid
flowchart LR
A[Scenario Inputs] --> B[Monte Carlo Engine]
B --> C[Loss Distribution Modeling]
C --> D[Financial Risk Outputs]
D --> E[Control ROI Analysis]
E --> F[Decision Insights]

Components
Scenario Inputs: TEF assumptions and loss distributions
Monte Carlo Engine: Simulates thousands of possible outcomes
Loss Distribution Modeling: Produces ALE and percentile outputs
Financial Risk Outputs: Quantifies exposure (median, tail risk)
Control ROI Analysis: Evaluates financial impact of controls
Decision Insights: Converts outputs into investment decisions

Project Structure
notebooks/
  01_fair_loss_model.ipynb
  02_scenario_analysis.ipynb
  03_control_roi_analysis.ipynb

outputs/
  (generated analysis files)

README.md

How to Run This Project
1. Clone repository
git clone https://github.com/rafatyazdani/cyber-risk-quantification.git
cd cyber-risk-quantification

2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

3. Install dependencies
pip install numpy pandas matplotlib jupyter

4. Launch Jupyter
jupyter notebook

5. Run notebooks in order
01_fair_loss_model.ipynb
02_scenario_analysis.ipynb
03_control_roi_analysis.ipynb

Executive Interpretation

This model is designed to support risk-informed capital allocation decisions.

Rather than treating cybersecurity as a compliance function, it:
Quantifies uncertainty in financial terms
Highlights tail-risk exposure
Evaluates controls based on economic impact

This enables leadership to:
Compare security investments like financial assets
Prioritize controls based on ROI
Understand downside exposure in monetary terms