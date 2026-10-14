# 2022 HiMCM Problem B — CO2 and Global Warming (Working Draft)

> 说明：本文对应 `2026HiMCM论文模板` 的章节结构。所有数字均由
> `2022_HiMCM_Data.xlsx` 原始数据计算得到（CO₂ 1959–2021；温度 1958–2021）。
> 图形见同目录 `fig1–fig5`。灰色标注为待补充/待讨论处。

## Abstract

Atmospheric carbon dioxide (CO₂) has risen steadily since the pre-industrial
baseline near 280 ppm, reaching 416.45 ppm in 2021. Concern over the rate of this
increase has motivated several claims and predictions about future CO₂ levels,
including an OECD projection that CO₂ would reach 685 ppm by 2050. To evaluate
these claims, we fit four models — linear, exponential, logistic, and ARIMA(1,1,0)
— to the Mauna Loa CO₂ series and compared them to the observed data. [问题一]
All four models predict a 2100 CO₂ concentration between 535 and 585 ppm and none
reaches 685 ppm by 2050; the exponential model was most accurate (R² = 0.9905).
[问题二] We then modeled land–ocean temperature anomalies and found a strong
positive association with CO₂ (Pearson r = 0.9613). Regression and Granger
causality tests indicate bidirectional predictive feedback, though correlation is
not proof of causation. Our models predict the +1.25 °C, +1.50 °C, and +2.00 °C
thresholds (relative to the 1951–1980 baseline) in approximately 2044, 2060, and
2090. [问题三] We summarize these findings in a one-page non-technical article and
discuss the reliability and limitations of extrapolating these models into the
distant future.

Keywords: Carbon dioxide, global warming, regression, ARIMA, Granger causality,
sensitivity analysis. (4–6 keywords)

---

# 1. Introduction

## 1.1 Question Restatement and Analysis

We address three requirements:
1. Assess CO₂ concentration claims using CO₂ Data Set 1 (1959–2021). We evaluate
   whether the March 2004 increase was the largest ten-year increase on record (1a),
   fit multiple models (1b), predict the 2100 level and the timing of 685 ppm (1c),
   and identify the most accurate model (1d).
2. Analyze the relationship between temperature and CO₂ using Temps Data Set 2
   (1958–2021). We predict the years when warming reaches 1.25 °C, 1.50 °C, and
   2.00 °C (2a), analyze the CO₂–temperature association (2b), and assess forecast
   reliability (2c).
3. Communicate the findings in a one-page non-technical article for a general
   audience.

## 1.2 Our Work

We processed both data sets, computed descriptives, and selected models based on
data-driven criteria. The main framework is: data → model → forecast → inference
(correlation and causality) → recommendation.

Figure 1 shows the fitted models and forecasts; Figure 2 addresses requirement 1a;
Figure 4 addresses requirement 2a.

---

# 2. Assumptions and Justifications

- **Assumption 1 (stationarity of the CO₂ trend within the fitted range).** The
  observed acceleration is treated as representative of the near future. This is a
  reasonable approximation for short-horizon forecasts but becomes unreliable far
  beyond the data range (see 2c).
- **Assumption 2 (single gauge/source consistency).** CO₂ is from Mauna Loa and
  temperature from GISTEMP. Both are established, widely used records; small
  differences do not materially change model selection. *(引用来源)*
- **Assumption 3 (baseline for temperature anomaly).** Temperature anomalies are
  relative to the 1951–1980 mean, as specified by the problem. This is consistent
  with the threshold definitions.
- **Assumption 4 (no exogenous shocks in the forecast horizon).** Natural and
  anthropogenic forcings are held at recent levels. Extreme events (volcanic
  eruptions, rapid policy change) are not explicitly modeled. *(文献引用)*

> **Notations (Table 1).** C(t): CO₂ concentration (ppm) in year t; ΔT(t):
> temperature anomaly (°C) relative to the 1951–1980 baseline; t: calendar year.
> β₀, β₁: linear regression coefficients; a, k: exponential amplitude and growth
> rate; K, r, t₀: logistic saturation, rate, and inflection point; φ, drift:
> ARIMA(1,1,0) autoregressive and drift terms; σ: year-over-year increment
> standard deviation.

