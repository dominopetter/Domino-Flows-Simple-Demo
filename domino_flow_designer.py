import dash
from dash import html, dcc, Input, Output, State
import dash_cytoscape as cyto
import os
from pathlib import Path

# --- Constants ---
CODE_DIR = "/mnt/code"
SAVE_DIR = Path("/mnt/data/flows-demo")
SAVE_DIR.mkdir(parents=True, exist_ok=True)

# List Python scripts
scripts = [f for f in os.listdir(CODE_DIR) if f.endswith(".py")]

# Initial empty graph
default_elements = []

app = dash.Dash(__name__)
app.title = "Domino Flow Builder"

app.layout = html.Div([
    html.H1("Domino Flow Builder (Dash Prototype)"),
    html.Div([
        html.H3("Available Scripts"),
        html.Ul([html.Li(script, id=f"script-{i}") for i, script in enumerate(scripts)])
    ], style={"width": "20%", "float": "left"}),

    html.Div([
        cyto.Cytoscape(
            id='dag-canvas',
            layout={'name': 'breadthfirst'},
            style={'width': '100%', 'height': '500px'},
            elements=default_elements,
            stylesheet=[
                {'selector': 'node', 'style': {'label': 'data(label)'}},
                {'selector': 'edge', 'style': {'curve-style': 'bezier', 'target-arrow-shape': 'triangle'}}
            ]
        ),
        html.Button("Generate Workflow", id="generate-btn", n_clicks=0),
        html.Div(id="output")
    ], style={"width": "75%", "float": "right"})
])

@app.callback(
    Output("output", "children"),
    Input("generate-btn", "n_clicks"),
    State("dag-canvas", "elements")
)
def generate_workflow(n_clicks, elements):
    if n_clicks == 0:
        return ""
    if not elements:
        return "No graph defined."

    nodes = [el for el in elements if el['data'].get('id') and el['group'] == 'nodes']
    edges = [el for el in elements if el['group'] == 'edges']

    # Simple code generation (linear order for now)
    tasks = ""
    for node in nodes:
        script = node['data']['label']
        tasks += f"""
    {node['data']['id']}_results = run_domino_job_task(
        flyte_task_name="{node['data']['id']}",
        command="python {script}",
        inputs=[],
        output_specs=[],
        use_project_defaults_for_omitted=True
    )"""

    workflow_code = f"""from flytekit import workflow
from flytekitplugins.domino.helpers import run_domino_job_task

@workflow
def auto_generated_flow():
{tasks}
    return
"""
    save_path = SAVE_DIR / "workflow.py"
    save_path.write_text(workflow_code)

    return f"Workflow generated and saved to {save_path}"

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8050)