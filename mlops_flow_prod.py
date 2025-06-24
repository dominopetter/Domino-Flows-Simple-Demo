from flytekit import workflow
from flytekit.types.file import FlyteFile
from typing import TypeVar, NamedTuple
from flytekitplugins.domino.helpers import Input, Output, run_domino_job_task
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, GitRef, EnvironmentRevisionSpecification, EnvironmentRevisionType, DatasetSnapshot
from flytekitplugins.domino.artifact import Artifact, DATA, MODEL, REPORT

# As this is considered a PROD Flow definition, we set use_project_defaults_for_omitted to False 
# and explictly set every required parameter in the task defintion to ensure reproducability.
environment_name="6.0 Domino Standard Environment Py3.10 R4.4"
environment_revision_id="6732709a37394436a080d8ac"
GitRef_type="branches"
GitRef_value="main"
volume_size_gib=10
dfs_repo_commit_id="210c74f00622f1e509e8a3fed280b11bd05ff9f9"


# Set if you want caching on or off. 
cache=False

# This calls the Artifact library, to create two named Flow Artifacts that we can label our merged data and model files as. 
DataArtifact = Artifact("Merged Data", DATA)
ModelArtifact = Artifact("Random Forest Model", MODEL)

@workflow
def model_training(data_path_a: str, data_path_b: str): 
    '''
    Sample data preparation and training flow. This flow:
    
        1. Loads two datasets in from different sources
        2. Merges the data together
        3. Does some data preprocessing
        4. Trains a model using the processed data
        5. Output the merged data and model as Flow Artifacts

    To run this flow, execute the following line in the terminal

    pyflyte run --remote  mlops_flow_prod.py model_training --data_path_a /mnt/code/data/datasetA.csv --data_path_b /mnt/code/data/datasetB.csv
    '''

    task1 = run_domino_job_task(
        flyte_task_name='Load Data A',
        command='python /mnt/code/scripts/load-data-A.py',
        inputs=[Input(name='data_path', type=str, value=data_path_a)],
        output_specs=[Output(name='datasetA', type=FlyteFile[TypeVar('csv')])],
        environment_name=environment_name,
        #environment_revision_id=environment_revision_id,
        hardware_tier_name="Small",
        dataset_snapshots=[],
        main_git_repo_ref=GitRef(Type=GitRef_type, Value=GitRef_value),
        volume_size_gib=volume_size_gib,
        dfs_repo_commit_id=dfs_repo_commit_id,
        external_data_volumes=[],
        cache=cache,
        cache_version="1.0",
        use_project_defaults_for_omitted=True
    )


    task2 = run_domino_job_task(
        flyte_task_name='Load Data B',
        command='python /mnt/code/scripts/load-data-B.py',
        inputs=[Input(name='data_path', type=str, value=data_path_b)],
        output_specs=[Output(name='datasetB', type=FlyteFile[TypeVar('csv')])],
        environment_name=environment_name,
        #environment_revision_id=environment_revision_id,
        hardware_tier_name="Small",
        dataset_snapshots=[],
        main_git_repo_ref=GitRef(Type=GitRef_type, Value=GitRef_value),
        volume_size_gib=volume_size_gib,
        dfs_repo_commit_id=dfs_repo_commit_id,
        external_data_volumes=[],
        cache=cache,
        cache_version="1.0",
        use_project_defaults_for_omitted=True
    )

    task3 = run_domino_job_task(
        flyte_task_name='Merge Data',
        command='python /mnt/code/scripts/merge-data.py',
        inputs=[
            Input(name='datasetA', type=FlyteFile[TypeVar('csv')], value=task1['datasetA']),
            Input(name='datasetB', type=FlyteFile[TypeVar('csv')], value=task2['datasetB'])],
        output_specs=[Output(name='merged_data', type=DataArtifact.File(name="merged_data.csv"))],
        environment_name=environment_name,
        #environment_revision_id=environment_revision_id,
        hardware_tier_name="Small",
        dataset_snapshots=[],
        main_git_repo_ref=GitRef(Type=GitRef_type, Value=GitRef_value),
        volume_size_gib=volume_size_gib,
        dfs_repo_commit_id=dfs_repo_commit_id,
        external_data_volumes=[],
        cache=cache,
        cache_version="1.0",
        use_project_defaults_for_omitted=True
    )

    task4 = run_domino_job_task(
        flyte_task_name='Process Data',
        command='python /mnt/code/scripts/process-data.py',
        inputs=[Input(name='merged_data', type=FlyteFile[TypeVar('csv')], value=task3['merged_data'])],
        output_specs=[Output(name='processed_data', type=FlyteFile[TypeVar('csv')])],
        environment_name=environment_name,
        #environment_revision_id=environment_revision_id,
        hardware_tier_name="Small",
        dataset_snapshots=[],
        main_git_repo_ref=GitRef(Type=GitRef_type, Value=GitRef_value),
        volume_size_gib=volume_size_gib,
        dfs_repo_commit_id=dfs_repo_commit_id,
        external_data_volumes=[],
        cache=cache,
        cache_version="1.0",
        use_project_defaults_for_omitted=True
    )

    task5 = run_domino_job_task(
        flyte_task_name='Train Model',
        command='python /mnt/code/scripts/train-model.py',
        inputs=[
            Input(name='processed_data', type=FlyteFile[TypeVar('csv')], value=task4['processed_data']),
            Input(name='num_estimators', type=int, value=100)],
        output_specs=[Output(name='model', type=ModelArtifact.File(name="model.pkl"))],
        environment_name=environment_name,
        #environment_revision_id=environment_revision_id,
        hardware_tier_name="Small",
        dataset_snapshots=[],
        main_git_repo_ref=GitRef(Type=GitRef_type, Value=GitRef_value),
        volume_size_gib=volume_size_gib,
        dfs_repo_commit_id=dfs_repo_commit_id,
        external_data_volumes=[],
        cache=cache,
        cache_version="1.0",
        use_project_defaults_for_omitted=True
    )

    return 
