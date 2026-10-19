
# 🚁 Smart Drone Battery Monitoring System

A Python-based interactive dashboard for simulating drone battery
monitoring, discharge behaviour, and estimated remaining flight time.

## 📌 Project Overview

This project demonstrates how drone battery readings can be
visualised and analysed using a web dashboard.

The application uses simulated values and does not connect to
a physical drone or battery.

## ✨ Features

- Battery percentage monitoring
- Voltage, current, and power display
- Estimated remaining flight time
- Simulated battery discharge
- Battery history graph
- Flight history table
- Battery performance summary
- CSV download for recorded data and reports

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- VS Code

## ⚙️ Installation

1. Install Python 3.10 or later.
2. Open the project folder in VS Code.
3. Open the terminal.
4. Install the required libraries:

```bash
py -m pip install streamlit pandas
```

## ▶️ Run the Application

Run this command in the project terminal:

```bash
py -m streamlit run app.py
```

Open the local URL displayed in the terminal.

## 🧪 How to Test

1. Adjust the simulated battery settings.
2. Click **Simulate Next Reading**.
3. View the battery history graph and table.
4. Review the battery performance report.
5. Download the CSV reports.

## ⚠️ Limitations

This is a software simulation project. It does not measure
real battery voltage, current, or battery health.

Flight-time values are simplified mathematical estimates
and must not be used for real flight safety decisions.

## 👩‍💻 Project Status

Working software prototype with simulated battery readings,
interactive visualisation, and CSV report export.
