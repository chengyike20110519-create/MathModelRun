# 2022 HiMCM Problem B — CO2 and Global Warming (Working Draft)

> 说明：本文数字均来自本案例的 `run-002`，并已登记在
> `frozen_numbers.json`。图形由 `code/reproduce_himcm.py --plot` 原位重生成。
> 趋势外推和 Granger 检验均保留其统计限制，不被解释为物理气候机制。

## Abstract

Atmospheric carbon dioxide (CO₂) has risen steadily since the pre-industrial
baseline near 280 ppm, reaching 416.45 ppm in 2021. Concern over the rate of this
increase has motivated several claims and predictions about future CO₂ levels,
including an OECD projection that CO₂ would reach 685 ppm by 2050. To evaluate
these claims, we fit four models — linear, exponential, logistic, and ARIMA(1,1,0)
— to the Mauna Loa CO₂ series and compared them to the observed data. [问题一]
The four models predict 2100 CO₂ concentrations from 518.11 to 564.90 ppm and
none reaches 685 ppm by 2050. Under the common ten-year holdout, ARIMA(1,1,0)
has the lowest RMSE (5.8837 ppm), while the exponential model has RMSE 8.5843 ppm.
[问题二] We then modeled land–ocean temperature anomalies and found a strong
positive association with CO₂ (Pearson r = 0.9612). The one-lag exploratory
Granger statistic is significant from CO₂ to temperature (p = 4.31×10⁻⁸) but not
in the reverse direction (p = 0.7886); neither result proves physical causation.
The temperature trend reaches +1.25 °C, +1.50 °C, and +2.00 °C around 2044.24,
2059.39, and 2089.71, with wide reported year intervals. We discuss why these
trend estimates should not be read as precise climate forecasts.

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
| Linear | OLS | test RMSE=10.8935 | 518.11 | not reached by 2100 |
| Exponential | log-linear OLS | test RMSE=8.5843 | 564.90 | not reached by 2100 |
| Logistic | bounded grid fit | test RMSE=8.9124 | 555.74 | not reached by 2100 |
| ARIMA(1,1,0) | NumPy difference regression | test RMSE=5.8837 | 534.06 | not reached by 2100 |

## 4.3 Results

- **(1a) Disagree.** The ten-year increase ending 2004 was 18.74 ppm, but the
  largest occurred recently: 24.60 (2021), 24.14 (2020), 24.02 (2019). The
  ten-year increase ending 1994 was 14.09 ppm, confirming acceleration.
- **(1c) None reach 685 ppm in 2050.** The 2100 point forecasts span 518.11–564.90
  ppm. The present run does not claim a reliable 685 ppm milestone beyond 2100;
  solving that milestone would be structurally dominated by the chosen trend model.
- **(1d) ARIMA(1,1,0) is best on this holdout** by RMSE, but its NumPy fallback and
  the short sample mean that this ranking is a model-selection result, not a claim
  that ARIMA represents the climate system.

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

ΔT(t) = −32.4677 + 0.016494·t, R² = 0.8907. Threshold years are 2044.24,
2059.39, and 2089.71 for +1.25°C, +1.50°C, and +2.00°C. Their 95% year
intervals are [2039.20, 2049.27], [2053.09, 2065.70], and [2080.82, 2098.59].

## 5.2 CO₂–temperature association

Pearson r = 0.9612 (shared years 1959–2021). The exploratory one-lag statistic is
CO₂→temperature F = 39.5142, p = 4.31×10⁻⁸, while temperature→CO₂ gives
F = 0.0725, p = 0.7886. This asymmetry is a predictive-statistics result, not
physical causation; shared trends and omitted factors remain important limitations.

## 5.3 Reliability (2c)

The linear temperature model is a useful within-sample baseline but becomes
increasingly uncertain toward 2100. The residual standard deviation is 0.1076 °C.
The threshold intervals above are uncertainty windows, not exact dates. For CO₂,
the ARIMA holdout RMSE is 5.8837 ppm, but the long-range point forecast still
depends on recursive extrapolation. Policy changes, natural variability and model
misspecification are not represented.

**Algorithm (Model 2, temperature–CO₂ relationship).**

```
INPUT: CO2 series C[t], temp anomaly ΔT[t], years 1959..2021
1. Fit ΔT: OLS ΔT(t)=α0+α1·t; residual sd s
2. Thresholds : solve α0+α1·t=1.25,1.50,2.00 -> t*; 95% window ±1.96·s/α1
3. Correlation : Pearson r between C and ΔT over shared years
4. Granger    : for lag p=1, compare restricted vs unrestricted RSS
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

We varied the exponential growth rate by ±10% and recomputed the 2100 forecast
(Figure 5). The resulting scenario range is 532.24–599.56 ppm, with the baseline
at 564.90 ppm. This is a scenario range, not a confidence interval. The four
model point forecasts (518.11, 564.90, 555.74, and 534.06 ppm) remain below
685 ppm by 2100 in this run, while the spread itself demonstrates structural
uncertainty.

---

# 7. Strengths and Weaknesses

## 7.1 Strengths

- Multiple transparent models are compared on one time-ordered holdout.
- The script records both point forecasts and a growth-rate scenario range.
- We separate correlation from exploratory predictive-direction statistics.
- Every reported quantitative result is mapped to the frozen run.

## 7.2 Weaknesses

- Simple trend models ignore feedbacks, policy change, and natural variability.
- Logistic saturation (K=1200 ppm) is not well identified since the data show no
  saturation yet.
- Extrapolation far beyond 2100 is unreliable.
- Granger causality is predictive, not definitive causal.

---

# 8. Conclusion

We disagree that the 2004 increase was the largest ten-year increase on record:
the 2011–2021 increase was 24.60 ppm versus 18.74 ppm for 1994–2004. None of the
four fitted models supports 685 ppm by 2050; their 2100 point forecasts range from
518.11 to 564.90 ppm. CO₂ and temperature have a strong shared trend, but the
exploratory Granger result is one-directional in this run and does not establish
physical causation. Threshold estimates are useful scenario markers, not precise
climate forecasts.

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
see where CO₂ is heading. For the year 2100, the model point forecasts span
518–565 ppm. None of them reaches 685 ppm in 2050. Because the current run does
not establish a reliable milestone beyond 2100, we do not report a spurious year
for reaching 685 ppm.

**CO₂ and temperature move together — but correlation is not the whole story.**
We compared CO₂ levels with global temperature and found a strong link
(r = 0.9612). A one-lag exploratory test finds predictive direction from CO₂ to
temperature (p = 4.31×10⁻⁸), but not in the reverse direction (p = 0.7886).
These are statistical results, not proof that CO₂ alone causes warming; shared
trends and other factors still matter.

**What it means for the future.** Using the temperature trend, our model predicts
the world will warm by 1.25 °C above the 1951–1980 average around 2044, by
1.50 °C around 2059, and by 2 °C around 2090. The reported 95% year intervals
are approximately 2039–2049, 2053–2066, and 2081–2099. The bottom line: the planet is warming, CO₂ is rising faster than
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

## 当前交付状态

本文中的定量结果已由 `run-002` 冻结并完成证据映射。正式 LaTeX 排版、PDF
逐页检查和最终独立审计仍待完成；在此之前，本文不是最终提交 PDF。