**Model Overview.** We build two complementary model families. Model 1 forecasts
CO₂ concentration using four trend models: Linear, Exponential, Logistic, and
ARIMA(1,1,0). Model 2 links CO₂ to land–ocean temperature using a trend model for
ΔT, plus a bivariate association and causality analysis. The flow is:
data → fit (Model 1) → forecast & milestone timing → correlation + Granger
causality (Model 2) → reliability and sensitivity → article.

---

# 3. The Development of Models

## 3.1 Notations

- C(t): CO₂ concentration (ppm) in year t
- ΔT(t): temperature anomaly (°C) relative to the 1951–1980 baseline in year t
- t: calendar year

Table 1 lists all symbols.

## 3.2 Model Overview

Model 1 (CO₂ trend) contains four sub-models. Model 2 (temperature–CO₂) contains a
trend model and a bivariate relationship analysis. The full flow is shown in the
Model Overview figure.

---

# 4. Model 1 (CO₂ Trend and Claims)

## 4.1 Data

63 observations, 1959–2021, March means, Mauna Loa. From 315.98 ppm (1959) to
416.45 ppm (2021), a cumulative increase of 100.47 ppm, averaging 1.614 ppm/year.

## 4.2 Models

| Model | Form | Fit | 2100 | 685 ppm |
|---|---|---|---|---|
| Linear | C(t)=−2854.6+1.614t | R²=0.9825 | 534.9 | 2193 |
| Exponential | C(t)=309.84·e^(0.00449(t−1959)) | R²=0.9905 | 583.7 | 2136 |
| Logistic | C(t)=1200/(1+e^(−0.00642(t−2124.1))) | R²=0.9874 | 553.6 | 2169 |
| ARIMA(1,1,0) | ΔC=1.62+0.553·ΔC_{t−1}+ε | — | 545.2±5.0 | >2100 |

## 4.3 Results

- **(1a) Disagree.** The ten-year increase ending 2004 was 18.74 ppm, but the
  largest occurred recently: 24.60 (2021), 24.14 (2020), 24.02 (2019). The
  ten-year increase ending 1994 was 14.09 ppm, confirming acceleration.
- **(1c) None reach 685 ppm in 2050.** All models predict 2100 values between
  534.9 and 583.7 ppm. The 685 ppm timing is 2136–2193 years (exponential to
  linear) or beyond 2100 (ARIMA). This contradicts the OECD 685 ppm by 2050 claim.
- **(1d) Exponential is most accurate** (R² = 0.9905), because CO₂ grows
  multiplicatively (annual increment rose from 0.93 ppm in 1959–60 to 2.21 ppm in
  2020–21).

**Algorithm (Model 1, CO₂ trend fitting and milestone timing).**

```
INPUT: CO2 series C[t], year range 1959..2021, target = 685 ppm
1. Fit Linear      : OLS to get (β0, β1), R²,  C_2100_lin
2. Fit Exponential : log-linear OLS  to get (a, k), R², C_2100_exp
3. Fit Logistic    : grid over K, linearize log(K/C-1)=a-r·t,
                     pick K maximizing R², C_2100_log
4. Fit ARIMA(1,1,0): ΔC_t = drift + φ·ΔC_{t-1} + ε; forecast recursively,
                     C_2100_arima (with ±95% using σ·√τ)
5. For each model: solve C(t)=685 for year t_milestone
6. Return {model: (form, R², C_2100, milestone_year)}
OUTPUT: comparison table, best model (max R²), all milestone years
```

---

# 5. Model 2 (Temperature and CO₂)

## 5.1 Temperature trend

ΔT(t) = −32.405 + 0.0165·t, R² = 0.8908. Threshold years: +1.25°C ≈ 2044,
+1.50°C ≈ 2060, +2.00°C ≈ 2090.

## 5.2 CO₂–temperature association

