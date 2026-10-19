
import random
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Smart Drone Battery Monitor",
    page_icon="🚁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Session state ----------
if "history" not in st.session_state:
    st.session_state.history = []

if "sim_battery" not in st.session_state:
    st.session_state.sim_battery = None

if "flight_started" not in st.session_state:
    st.session_state.flight_started = False


# ---------- Sidebar ----------
st.sidebar.title("⚙️ Battery Configuration")
st.sidebar.caption("Simulation Controls")

capacity = st.sidebar.number_input(
    "Battery Capacity (mAh)",
    min_value=500,
    max_value=30000,
    value=3000,
    step=500
)

start_level = st.sidebar.slider(
    "Starting Battery (%)",
    min_value=0,
    max_value=100,
    value=80
)

voltage = st.sidebar.number_input(
    "Battery Voltage (V)",
    min_value=0.1,
    max_value=60.0,
    value=11.1,
    step=0.1,
    format="%.2f"
)

current = st.sidebar.number_input(
    "Current Consumption (A)",
    min_value=0.0,
    max_value=100.0,
    value=2.0,
    step=0.5
)

st.sidebar.divider()

if st.sidebar.button("🔄 Reset / New Simulation", use_container_width=True):
    st.session_state.history = []
    st.session_state.sim_battery = None
    st.session_state.flight_started = False
    st.rerun()

st.sidebar.caption(
    "Demo only — no physical drone or battery connected."
)


# ---------- Current values ----------
if st.session_state.sim_battery is None:
    battery = start_level
else:
    battery = st.session_state.sim_battery

power = voltage * current
remaining_capacity = (capacity / 1000) * battery / 100

if current > 0:
    flight_time = (remaining_capacity / current) * 60
else:
    flight_time = 0


# ---------- Header ----------
st.title("🚁 Smart Drone Battery Monitoring System")
st.caption(
    "DRONE TELEMETRY  /  BATTERY ANALYTICS  /  SIMULATION"
)

st.info(
    "Simulation Mode: All readings are simulated, "
    "not measured from a real drone."
)

# ---------- Metric cards ----------
st.subheader("📊 Battery Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("🔋 Battery Level", f"{battery}%")
c2.metric("⚡ Voltage", f"{voltage:.2f} V")
c3.metric("🔌 Current", f"{current:.2f} A")
c4.metric("💡 Power", f"{power:.2f} W")


# ---------- Battery status ----------
st.subheader("🔎 Battery Status")
st.progress(battery / 100)

if battery <= 20:
    st.error("🚨 CRITICAL: Simulated battery level is low!")
elif battery <= 50:
    st.warning("⚠️ WARNING: Simulated battery level is moderate.")
else:
    st.success("✅ Simulated battery level is normal.")


# ---------- Flight time ----------
st.subheader("⏱️ Estimated Remaining Flight Time")

t1, t2 = st.columns([1, 2])

with t1:
    st.metric("Estimated Time", f"{flight_time:.1f} minutes")

with t2:
    st.caption(
        "Simplified estimate based on remaining capacity "
        "and constant current consumption. Not a real flight prediction."
    )


# ---------- Flight simulation ----------
st.divider()
st.subheader("🧪 Flight Simulation")

left, right = st.columns([1, 3])

with left:
    simulate = st.button(
        "▶ Simulate Next Reading",
        use_container_width=True
    )

with right:
    st.caption(
        "First reading records the starting level. "
        "Each subsequent reading simulates battery discharge."
    )

if simulate:
    if st.session_state.sim_battery is None:
        new_battery = start_level
    else:
        previous = st.session_state.sim_battery
        new_battery = max(0, previous - random.randint(3, 8))

    st.session_state.sim_battery = new_battery
    st.session_state.flight_started = True

    st.session_state.history.append({
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Battery (%)": new_battery,
        "Voltage (V)": voltage,
        "Current (A)": current,
        "Power (W)": round(power, 2)
    })

    if new_battery == 0:
        st.warning("Simulation reached 0% battery.")
    else:
        st.success(f"Reading recorded: {new_battery}% battery")

    st.rerun()


# ---------- History graph ----------
st.divider()
st.subheader("📈 Simulated Battery History")

if st.session_state.history:
    history_df = pd.DataFrame(st.session_state.history)

    chart_data = history_df[["Time", "Battery (%)"]].set_index("Time")
    st.line_chart(chart_data, height=300)

    st.subheader("📋 Flight History")
    st.dataframe(history_df, use_container_width=True)

    st.download_button(
        "⬇️ Download Flight History CSV",
        data=history_df.to_csv(index=False).encode("utf-8"),
        file_name="drone_flight_history.csv",
        mime="text/csv"
    )
else:
    st.info(
        "No readings recorded yet. Click "
        "'Simulate Next Reading' to start."
    )


# ---------- Battery performance report ----------
st.divider()
st.subheader("🩺 Battery Performance Report")

if st.session_state.history:
    report_df = pd.DataFrame(st.session_state.history)

    first_level = float(report_df["Battery (%)"].iloc[0])
    latest_level = float(report_df["Battery (%)"].iloc[-1])
    total_readings = len(report_df)

    # Positive means discharged; negative means increased.
    total_discharge = first_level - latest_level

    if total_readings > 1:
        average_discharge = total_discharge / (total_readings - 1)
    else:
        average_discharge = 0.0

    r1, r2, r3 = st.columns(3)

    r1.metric("Recorded Readings", total_readings)
    r2.metric("Starting Battery", f"{first_level:.0f}%")
    r3.metric(
        "Latest Battery",
        f"{latest_level:.0f}%",
        delta=f"{latest_level - first_level:+.0f} percentage points"
    )

    st.write(
        f"**Total simulated discharge:** "
        f"{total_discharge:.1f} percentage points"
    )

    st.write(
        f"**Average discharge per interval:** "
        f"{average_discharge:.2f} percentage points"
    )

    if latest_level <= 20:
        st.error("Report status: Simulated battery level is critical.")
    elif latest_level <= 50:
        st.warning("Report status: Simulated battery level is moderate.")
    else:
        st.success("Report status: Simulated battery level is above 50%.")

    st.download_button
    report_summary = pd.DataFrame([{
        "Recorded Readings": total_readings,
        "Starting Battery (%)": first_level,
        "Latest Battery (%)": latest_level,
        "Total Discharge (percentage points)": total_discharge,
        "Average Discharge Per Interval (percentage points)": average_discharge,
        "Report Type": "Simulation Only"
    }])

    st.download_button(
        "📥 Download Battery Performance Summary",
        data=report_summary.to_csv(index=False).encode("utf-8"),
        file_name="battery_performance_summary.csv",
        mime="text/csv"
    )


