select
    compound,
    avg(avg_lifespan_change) as avg_lifespan_change,
    median(avg_lifespan_change) as median_lifespan_change,
    stddev(avg_lifespan_change) as stddev_lifespan_change
from {{ ref('raw__drug_age_clean') }}
group by compound