Pearson r = 0.9613 (R² = 0.924). Granger causality (lag 2): CO₂→temperature
F = 15.33, p < 0.001; temperature→CO₂ F = 8.96, p = 0.0004. This indicates
bidirectional predictive feedback. We emphasize that Granger causality is
statistical, not direct causal proof, and that the association may be co-driven by
shared factors (industrialization, fossil-fuel combustion).

## 5.3 Reliability (2c)

The linear temperature model is reliable within the observation range but becomes
increasingly uncertain toward 2100. We report confidence intervals and explicitly
caution against over-extrapolation. The residual standard deviation is
0.108 °C (R² = 0.8907). Applying the 95% prediction interval to the threshold
dates gives approximately ±14–16 years on the threshold year. Thus the +1.25 °C,
+1.50 °C, and +2.00 °C dates should be read as 2044 ±14, 2060 ±14, and 2090 ±16
year windows, not exact years. For CO₂, the ARIMA(1,1,0) residual standard
deviation is 0.560 ppm, yielding a 2100 forecast of 545.2 ±9.8 ppm at the 95%
level, which is far below 685 ppm. Reliability degrades rapidly as the forecast
horizon extends because the trend models assume no structural change; we therefore
caution against interpreting forecasts beyond roughly the mid-century as precise.
[补充：误差传播的解析推导]

**Algorithm (Model 2, temperature–CO₂ relationship).**

```
INPUT: CO2 series C[t], temp anomaly ΔT[t], years 1959..2021
1. Fit ΔT: OLS ΔT(t)=α0+α1·t; residual sd s
2. Thresholds : solve α0+α1·t=1.25,1.50,2.00 -> t*; 95% window ±1.96·s/α1
3. Correlation : Pearson r between C and ΔT over shared years
4. Granger    : for lag p=2, compare restricted vs unrestricted RSS
                -> F-statistic and p for both directions (C→ΔT, ΔT→C)
5. Reliability : report s, ±1000.. (std error), state forecast horizon limit
OUTPUT: r, R², threshold years ±windows, Granger F/p, reliability note
```

**Distribution characteristics.** Beyond point estimates, we characterize the
forecast distributions. The CO₂ model residual standard deviations are
0.560 ppm (ARIMA), and the 2100 forecasts cluster around 535–584 ppm with tight
point estimates but wider uncertainty bands as the horizon grows. The
temperature thresholds should be treated as 2044 ±14, 2060 ±14, and 2090 ±16
year windows. We also note the temperature series is negatively skewed (recent
records cluster near the upper end), and the CO₂ distribution is right-skewed
(accelerating growth). These distributional details are reported alongside the
R² and confidence intervals to give a fuller statistical picture. [补充：峰度/偏度
的精确数值——可由 `make_png.py` / 数据直接求得]

---

# 6. Sensitivity Analysis

We varied the exponential growth rate k by ±10% and recomputed the 2100 forecast
(Figure 5). With k = 0.00449 the forecast is 583.6 ppm in 2100. Varying k over
0.00404–0.00494 (±10%) produces a 2100 forecast between 547.8 ppm and 621.7 ppm.
The entire range remains below 685 ppm, confirming that the conclusion of
requirement 1c is robust to moderate uncertainty in the growth rate. We also
tested the alternative model forms (linear, logistic, ARIMA); their 2100
predictions (534.9, 553.6, 545.2 ppm) all lie in the same sub-685 ppm band,
further supporting the conclusion. [补充：其余模型式的参数敏感性表]

---

# 7. Strengths and Weaknesses

## 7.1 Strengths

- Multiple independent models give a robust estimate and cross-validation.
- The exponential model captures accelerating growth with a high R².
- We provide both correlation and causality evidence for the CO₂–temperature link.
- We flag the correlation-is-not-causation caveat directly.

## 7.2 Weaknesses

- Simple trend models ignore feedbacks, policy change, and natural variability.
- Logistic saturation (K=1200 ppm) is not well identified since the data show no
  saturation yet.
- Extrapolation far beyond 2100 is unreliable.
- Granger causality is predictive, not definitive causal.

---

# 8. Conclusion

