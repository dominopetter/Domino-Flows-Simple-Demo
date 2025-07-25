import streamlit as st
import os
from io import StringIO

# --- Page Setup ---
st.set_page_config(page_title="Domino Flow Designer", layout="wide")
st.title("Domino Flow Designer (Single Task Prototype)")

# --- Step 1: Upload/Select Script ---
st.subheader("1. Select or Upload Script")
uploaded_file = st.file_uploader("Upload a Python script for your task", type=["py"])

script_name = None
if uploaded_file:
    # Save script locally (in a Domino Workspace this would be the project directory)
    script_name = uploaded_file.name
    with open(script_name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Uploaded {script_name}")

# --- Step 2: Task Definition ---
st.subheader("2. Define Task Settings")
task_name = st.text_input("Task name", value="MyTask")
command = st.text_input("Command", value=f"python {script_name if script_name else 'script.py'}")

# --- Step 3: Task Inputs ---
st.subheader("3. Define Task Inputs (only one for now)")
input_name = st.text_input("Input name", value="data_path")
input_type = st.selectbox("Input type", ["str", "int", "float", "bool"])

# --- Step 4: Task Outputs ---
st.subheader("4. Define Task Output (only one for now)")
output_name = st.text_input("Output name", value="processed_data")
output_type = st.selectbox("Output type", ["FlyteFile[TypeVar('csv')]", "FlyteFile[TypeVar('txt')]", "float", "int", "str"])

# --- Step 5: Generate workflow.py ---
if st.button("Generate Workflow File"):
    workflow_code = f'''from flytekit import workflow
from flytekitplugins.domino.helpers import Input, Output, run_domino_job_task
from flytekit.types.file import FlyteFile
from typing import TypeVar

@workflow
def simple_flow({input_name}: {input_type}) -> {output_type}:
    results = run_domino_job_task(
        flyte_task_name="{task_name}",
        command="{command}",
        inputs=[Input(name="{input_name}", type={input_type}, value={input_name})],
        output_specs=[Output(name="{output_name}", type={output_type})],
        use_project_defaults_for_omitted=True
    )
    return results["{output_name}"]
'''

    st.code(workflow_code, language="python")

    # Provide download button
    st.download_button(
        label="Download workflow.py",
        data=workflow_code,
        file_name="workflow.py",
        mime="text/plain"
    )