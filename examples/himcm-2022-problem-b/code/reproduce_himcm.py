#!/usr/bin/env python3
"""Reproduce the transparent Q1/Q2 CO2 and temperature experiments.

This first pass intentionally avoids optional machine-learning packages. It
produces auditable metrics and figures from the case CSV using NumPy and
Matplotlib only.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


def read_series(path: Path, series_type: str) -> tuple[np.ndarray, np.ndarray]:
    years: list[int] = []
    values: list[float] = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row.get("type") == series_type:
                years.append(int(row["year"]))
                values.append(float(row["value"]))
    if len(years) < 3:
        raise ValueError(f"Need at least three {series_type} observations")
    order = np.argsort(years)
    return np.asarray(years, dtype=float)[order], np.asarray(values, dtype=float)[order]


def fit_linear(years: np.ndarray, values: np.ndarray) -> tuple[float, float]:
    slope, intercept = np.polyfit(years, values, 1)
    return float(intercept), float(slope)


def fit_exponential(years: np.ndarray, values: np.ndarray) -> tuple[float, float]:
    if np.any(values <= 0):
        raise ValueError("Exponential fit requires positive values")
    log_intercept, rate = np.polyfit(years - years[0], np.log(values), 1)[::-1]
    return float(math.exp(log_intercept)), float(rate)


def linear_predict(params: tuple[float, float], years: np.ndarray) -> np.ndarray:
    intercept, slope = params
    return intercept + slope * years


def exponential_predict(params: tuple[float, float], years: np.ndarray, origin: float) -> np.ndarray:
    amplitude, rate = params
    return amplitude * np.exp(rate * (years - origin))


def fit_logistic(years: np.ndarray, values: np.ndarray) -> tuple[float, float, float]:
    """Fit a bounded logistic curve by a transparent K grid and linearization."""
    origin = float(years[0])
    best: tuple[float, float, float, float] | None = None
    for carrying in np.linspace(float(np.max(values) * 1.05), float(np.max(values) * 8), 300):
        transformed = carrying / values - 1
        if np.any(transformed <= 0):
            continue
        intercept, slope = np.polyfit(years - origin, np.log(transformed), 1)[::-1]
        rate = -float(slope)
        midpoint = origin + float(intercept) / rate if rate else float(origin)
        predicted = carrying / (1 + np.exp(-rate * (years - midpoint)))
        error = float(np.mean((values - predicted) ** 2))
        if best is None or error < best[0]:
            best = (error, float(carrying), rate, midpoint)
    if best is None:
        raise ValueError("Unable to fit logistic model")
    return best[1], best[2], best[3]


def logistic_predict(params: tuple[float, float, float], years: np.ndarray) -> np.ndarray:
    carrying, rate, midpoint = params
    return carrying / (1 + np.exp(-rate * (years - midpoint)))


def fit_arima110(values: np.ndarray) -> tuple[float, float, float]:
    """Fit ARIMA(1,1,0) as an AR(1) regression on first differences."""
    differences = np.diff(values)
    if len(differences) < 3:
        raise ValueError("ARIMA(1,1,0) requires at least four observations")
    design = np.column_stack([np.ones(len(differences) - 1), differences[:-1]])
    drift, phi = np.linalg.lstsq(design, differences[1:], rcond=None)[0]
    residuals = differences[1:] - design @ np.asarray([drift, phi])
    residual_sd = float(np.std(residuals, ddof=2)) if len(residuals) > 2 else 0.0
    return float(drift), float(phi), residual_sd


def arima_predict(params: tuple[float, float, float], history: np.ndarray, count: int) -> np.ndarray:
    """Recursively forecast an ARIMA(1,1,0) model from the last observed value."""
    drift, phi, _ = params
    last_value = float(history[-1])
    last_difference = float(history[-1] - history[-2])
    predictions = []
    for _ in range(count):
        next_difference = drift + phi * last_difference
        last_value += next_difference
        predictions.append(last_value)
        last_difference = next_difference
    return np.asarray(predictions, dtype=float)


def granger_f_test(cause: np.ndarray, effect: np.ndarray, lag: int = 1) -> dict[str, float | int | None]:
    """Test whether lagged cause values add explanatory power for the effect."""
    if len(cause) != len(effect) or len(effect) <= 2 * lag + 2:
        raise ValueError("Granger test requires aligned series with enough observations")
    y = effect[lag:]
    effect_lags = np.column_stack([effect[lag - offset - 1 : -offset - 1] for offset in range(lag)])
    cause_lags = np.column_stack([cause[lag - offset - 1 : -offset - 1] for offset in range(lag)])
    restricted_design = np.column_stack([np.ones(len(y)), effect_lags])
    unrestricted_design = np.column_stack([restricted_design, cause_lags])
    restricted_residuals = y - restricted_design @ np.linalg.lstsq(restricted_design, y, rcond=None)[0]
    unrestricted_residuals = y - unrestricted_design @ np.linalg.lstsq(unrestricted_design, y, rcond=None)[0]
    rss_restricted = float(np.sum(restricted_residuals**2))
    rss_unrestricted = float(np.sum(unrestricted_residuals**2))
    numerator_df = lag
    denominator_df = len(y) - unrestricted_design.shape[1]
    f_statistic = ((rss_restricted - rss_unrestricted) / numerator_df) / (rss_unrestricted / denominator_df)
    p_value = regularized_beta(denominator_df / (denominator_df + max(0.0, f_statistic * numerator_df)), denominator_df / 2.0, numerator_df / 2.0)
    return {
        "lag": lag,
        "observations": int(len(y)),
        "f_statistic": float(max(0.0, f_statistic)),
        "numerator_df": numerator_df,
        "denominator_df": denominator_df,
        "p_value": float(p_value),
        "p_value_status": "computed_by_local_incomplete_beta",
    }


def metrics(actual: np.ndarray, predicted: np.ndarray) -> dict[str, float]:
    residual = actual - predicted
    ss_res = float(np.sum(residual**2))
    ss_tot = float(np.sum((actual - np.mean(actual)) ** 2))
    return {
        "rmse": float(np.sqrt(np.mean(residual**2))),
        "mae": float(np.mean(np.abs(residual))),
        "r2": float(1 - ss_res / ss_tot) if ss_tot else 0.0,
        "residual_sd": float(np.std(residual, ddof=1)) if len(residual) > 1 else 0.0,
    }


def regularized_beta(x: float, a: float, b: float) -> float:
    """Evaluate the regularized incomplete beta using a continued fraction."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    log_beta = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)

    def fraction(value: float, first: float, second: float) -> float:
        tiny = 1e-300
        qab, qap, qam = first + second, first + 1.0, first - 1.0
        c = 1.0
        d = 1.0 - qab * value / qap
        d = math.copysign(max(abs(d), tiny), d)
        d = 1.0 / d
        result = d
        for index in range(1, 201):
            m = float(index)
            m2 = 2.0 * m
            aa = m * (second - m) * value / ((qam + m2) * (first + m2))
            d = math.copysign(max(abs(1.0 + aa * d), tiny), 1.0 + aa * d)
            c = math.copysign(max(abs(1.0 + aa / c), tiny), 1.0 + aa / c)
            d = 1.0 / d
            result *= d * c
            aa = -(first + m) * (qab + m) * value / ((first + m2) * (qap + m2))
            d = math.copysign(max(abs(1.0 + aa * d), tiny), 1.0 + aa * d)
            c = math.copysign(max(abs(1.0 + aa / c), tiny), 1.0 + aa / c)
            d = 1.0 / d
            delta = d * c
            result *= delta
            if abs(delta - 1.0) < 3e-14:
                break
        return result

    front = math.exp(a * math.log(x) + b * math.log1p(-x) - log_beta) / a
    if x < (a + 1.0) / (a + b + 2.0):
        return front * fraction(x, a, b)
    return 1.0 - math.exp(b * math.log1p(-x) + a * math.log(x) - log_beta) / b * fraction(1.0 - x, b, a)


