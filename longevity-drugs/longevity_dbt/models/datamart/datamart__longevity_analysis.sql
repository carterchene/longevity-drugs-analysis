

-- this model will join to the species dimension which has the colloquial name for species rather than scientific name

with 

fact as (select * from {{ref('raw__drug_age_clean')}})

,dim as (select * from {{ref('species_dim')}})

select f.*, d.common_name
from fact f
left join dim d on f.species = d.species



