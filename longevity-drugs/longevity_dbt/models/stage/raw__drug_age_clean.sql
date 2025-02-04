
with raw_data as    (
    SELECT
        "Compound/Formulationx" AS compound_formulation,
        "Speciesx" AS species,
        "Avg/Med Lifespan Change (%)-96267.9-96267.9x" AS avg_med_lifespan_change_percent,
        "Max Lifespan Change (%)-94.993-94.993x" AS max_lifespan_change_percent,
        "Strainx" AS strain,
        "Dosagex" AS dosage,
        "Significant?NNDYx" AS is_significant,
        "Referencex" AS reference
    from {{source('raw','drug_age')}}

)

,exclude_nulls as (
    select *
    from raw_data
    where 1=1
    and compound_formulation is not null
    and species is not null

)

select * from exclude_nulls