def rolling_increases(years: np.ndarray, values: np.ndarray, window: int = 10) -> list[dict[str, float | int]]:
    by_year = {int(year): float(value) for year, value in zip(years, values)}
    output = []
    for end_year in sorted(by_year):
        start_year = end_year - window
        if start_year in by_year:
            output.append({"start_year": start_year, "end_year": end_year, "increase": by_year[end_year] - by_year[start_year]})
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Reproduce HiMCM 2022 Problem B Q1 PoC")
    parser.add_argument("project", nargs="?", default=Path(__file__).resolve().parents[1], type=Path)
    parser.add_argument("--plot", action="store_true", help="also render the PoC figure")
    args = parser.parse_args()
    root = args.project.resolve()
    input_path = root / "problem_files" / "himcm_data.csv"
    run_dir = root / "results" / "runs" / "run-002"
    figure_dir = root / "figures"
    run_dir.mkdir(parents=True, exist_ok=True)
    figure_dir.mkdir(parents=True, exist_ok=True)

    years, values = read_series(input_path, "CO2")
    temp_years, temp_values = read_series(input_path, "TEMP")
    train_size = len(years) - 10
    train_years, train_values = years[:train_size], values[:train_size]
    test_years, test_values = years[train_size:], values[train_size:]
    linear_params = fit_linear(train_years, train_values)
    exponential_params = fit_exponential(train_years, train_values)
    logistic_params = fit_logistic(train_years, train_values)
    arima_params = fit_arima110(train_values)
    linear_test = linear_predict(linear_params, test_years)
    exponential_test = exponential_predict(exponential_params, test_years, train_years[0])
    logistic_test = logistic_predict(logistic_params, test_years)
    arima_test = arima_predict(arima_params, train_values, len(test_values))
    linear_all = linear_predict(linear_params, years)
    exponential_all = exponential_predict(exponential_params, years, train_years[0])
    logistic_all = logistic_predict(logistic_params, years)
    forecast_years = np.arange(2022, 2101, dtype=float)
    linear_forecast = linear_predict(linear_params, forecast_years)
    exponential_forecast = exponential_predict(exponential_params, forecast_years, train_years[0])
    logistic_forecast = logistic_predict(logistic_params, forecast_years)
    arima_forecast = arima_predict(arima_params, values, len(forecast_years))

    def milestone(prediction: np.ndarray, target: float) -> float | None:
        hits = forecast_years[prediction >= target]
        return float(hits[0]) if len(hits) else None

    rolling = rolling_increases(years, values)
    maximum = max(rolling, key=lambda item: float(item["increase"]))
    target = 685.0
    shared_years = [int(year) for year in sorted(set(years.astype(int)) & set(temp_years.astype(int)))]
    co2_by_year = {int(year): float(value) for year, value in zip(years, values)}
    temp_by_year = {int(year): float(value) for year, value in zip(temp_years, temp_values)}
    shared_co2 = np.asarray([co2_by_year[year] for year in shared_years], dtype=float)
    shared_temp = np.asarray([temp_by_year[year] for year in shared_years], dtype=float)
    temp_params = fit_linear(temp_years, temp_values)
    temp_fit = linear_predict(temp_params, temp_years)
    temp_residual = temp_values - temp_fit
    temp_slope = temp_params[1]
    thresholds = {}
    temp_design = np.column_stack([np.ones(len(temp_years)), temp_years])
    temp_residual_variance = float(np.sum(temp_residual**2) / (len(temp_years) - 2))
    temp_covariance = temp_residual_variance * np.linalg.inv(temp_design.T @ temp_design)
    for threshold in (1.25, 1.50, 2.00):
        threshold_year = (threshold - temp_params[0]) / temp_slope
        gradient = np.asarray([-1.0 / temp_slope, -(threshold - temp_params[0]) / (temp_slope**2)])
        threshold_se = float(np.sqrt(max(0.0, gradient @ temp_covariance @ gradient)))
        thresholds[str(threshold)] = {
            "year": float(threshold_year),
            "standard_error_years": threshold_se,
            "ci95_years": [float(threshold_year - 1.96 * threshold_se), float(threshold_year + 1.96 * threshold_se)],
            "threshold_degC": threshold,
        }
    correlation = float(np.corrcoef(shared_co2, shared_temp)[0, 1])
    granger_co2_to_temp = granger_f_test(shared_co2, shared_temp)
    granger_temp_to_co2 = granger_f_test(shared_temp, shared_co2)
    sensitivity = {}
    for label, multiplier in (("minus_10_percent_rate", 0.90), ("baseline_rate", 1.00), ("plus_10_percent_rate", 1.10)):
        adjusted_rate = exponential_params[1] * multiplier
        adjusted_params = (exponential_params[0], adjusted_rate)
        sensitivity[label] = {
            "rate": float(adjusted_rate),
            "forecast_2050": float(exponential_predict(adjusted_params, np.array([2050.0]), train_years[0])[0]),
            "forecast_2100": float(exponential_predict(adjusted_params, np.array([2100.0]), train_years[0])[0]),
        }
    metrics_payload = {
        "run_id": "run-002",
        "case": "HiMCM 2022 Problem B",
        "subproblem": "Q1/Q2",
        "status": "pass",
        "input": {"path": "problem_files/himcm_data.csv", "series": "CO2", "observations": int(len(years)), "year_start": int(years[0]), "year_end": int(years[-1])},
        "split": {"train_observations": int(len(train_years)), "test_observations": int(len(test_years)), "test_year_start": int(test_years[0])},
        "models": {
            "linear": {"parameters": {"intercept": linear_params[0], "slope": linear_params[1]}, "train": metrics(values[:train_size], linear_all[:train_size]), "test": metrics(test_values, linear_test), "forecast_2050": float(linear_predict(linear_params, np.array([2050.0]))[0]), "forecast_2100": float(linear_predict(linear_params, np.array([2100.0]))[0]), "target_685_year": milestone(linear_forecast, target)},
            "exponential": {"parameters": {"amplitude_at_first_year": exponential_params[0], "rate": exponential_params[1]}, "train": metrics(values[:train_size], exponential_all[:train_size]), "test": metrics(test_values, exponential_test), "forecast_2050": float(exponential_predict(exponential_params, np.array([2050.0]), train_years[0])[0]), "forecast_2100": float(exponential_predict(exponential_params, np.array([2100.0]), train_years[0])[0]), "target_685_year": milestone(exponential_forecast, target)},
            "logistic": {"parameters": {"carrying_capacity": logistic_params[0], "rate": logistic_params[1], "midpoint_year": logistic_params[2]}, "train": metrics(values[:train_size], logistic_all[:train_size]), "test": metrics(test_values, logistic_test), "forecast_2050": float(logistic_predict(logistic_params, np.array([2050.0]))[0]), "forecast_2100": float(logistic_predict(logistic_params, np.array([2100.0]))[0]), "target_685_year": milestone(logistic_forecast, target)},
            "arima110": {"parameters": {"drift": arima_params[0], "phi": arima_params[1], "residual_sd": arima_params[2]}, "test": metrics(test_values, arima_test), "forecast_2050": float(arima_forecast[2050 - 2022]), "forecast_2100": float(arima_forecast[-1])},
        },
        "q1a_rolling_ten_year": {"window_years": 10, "maximum": maximum, "reference_2004": next(item for item in rolling if item["end_year"] == 2004), "all_windows": rolling},
        "q2_temperature": {
            "observations": int(len(temp_years)),
            "year_start": int(temp_years[0]),
            "year_end": int(temp_years[-1]),
            "linear_parameters": {"intercept": temp_params[0], "slope_degC_per_year": temp_params[1]},
            "fit": metrics(temp_values, temp_fit),
            "thresholds": thresholds,
            "shared_years": {"count": len(shared_years), "start": shared_years[0], "end": shared_years[-1]},
            "pearson_r": correlation,
            "granger": {"status": "computed_with_local_beta", "cause_co2_to_temperature": granger_co2_to_temp, "cause_temperature_to_co2": granger_temp_to_co2, "interpretation": "Granger statistics are exploratory and do not establish physical causation."},
        },
        "sensitivity": {"model": "exponential", "rate_multiplier": "baseline rate multiplied by 0.90/1.00/1.10", "scenarios": sensitivity},
        "environment": {"python": sys.version.split()[0], "numpy": np.__version__, "platform": platform.platform()},
        "warnings": ["ARIMA and Granger are transparent NumPy fallbacks; Granger p values use a local incomplete-beta implementation and remain exploratory.", "Trend extrapolation is exploratory and is not a physical climate model.", "Final paper and result freezing remain open."],
    }
    metrics_path = run_dir / "metrics.json"
    metrics_path.write_text(json.dumps(metrics_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    figure_path = None
    if args.plot:
        from plot_himcm_figures import draw_figures
        all_years = np.concatenate([years, forecast_years])
        figure_path = figure_dir / "fig1_co2_fits.png"
        rolling_years = np.asarray([item["end_year"] for item in rolling], dtype=float)
        rolling_values = np.asarray([item["increase"] for item in rolling], dtype=float)
        draw_figures(figure_dir, years, values, train_years, test_years, all_years, forecast_years,
                     linear_all, exponential_all, logistic_all, linear_forecast,
                     exponential_forecast, logistic_forecast, target, rolling_years, rolling_values,
                     maximum, temp_years, temp_values, temp_fit,
                     linear_predict(temp_params, forecast_years), thresholds,
                     shared_co2, shared_temp, correlation, sensitivity)

    print(json.dumps({"run": str(metrics_path), "figure": str(figure_path) if figure_path else None, "rolling_maximum": maximum, "linear_test_rmse": metrics_payload["models"]["linear"]["test"]["rmse"], "exponential_test_rmse": metrics_payload["models"]["exponential"]["test"]["rmse"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
