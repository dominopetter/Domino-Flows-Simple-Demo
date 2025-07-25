import streamlit as st
import os
from io import StringIO
from pathlib import Path

# --- Constants ---
CODE_DIR = "/mnt/code"
SAVE_DIR = "/mnt/data/flows-demo"
Path(SAVE_DIR).mkdir(parents=True, exist_ok=True)

# --- Page Setup ---
st.set_page_config(page_title="Domino Flow Designer", layout="wide")
st.title("Domino Flow Designer (Single Task Prototype)")

# --- Step 1: Select or Upload Script ---
st.subheader("1. Select or Upload Script")

# List .py files from /mnt/code
existing_scripts = [f for f in os.listdir(CODE_DIR) if f.endswith(".py")]
selected_script = st.selectbox("Select existing script from /mnt/code:", ["-- None --"] + existing_scripts)

uploaded_file = st.file_uploader("Or upload a Python script", type=["py"])

script_name = None
if selected_script != "-- None --":
    script_name = os.path.join(CODE_DIR, selected_script)
    st.info(f"Using existing script: {script_name}")
elif uploaded_file:
    script_name = uploaded_file.name
    with open(script_name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Uploaded {script_name}")

# --- Step 2: Task Definition ---
st.subheader("2. Define Task Settings")
task_name = st.text_input("Task name", value="MyTask")
default_command = f"python {os.path.basename(script_name) if script_name else 'script.py'}"
command = st.text_input("Command", value=default_command)

# --- Step 3: Task Inputs ---
st.subheader("3. Define Task Inputs (only one for now)")
input_name = st.text_input("Input name", value="data_path")
input_type = st.selectbox("Input type", ["str", "int", "float", "bool"])

# --- Step 4: Task Outputs ---
st.subheader("4. Define Task Output (only one for now)")
output_name = st.text_input("Output name", value="processed_data")
output_type = st.selectbox(
    "Output type",
    ["FlyteFile[TypeVar('csv')]", "FlyteFile[TypeVar('txt')]", "float", "int", "str"]
)

# --- Step 5: Generate workflow.py ---
if st.button("Generate Workflow File"):
    workflow_code = f'''from flytekit import workflow
from flytekitplugins.domino.helpers import Input, Output, run_domino_job_task
from flytekit.types.file import FlyteFile
from typing import TypeVar

@workflow