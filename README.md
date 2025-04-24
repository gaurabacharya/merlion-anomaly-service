# merlion-anomaly-service

A lightweight Python API built with **FastAPI** that wraps the [Salesforce Merlion](https://github.com/salesforce/Merlion) anomaly detection library to serve real-time predictions on market tick data. This service is intended to be used in tandem with the [`market-anomaly-detector`](https://github.com/your-org/market-anomaly-detector) Spring Boot backend.

## 🌟 Purpose

This service is designed to:
- Accept time-series tick data (timestamp + price) via an HTTP API.
- Use **Merlion's SpectralResidual** anomaly detection model with configurable post-processing.
- Return anomaly scores and binary anomaly labels to help identify data feed glitches, sudden price jumps, or unusual market patterns.
- Allow flexible, lightweight deployment either via Docker or as a standalone Python app.

## 🧠 Why Merlion?

Merlion is an open-source time series anomaly detection library by Salesforce that provides:
- Univariate and multivariate anomaly detection.
- Support for advanced detection algorithms like SpectralResidual, ZMS, and IsolationForest.
- Optional post-rule thresholding (e.g., z-score filtering).
- Built-in transform pipelines (resampling, normalization, etc.).

## 🧩 Architecture

