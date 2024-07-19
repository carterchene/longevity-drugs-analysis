select
    species,
    avg(avg_med_lifespan_change_percent) as avg_med_lifespan_change_percent,
    median(max_lifespan_change_percent) as max_lifespan_change_percent,
    stddev(avg_med_lifespan_change_percent) as stddev_lifespan_change
from {{ ref('raw__drug_age_clean') }}
group by species

