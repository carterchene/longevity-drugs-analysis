from dagster import Definitions, load_assets_from_modules, define_asset_job, AssetSelection, ScheduleDefinition
from dagster_dbt import DbtCliResource
from dagster_duckdb import DuckDBResource
from dagster_gcp import BigQueryResource

from . import assets
from .project import longevity_dbt
from .assets import my_dbt_assets

all_assets = load_assets_from_modules([assets])

scrape_drug_age_job = define_asset_job("scrape_drug_age_job", selection=AssetSelection.all()) # creating a single job which materializes all assets

scrape_drug_age_schedule = ScheduleDefinition(
    job=scrape_drug_age_job,
    cron_schedule = '0 0 1 * *' # once per month
)

defs = Definitions(
    assets=all_assets,
    resources={
        "duckdb": DuckDBResource(database='../duckdb_database/drug_age.db'),
        "dbt": DbtCliResource(project_dir=longevity_dbt), # this makes dagster aware of my dbt project
        "bigquery": BigQueryResource(
            project="longevity-analysis",
        )
    },
    schedules=[scrape_drug_age_schedule],
)
