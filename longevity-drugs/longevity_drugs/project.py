from pathlib import Path

from dagster_dbt import DbtProject

# this file creates the dbtproject object that we reference in the __init__.py dagster file

RELATIVE_PATH_TO_MY_DBT_PROJECT = "../longevity_dbt"

longevity_dbt = DbtProject(
    project_dir=Path(__file__)
    .joinpath("..", RELATIVE_PATH_TO_MY_DBT_PROJECT)
    .resolve(),
)
longevity_dbt.prepare_if_dev()
