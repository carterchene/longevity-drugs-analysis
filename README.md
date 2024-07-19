# DrugAge Explorer: Longevity Compound Analysis Pipeline

![Project Overview](path_to_overview_image.png)

## Project Overview

DrugAge Explorer is a comprehensive data engineering project that processes and visualizes data from the DrugAge database, focusing on compounds that affect lifespan in model organisms. This project demonstrates a full-stack data pipeline, from web scraping to data visualization, all orchestrated by Dagster.

### Key Features

- 🕷️ Web Scraping: Extracts data from genomics.senescence.info
- 🗃️ Data Storage: Utilizes DuckDB for efficient data handling
- 🧹 Data Transformation: Employs dbt for data cleaning and modeling
- ☁️ Cloud Integration: Loads data into Google BigQuery
- 📊 Data Visualization: Presents insights through a Streamlit app
- 🐳 Containerization: Dockerized for easy deployment
- ☁️ Cloud Hosting: Deployed on Azure App Service
- 🎭 Orchestration: Managed end-to-end with Dagster

## Architecture

![Architecture Diagram](path_to_architecture_diagram.png)

1. **Orchestration**: Dagster manages the entire data pipeline flow.
2. **Data Extraction**: Python scripts with Selenium scrape the DrugAge database.
3. **Local Storage**: Raw data is stored in DuckDB for initial processing.
4. **Data Transformation**: dbt models clean and transform the data.
5. **Cloud Storage**: Processed data is loaded into Google BigQuery.
6. **Visualization**: A Streamlit app queries BigQuery and presents interactive visualizations.
7. **Deployment**: The app is containerized with Docker and hosted on Azure App Service.

## Technologies Used

- Dagster (Orchestration)
- Python
- Selenium
- DuckDB
- dbt
- Google BigQuery
- Streamlit
- Docker
- Azure App Service

## Dagster Workflow

![Dagster DAG](path_to_dagster_dag.png)

Dagster orchestrates our entire data pipeline, providing:
- Asset-based data orchestration
- Dependency management between tasks
- Scheduling and triggering of data updates
- Monitoring and alerting
- Data lineage and observability

## Getting Started

(Include instructions for setting up and running the project locally, including Dagster setup)

## Data Insights

![Sample Visualization](path_to_sample_visualization.png)

(Brief description of key findings or interesting data points)

## Future Enhancements

- Implement automated data refresh pipeline using Dagster's scheduling
- Expand analysis to include more datasets from genomics.senescence.info
- Develop machine learning models for lifespan prediction
- Enhance Dagster observability with custom sensors and monitoring

## Contact

[Your Name] - [Your Email]

Project Link: [GitHub Repo URL]

Live Demo: [Streamlit App URL]
