import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import duckdb

st.set_page_config(
    layout='wide'
)
st.title("Drug Age Longevity Analysis")
st.write("This Streamlit app analyzes data from https://genomics.senescence.info/")

# Load the dataset
database_location = r'C:\Users\Carter Dakota\portfolio\longevity-drugs-analysis\longevity-drugs\duckdb_database\drug_age.db'
database_location = '/usr/src/app/drug_age.db'
with duckdb.connect(database=database_location) as con:
    query = 'SELECT * FROM datamart.longevity_analysis'
    drug_age_data = con.execute(query).df()

drug_age_data['dosage'] = drug_age_data['dosage'].astype(str)

### create filters
species_list = drug_age_data['common_name'].unique()
compound_list = drug_age_data['compound_formulation'].unique().tolist()

col1,col3, col2 = st.columns([2,0.2,2])

with col1:
    subcol1, subcol2 = st.columns([1,1])

    with subcol1:
        selected_species = st.selectbox('Select Species', species_list)

    with subcol2: 
        selected_num_interventions = st.number_input('Limit: ', step=1, value=10)

    filtered_data = drug_age_data[drug_age_data['common_name'] == selected_species]

    # Plotting average and maximum lifespan changes by compound
    st.subheader(f"Top {selected_num_interventions} Interventions: Average and Maximum Lifespan Change by Compound")
    fig, ax = plt.subplots(figsize=(12, 6))
    top_10_compounds = filtered_data.groupby('compound_formulation')[['avg_med_lifespan_change_percent', 'max_lifespan_change_percent']].mean().sort_values('avg_med_lifespan_change_percent', ascending=False).head(selected_num_interventions)
    top_10_compounds.plot(kind='barh', width=0.8, ax=ax)
    ax.set_title('Top 10 Interventions: Average and Maximum Lifespan Change by Compound')
    ax.set_ylabel('Compound Formulation')
    ax.set_xlabel('Lifespan Change Percent')
    ax.legend(['Average Lifespan Change', 'Maximum Lifespan Change'])
    plt.yticks(rotation=0)
    st.pyplot(fig)

with col2: 
    # default to resveratrol cuz has lots of experiments
    indx = compound_list.index('Resveratrol')
    selected_compound = st.selectbox('Select Compound', compound_list, index=indx)

    compound_data = drug_age_data[drug_age_data['compound_formulation'] == selected_compound]

    

    # Plotting average and maximum lifespan changes by compound
    st.subheader(f"Species lifespan change when given {selected_compound}")
    fig, ax = plt.subplots(figsize=(12, 6))
    top_10_compounds = compound_data.groupby('common_name')[['avg_med_lifespan_change_percent', 'max_lifespan_change_percent']].mean().sort_values('avg_med_lifespan_change_percent', ascending=False)
    top_10_compounds.plot(kind='barh', width=0.8, ax=ax)
    ax.set_title('Lifespan Effect by Species for a given compound')
    ax.set_ylabel('Species')
    ax.set_xlabel('Lifespan Change Percent')
    ax.legend(['Average Lifespan Change', 'Maximum Lifespan Change'])
    plt.yticks(rotation=0)
    st.pyplot(fig)