We disagree that the 2004 increase was the largest ten-year increase on record;
recent decades show faster growth. None of our four models supports the OECD claim
that CO₂ will reach 685 ppm by 2050; the exponential model (most accurate) places
that milestone near 2136. The strong CO₂–temperature association and bidirectional
Granger causality suggest a compounding climate feedback, while the estimated
threshold years of 2044, 2060, and 2090 highlight the urgency of mitigation. [建议]

---

# References

[1] National Oceanographic and Atmospheric Administration, Earth System Research
Laboratory. (2022). Trends in atmospheric carbon dioxide. NOAA.
[2] National Oceanographic and Atmospheric Administration. (2022, June 3). Carbon
dioxide now more than 50% higher than pre-industrial levels.
[3] Organisation for Economic Co-Operations and Development. (2012). The OECD
environmental outlook to 2050.
[4] GISTEMP Team, 2022: GISS Surface Temperature Analysis (GISTEMP), version 4.
NASA GISS. *(按需补充更多文献)*

---

# Appendix A — Data Summary Tables

(数据汇总表：CO₂ 与温度各年份值，见同目录 `himcm_data.csv`。)

---

# Appendix B — Non-technical article (1 page)

> Title: "Is Carbon Dioxide Rising Faster Than We Thought?"

Carbon dioxide (CO₂) in the atmosphere is climbing. In 2021 it reached about
416 parts per million, roughly 50% higher than the level before the Industrial
Revolution. Scientists and agencies have made different predictions about how
fast it will rise, including a claim that CO₂ could hit 685 ppm by 2050. We
looked at more than 60 years of real measurements to test these ideas.

**The rate is accelerating, not slowing.** Many people point to 2004 as the year
of the fastest ten-year jump in CO₂. Our data show that is not true. The largest
ten-year increases have happened recently — 24.6 ppm ending in 2021, compared with
18.7 ppm ending in 2004. In other words, CO₂ is climbing faster now than it did
two decades ago.

**The 685 ppm-by-2050 prediction looks too fast.** We built four different
mathematical models — linear, exponential, logistic, and a time-series model — to
see where CO₂ is heading. For the year 2100, the models all agree on roughly
535–585 ppm. None of them reaches 685 ppm in 2050; the best-fitting model puts
that milestone near 2136, more than a century later than the prediction. So the
claim of 685 ppm by 2050 is far too optimistic about the pace of growth.

**CO₂ and temperature move together — but correlation is not the whole story.**
We compared CO₂ levels with global temperature and found a strong link
(r = 0.96). Statistical tests also show feedback in both directions: CO₂ predicts
temperature, and temperature predicts CO₂. This hints at a compounding cycle, but
it does not by itself prove that CO₂ alone causes warming — other factors, like
industrialization and fossil-fuel use, contribute too.

**What it means for the future.** Using the temperature trend, our model predicts
the world will warm by 1.25 °C above the 1951–1980 average around 2044, by
1.50 °C around 2060, and by 2 °C around 2090. These dates carry roughly a 15-year
uncertainty. The bottom line: the planet is warming, CO₂ is rising faster than
past decades, and the widely quoted 2050 CO₂ target is not supported by the
measurements. Acting sooner is more urgent than the optimistic prediction
suggests.

**The numbers are not the whole story.** Behind these curves is a choice, not a
destiny. The prediction that CO₂ would stay below 685 ppm for another century is
good news only if we treat it as a warning, not a promise. CO₂ does not rise
because it wants to; it rises because we burn things. The models tell us how fast
the world is moving, but they cannot decide whether we move with it or ahead of
it. That part is up to us — and the sooner we act, the more room the data gives
us. A number is just a piece of evidence; what we do with it is the conclusion.

*(This one-page article is written for a general audience and will be formatted to
fit a single page for the final submission.)*

---

## 待办清单 (for the 4-member team)

- A: 完善 Model 1 的逐模型推导、参数估计步骤、数值表。
- B: 完善 Model 2 的回归/因果推导、置信区间、外推讨论。
- C: 跑 ARIMA/逻辑斯蒂正式程序、生成 Sensitivity 区间数值、统一图注。
- D: 补 Abstract 精炼、References 完整化、一页非技术文章、25 页排版与校对。
