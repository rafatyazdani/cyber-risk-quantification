# Cyber Risk Quantification & Financial Modeling

## Overview

This project models cybersecurity risk in financial terms using probabilistic simulation and scenario-based analysis. It translates technical cyber risk into **expected financial exposure and investment decision metrics**.

The goal is to bridge the gap between cybersecurity operations and **capital allocation decision-making**.

---

## Why This Matters

Most cybersecurity programs measure:
- number of incidents
- compliance posture
- qualitative risk ratings

This project reframes cyber risk as:
> a financial distribution of potential losses

allowing leadership to evaluate:
- expected annual loss
- tail risk exposure
- ROI of security investments

---

## Methodology

The analysis is built on three components:

### 1. Loss Modeling (FAIR-inspired)
- Threat Event Frequency (TEF)
- Loss Magnitude (LM)
- Monte Carlo simulation

### 2. Scenario Analysis
Models multiple threat types:
- Ransomware
- Cloud Breach
- AI Misuse

Each scenario has distinct frequency and severity distributions.

### 3. Control ROI Analysis
Evaluates the financial impact of security controls:
- Reduction in expected loss
- ROI of investment
- Sensitivity to control effectiveness

---

## Key Outputs

### Annualized Loss Exposure (ALE)
- Median, 90th, 95th percentile losses
- Full loss distribution via Monte Carlo simulation

### Scenario Insights
- Ransomware drives highest tail risk exposure
- Cloud breaches exhibit lower frequency but higher severity
- AI misuse shows higher variability in outcomes

### Control Effectiveness
- Risk reduction quantified in dollar terms
- Example: ~$2.5M annual risk reduction observed
- ROI approximately 1.5x under baseline assumptions

---

## Key Insight

Cybersecurity investments should not be evaluated as cost centers.

They should be evaluated as:
> financial risk reduction instruments

This enables prioritization based on:
- expected loss reduction
- tail risk mitigation
- capital efficiency (ROI)

---

## Tools Used
- Python
- NumPy
- Pandas
- Matplotlib
- Monte Carlo simulation

---

## Potential Applications

- Security investment prioritization
- Board-level risk reporting
- Cyber insurance modeling
- Enterprise risk quantification frameworks