import streamlit as st
from io import StringIO
import sys
from deadlock_demo import Deadlock

st.set_page_config(page_title="Deadlock Recovery Simulator", page_icon="🧠")

st.title("🧠 Deadlock Recovery Simulator")
st.subheader("Recovery from Deadlock using Process Termination and Resource Preemption")

st.write("Choose a recovery method below and run the simulation:")

option = st.selectbox(
    "Recovery Method:",
    ("Terminate All Processes", "Terminate One at a Time", "Resource Preemption")
)

if st.button("Run Simulation"):
    buffer = StringIO()
    sys.stdout = buffer
    
    d = Deadlock()
    d.setup()
    if option == "Terminate All Processes":
        d.kill_all()
    elif option == "Terminate One at a Time":
        d.kill_one()
    else:
        d.preempt()
    
    sys.stdout = sys.__stdout__
    st.text_area("Simulation Output", buffer.getvalue(), height=400)
