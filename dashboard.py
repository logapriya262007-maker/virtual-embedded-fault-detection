import streamlit as st
import pandas as pd
import json
from datetime import datetime

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Virtual Hardware Fault Detection",
    page_icon="⚡",
    layout="wide"
)

# ---------------- COLOURFUL DESIGN ----------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #eef2ff, #fdf2f8, #ecfeff);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827, #312e81, #164e63);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

h1 {
    color: #312e81 !important;
    font-weight: 900 !important;
}

h2 {
    color: #4338ca !important;
    font-weight: 800 !important;
}

h3 {
    color: #0f766e !important;
}

p, label {
    color: #1f2937;
}

div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #ffffff, #e0e7ff);
    border: 2px solid #818cf8;
    padding: 18px;
    border-radius: 18px;
    box-shadow: 0 5px 15px rgba(79, 70, 229, 0.12);
}

div[data-testid="stMetricLabel"] {
    color: #4338ca !important;
    font-weight: bold;
}

div[data-testid="stMetricValue"] {
    color: #1e1b4b !important;
    font-weight: 900;
}

div.stButton > button {
    background: linear-gradient(90deg, #4338ca, #7c3aed);
    color: white !important;
    border: none;
    border-radius: 12px;
    padding: 10px 18px;
    font-weight: bold;
    transition: 0.3s;
}

div.stButton > button:hover {
    background: linear-gradient(90deg, #312e81, #6d28d9);
    transform: scale(1.02);
}

div[data-testid="stDownloadButton"] button {
    background: linear-gradient(90deg, #1d4ed8, #1e3a8a) !important;
    color: white !important;
    border: 2px solid #1e40af !important;
    border-radius: 10px !important;
    font-weight: bold !important;
}

div[data-testid="stDownloadButton"] button:hover {
    background: linear-gradient(90deg, #1e3a8a, #172554) !important;
    color: white !important;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

div[data-testid="stForm"] {
    background: rgba(255, 255, 255, 0.85);
    border: 2px solid #c7d2fe;
    padding: 20px;
    border-radius: 18px;
}

hr {
    border-color: #c4b5fd;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------

if "history" not in st.session_state:
    st.session_state.history = []

if "latest_result" not in st.session_state:
    st.session_state.latest_result = None


# ---------------- FAULT DETECTION ----------------

def analyze_sensors(temperature, voltage, current, vibration):

    faults = []

    if temperature > 70:
        faults.append("High Temperature")

    if voltage < 180 or voltage > 260:
        faults.append("Voltage Out of Range")

    if current > 1.0:
        faults.append("High Current")

    if vibration > 5.0:
        faults.append("High Vibration")

    if faults:
        status = "ABNORMAL"
        recommendation = (
            "Inspect the affected sensor and verify the input values. "
            "This is a virtual diagnostic recommendation."
        )
    else:
        status = "NORMAL"
        recommendation = (
            "All entered sensor values are within the configured limits."
        )

    return {
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Temperature": temperature,
        "Voltage": voltage,
        "Current": current,
        "Vibration": vibration,
        "Status": status,
        "Faults": ", ".join(faults) if faults else "No Fault",
        "Recommendation": recommendation
    }


# ---------------- HEADER ----------------

st.markdown("""
<div style="
background: linear-gradient(110deg, #312e81, #6d28d9, #0891b2);
padding: 28px;
border-radius: 20px;
text-align: center;
margin-bottom: 20px;
box-shadow: 0 8px 22px rgba(49, 46, 129, 0.22);
">
<h1 style="color:white !important; margin-bottom:8px;">
⚡ AI-Based Virtual Embedded Hardware Fault Detection System
</h1>
<p style="color:#f5f3ff !important; font-size:17px;">
Virtual Sensor Monitoring • Fault Detection • Diagnostics • Analytics
</p>
</div>
""", unsafe_allow_html=True)

st.caption(
    "Prototype mode: sensor values are entered manually. "
    "Fault detection uses configured rules; no physical hardware or trained ML model is connected."
)


# ---------------- SIDEBAR ----------------

st.sidebar.markdown("# ⚡ CONTROL PANEL")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate Dashboard",
    [
        "🏠 Overview",
        "📡 Sensor Monitoring",
        "🚨 Fault Detection",
        "🩺 Diagnostics",
        "📊 Analytics",
        "📁 Fault History"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("Virtual embedded system prototype")


# ---------------- OVERVIEW ----------------

if page == "🏠 Overview":

    st.title("🏠 System Overview")
    st.write("Welcome to your virtual embedded hardware monitoring dashboard!")

    total_tests = len(st.session_state.history)

    total_faults = sum(
        1 for item in st.session_state.history
        if item["Status"] == "ABNORMAL"
    )

    normal_tests = total_tests - total_faults

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("🧪 Total Tests", total_tests)

    with c2:
        st.metric("✅ Normal Tests", normal_tests)

    with c3:
        st.metric("🚨 Faulty Tests", total_faults)

    st.markdown("---")
    st.subheader("🌈 System Features")

    c1, c2 = st.columns(2)

    with c1:
        st.success("📡 Sensor Monitoring")
        st.write("Enter temperature, voltage, current and vibration values.")

        st.error("🚨 Fault Detection")
        st.write("Identify values that exceed configured limits.")

        st.info("🩺 Diagnostics")
        st.write("View fault information and suggested checks.")

    with c2:
        st.warning("📊 Analytics")
        st.write("Explore normal and abnormal test counts.")

        st.success("📁 Fault History")
        st.write("Review previous tests and export the recorded data.")

    st.markdown("---")
    st.subheader("🔧 Sensors in This Prototype")

    sensor_cols = st.columns(4)

    sensor_data = [
        ("🌡️ Temperature", "°C"),
        ("🔋 Voltage", "V"),
        ("⚡ Current", "A"),
        ("📳 Vibration", "mm/s")
    ]

    for col, (name, unit) in zip(sensor_cols, sensor_data):
        with col:
            st.markdown(
                f"""
                <div style="
                    background:linear-gradient(135deg,#dbeafe,#ede9fe);
                    border:2px solid #a5b4fc;
                    border-radius:16px;
                    padding:20px;
                    text-align:center;
                    min-height:100px;">
                    <h3 style="color:#3730a3;">{name}</h3>
                    <p style="color:#4338ca;">Unit: {unit}</p>
                </div>
                """,
                unsafe_allow_html=True
            )


# ---------------- SENSOR MONITORING ----------------

elif page == "📡 Sensor Monitoring":

    st.title("📡 Sensor Monitoring")
    st.write("Enter virtual sensor readings and analyze them.")

    with st.form("sensor_form"):

        st.subheader("🌡️ Enter Sensor Values")

        c1, c2 = st.columns(2)

        with c1:
            temperature = st.number_input(
                "🌡️ Temperature (°C)",
                min_value=-50.0,
                max_value=260.0,
                value=35.0,
                step=1.0
            )

            voltage = st.number_input(
                "🔋 Voltage (V)",
                min_value=0.0,
                max_value=260.0,
                value=3.3,
                step=0.1
            )

        with c2:
            current = st.number_input(
                "⚡ Current (A)",
                min_value=0.0,
                max_value=260.0,
                value=0.5,
                step=0.1
            )

            vibration = st.number_input(
                "📳 Vibration (mm/s)",
                min_value=0.0,
                max_value=100.0,
                value=2.0,
                step=0.5
            )

        submitted = st.form_submit_button(
            "🔍 ANALYZE SENSORS",
            use_container_width=True
        )

    if submitted:

        result = analyze_sensors(
            temperature,
            voltage,
            current,
            vibration
        )

        st.session_state.latest_result = result
        st.session_state.history.append(result)

        st.markdown("---")
        st.subheader("📋 Analysis Result")

        if result["Status"] == "NORMAL":
            st.success("✅ SYSTEM STATUS: NORMAL")
        else:
            st.error("🚨 SYSTEM STATUS: ABNORMAL")

        a, b, c, d = st.columns(4)

        a.metric("🌡️ Temperature", f"{temperature:.1f} °C")
        b.metric("🔋 Voltage", f"{voltage:.2f} V")
        c.metric("⚡ Current", f"{current:.2f} A")
        d.metric("📳 Vibration", f"{vibration:.1f}")

        if result["Status"] == "ABNORMAL":
            st.warning("Detected fault(s): " + result["Faults"])
        else:
            st.success("No configured faults detected.")

        st.info("🩺 Recommendation: " + result["Recommendation"])


# ---------------- FAULT DETECTION ----------------

elif page == "🚨 Fault Detection":

    st.title("🚨 Fault Detection Center")

    result = st.session_state.latest_result

    if result is None:
        st.info("No analysis result yet. Open Sensor Monitoring and analyze sensor values first.")

    else:
        if result["Status"] == "ABNORMAL":
            st.error("🚨 ABNORMAL CONDITION DETECTED")
            st.write("**Detected fault(s):**", result["Faults"])
        else:
            st.success("✅ ALL CHECKED VALUES ARE NORMAL")
            st.write("No configured faults were detected.")

        st.markdown("---")
        st.subheader("📋 Latest Sensor Readings")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Temperature", f'{result["Temperature"]:.1f} °C')
        c2.metric("Voltage", f'{result["Voltage"]:.2f} V')
        c3.metric("Current", f'{result["Current"]:.2f} A')
        c4.metric("Vibration", f'{result["Vibration"]:.1f}')

        st.caption("Detection is based on fixed thresholds, not a trained AI model.")


# ---------------- DIAGNOSTICS ----------------

elif page == "🩺 Diagnostics":

    st.title("🩺 Diagnostics & Recommendations")

    result = st.session_state.latest_result

    if result is None:
        st.info("Analyze sensor values first to view diagnostics.")

    else:
        st.write("### Latest Diagnostic Result")

        if result["Status"] == "NORMAL":
            st.success("System status: NORMAL")
        else:
            st.error("System status: ABNORMAL")

        st.write("**Fault information:**", result["Faults"])

        st.info(result["Recommendation"])

        st.markdown("---")
        st.subheader("🔧 Configured Fault Rules")

        rules = pd.DataFrame([
            ["Temperature", "Above 70 °C", "High Temperature"],
            ["Voltage", "Below 3.0 V or above 3.6 V", "Voltage Out of Range"],
            ["Current", "Above 1.0 A", "High Current"],
            ["Vibration", "Above 5.0 mm/s", "High Vibration"]
        ], columns=["Sensor", "Rule", "Detected Condition"])

        st.dataframe(rules, use_container_width=True, hide_index=True)


# ---------------- ANALYTICS ----------------

elif page == "📊 Analytics":

    st.title("📊 Analytics Dashboard")

    if not st.session_state.history:
        st.info("Run a sensor analysis to generate analytics.")

    else:
        df = pd.DataFrame(st.session_state.history)

        total = len(df)
        normal = int((df["Status"] == "NORMAL").sum())
        abnormal = int((df["Status"] == "ABNORMAL").sum())

        c1, c2, c3 = st.columns(3)

        c1.metric("🧪 Total Tests", total)
        c2.metric("✅ Normal", normal)
        c3.metric("🚨 Abnormal", abnormal)

        st.markdown("---")
        st.subheader("🟣 Normal vs Abnormal Tests")

        chart_data = pd.DataFrame({
            "Status": ["Normal", "Abnormal"],
            "Number of Tests": [normal, abnormal]
        }).set_index("Status")

        st.bar_chart(chart_data, color="#7c3aed")

        st.markdown("---")
        st.subheader("🌡️ Sensor Readings Over Time")

        numeric_cols = [
            "Temperature",
            "Voltage",
            "Current",
            "Vibration"
        ]

        st.line_chart(df[numeric_cols])


# ---------------- FAULT HISTORY ----------------

elif page == "📁 Fault History":

    st.title("📁 Fault History & Downloads")

    if not st.session_state.history:

        st.info("No test history is available in this session yet.")

        template = pd.DataFrame(columns=[
            "Time",
            "Temperature",
            "Voltage",
            "Current",
            "Vibration",
            "Status",
            "Faults",
            "Recommendation"
        ])

        st.download_button(
            "📥 Download CSV Template",
            data=template.to_csv(index=False).encode("utf-8"),
            file_name="sensor_history_template.csv",
            mime="text/csv",
            use_container_width=True
        )

    else:

        df = pd.DataFrame(st.session_state.history)

        total = len(df)
        abnormal_df = df[df["Status"] == "ABNORMAL"]

        c1, c2 = st.columns(2)

        c1.metric("📋 Total Records", total)
        c2.metric("🚨 Fault Records", len(abnormal_df))

        st.markdown("---")
        st.subheader("📑 Recorded Test History")

        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("📥 Download Your Reports")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.download_button(
                "📥 Full History CSV",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name="sensor_history.csv",
                mime="text/csv",
                use_container_width=True
            )

        with c2:
            json_data = json.dumps(
                st.session_state.history,
                indent=4
            )

            st.download_button(
                "📥 Full History JSON",
                data=json_data.encode("utf-8"),
                file_name="sensor_history.json",
                mime="application/json",
                use_container_width=True
            )

        with c3:
            st.download_button(
                "🚨 Fault Records CSV",
                data=abnormal_df.to_csv(index=False).encode("utf-8"),
                file_name="fault_records.csv",
                mime="text/csv",
                use_container_width=True
            )

        st.markdown("---")

        confirm_clear = st.checkbox(
            "I want to clear the current session history"
        )

        if st.button("🗑️ Clear History"):

            if confirm_clear:
                st.session_state.history = []
                st.session_state.latest_result = None
                st.success("Current session history cleared.")
                st.rerun()
            else:
                st.warning("Please tick the confirmation checkbox first.")


# ---------------- FOOTER ----------------

st.markdown("---")

st.markdown("""
<div style="
background:linear-gradient(90deg,#312e81,#6d28d9,#0891b2);
padding:15px;
border-radius:12px;
text-align:center;">
<p style="color:white !important; margin:0;">
⚡ Virtual Embedded Hardware Fault Detection System |
Prototype Dashboard
</p>
</div>
""", unsafe_allow_html=True)