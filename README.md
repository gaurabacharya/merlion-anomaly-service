# merlion-anomaly-service

A lightweight Python API built with **FastAPI** that wraps the [Salesforce Merlion](https://github.com/salesforce/Merlion) anomaly detection library to serve real-time predictions on market tick data. This service is intended to be used in tandem with the [`market-anomaly-detector`](https://github.com/gaurabacharya/market-anomoly-detector-springboot) Spring Boot backend.

## Demo 
https://youtu.be/YPlRRCrc9wo

## Purpose

This service is designed to:
- Accept time-series tick data (timestamp + price) via an HTTP API.
- Use **Merlion's SpectralResidual** anomaly detection model with configurable post-processing.
- Return anomaly scores and binary anomaly labels to help identify data feed glitches, sudden price jumps, or unusual market patterns.
- Allow flexible, lightweight deployment either via Docker or as a standalone Python app.

## Why Merlion?

Merlion is an open-source time series anomaly detection library by Salesforce that provides:
- Univariate and multivariate anomaly detection.
- Support for advanced detection algorithms like SpectralResidual, ZMS, and IsolationForest.
- Optional post-rule thresholding (e.g., z-score filtering).
- Built-in transform pipelines (resampling, normalization, etc.).


## How to Run Locally

### 1. Create and activate a virtual environment

```bash
python3 -m venv quotemediaapp
source quotemediaapp/bin/activate  # macOS/Linux
# OR
quotemediaapp\Scripts\activate     # Windows
```

### 2. Make sure your requirement.txt includes
```txt
fastapi
uvicorn
merlion
pydantic
pandas
numpy
scikit-learn
```
Then run:
```bash
pip install -r requirements.txt
```

### 3. Start the Server
Either 
```bash
python merlion_server.py
```
or 
```bash
uvicorn merlion_server:app --reload --port 8001
```
The app will be accessible at http://localhost:8001

### 4. Run the steps in the repo [market-anomaly-detector](https://github.com/gaurabacharya/market-anomoly-detector-springboot) and have the application working! 

## Endpoint
POST /detect

Request:
```json
{
  "timestamps": [
    "2025-04-21T09:30:00Z",
    "2025-04-21T09:30:05Z",
    "2025-04-21T09:30:10Z"
  ],
  "prices": [101.0, 102.3, 100.5],
  "symbol": "AAPL"
}
```

Response:
```json
{
  "anomaly_scores": [0.01, 0.05, 2.98],
  "labels": [0, 0, 1]
}
```

## Configuring Details
Currently using the SpectralResidual model with z-score thresholding:
```python
config = SpectralResidualConfig(
    transform=MeanVarNormalize(),
    post_rule=Threshold(alm_threshold=3.0)
)
```
This means only points with anomaly scores > 3 standard deviations from the mean will be labeled as anomalies.

### How This Scales
In production, this service could be:
- Containerized via Docker and deployed as a microservice.
- Connected to real-time tick feeds (e.g., from Kafka or WebSockets).
- Queried from multiple services including your Spring Boot backend.
- Extended to handle multivariate data (e.g., price + volume).
- Hooked into alerting systems (Slack, email, dashboards).

