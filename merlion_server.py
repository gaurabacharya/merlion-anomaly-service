from fastapi import FastAPI
from pydantic import BaseModel
from merlion.models.anomaly.spectral_residual import SpectralResidual, SpectralResidualConfig
from merlion.post_process.threshold import Threshold
from merlion.transform.normalize import MeanVarNormalize
from merlion.models.defaults import DefaultDetectorConfig, DefaultDetector
from merlion.models.anomaly.zms import ZMS, ZMSConfig
from merlion.utils import TimeSeries
from merlion.transform.resample import TemporalResample
import pandas as pd
import uvicorn

app = FastAPI()

class DetectRequest(BaseModel):
    timestamps: list[str]   # ISO 8601 strings
    prices: list[float]
    symbol: str

class DetectResponse(BaseModel):
    anomaly_scores: list[float]
    labels: list[int]

@app.post("/detect", response_model=DetectResponse)
def detect_anomalies(req: DetectRequest):
    if len(req.timestamps) != len(req.prices):
        raise ValueError("Timestamps and prices must be the same length.")

    df = pd.DataFrame({
        "timestamp": req.timestamps,
        "value": req.prices
    })

    df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.tz_convert(None)
    df.set_index("timestamp", inplace=True)

    print(f"Received {len(df)} rows of data")
    print(df.tail())

    ts = TimeSeries.from_pd(df)

    config = SpectralResidualConfig(
        transform=MeanVarNormalize(),
        post_rule=Threshold(alm_threshold=3.0) 
    )
    model = SpectralResidual(config=config)

    print("Data going into Merlion:")
    print(ts.to_pd().tail(11))

    model.train(ts)

    scores = model.get_anomaly_score(ts)
    labels = model.get_anomaly_label(ts)

    return DetectResponse(
        anomaly_scores=scores.to_pd().iloc[:, 0].tolist(),
        labels=labels.to_pd().iloc[:, 0].astype(int).tolist()
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
