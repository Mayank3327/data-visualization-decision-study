import pandas as pd
from pathlib import Path

RESULT_DIR = Path("results")
files = list(RESULT_DIR.glob("participant_*.csv"))

if not files:
    raise SystemExit("No participant CSV files found in results/.")

df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

summary = (
    df.groupby("data_display")
      .agg(
          accuracy_percent=("correct", lambda x: 100 * x.mean()),
          mean_response_time_sec=("response_time_sec", "mean"),
          mean_confidence=("confidence", "mean"),
          trials=("correct", "count")
      )
      .reset_index()
)

summary.to_csv("summary_by_display.csv", index=False)
print(summary.to_string(index=False))
print("\nTask-level summary:")
print(
    df.groupby(["data_display", "task_type"])
      .agg(accuracy_percent=("correct", lambda x: 100*x.mean()),
           mean_response_time_sec=("response_time_sec", "mean"),
           mean_confidence=("confidence", "mean"))
      .round(2)
)
