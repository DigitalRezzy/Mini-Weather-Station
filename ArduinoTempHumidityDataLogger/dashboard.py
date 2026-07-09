import streamlit as st
import serial
import pandas as pd
import time
from datetime import datetime

#settings
PORT = "COM3"
BAUD = 9600
CSV_FILE = "data.csv"

#page configs
st.set_page_config(page_title="Environment Monitor", layout="wide")

st.title("Arduino Environment Monitor")

#serial connection
@st.cache_resource
def connect_serial():
    try:
        return serial.Serial(PORT, BAUD, timeout=1)
    except Exception:
        st.error(f" Cannot open {PORT}. Close Serial Monitor or check port.")
        st.stop()

ser = connect_serial()

#load or create a csv
try:
    df = pd.read_csv(CSV_FILE)
except:
    df = pd.DataFrame(columns=["Time","Temperature","Humidity","HeatIndex"])
    df.to_csv(CSV_FILE, index=False)

#metrics row
metric_col1, metric_col2, metric_col3 = st.columns(3)

temp_metric = metric_col1.empty()
hum_metric = metric_col2.empty()
heat_metric = metric_col3.empty()

st.divider()

#overview graph
st.subheader("Combined Trends")
overview_chart = st.empty()

st.divider()

#indavidual graphs
col1, col2, col3 = st.columns(3)

col1.markdown("###  Temperature")
temp_chart = col1.empty()

col2.markdown("###  Feels Like")
heat_chart = col2.empty()

col3.markdown("###  Humidity")
humidity_chart = col3.empty()

while True:

    if ser.in_waiting:
        line = ser.readline().decode("utf-8").strip()

        try:
            temp, hum, heat = map(float, line.split(","))

            new_row = {
                "Time": datetime.now(),
                "Temperature": temp,
                "Humidity": hum,
                "HeatIndex": heat
            }

            #append to csv
            df = pd.read_csv(CSV_FILE)
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(CSV_FILE, index=False)

            #update metrics
            temp_metric.metric("Temperature (°C)", f"{temp:.1f}")
            hum_metric.metric("Humidity (%)", f"{hum:.0f}")
            heat_metric.metric("Feels Like (°C)", f"{heat:.1f}")

            df["Time"] = pd.to_datetime(df["Time"])
            df_indexed = df.set_index("Time")

            #update the graphs
            overview_chart.line_chart(
                df_indexed[["Temperature","Humidity","HeatIndex"]]
            )

            temp_chart.line_chart(df_indexed[["Temperature"]])
            heat_chart.line_chart(df_indexed[["HeatIndex"]])
            humidity_chart.line_chart(df_indexed[["Humidity"]])

        except:
            pass

    time.sleep(1)