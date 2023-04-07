{{ config(
    alias='go_districts',
    labels = {'layer': 'gold'}
) }}

/* 
    - this model selects directly from the bronze layer
    - only the latest version for each unique keyis selected
    - only needed columns are selected, ordering was added
    - renaming to german column names
    - further transformation/levels were not inserted here due to time constraints
*/

with cte_sum_tode as (
    select
        sum(deaths) as SummeTode
    from 
        {{ ref('br_districts') }}
    where
        dbt_valid_to is null
)

,cte_sum_bevoelkerung as (
    select
        sum(population) as SummeBevoelkerung
    from 
        {{ ref('br_districts') }}
    where
        dbt_valid_to is null
)

select
    name as Name
    , stateAbbreviation as Bundesland
    , county as Kreis
    , population as Bevoelkerung
    , round(population / SummeBevoelkerung * 100,4) as AnteilAnSumBevoelkerung
    , cases as Faelle
    , deaths as Tode
    , round(deaths / SummeTode * 100,4) as AnteilAnSumTode
    , recovered as Genesen
    , casesPer100k as FallePro100k
from {{ ref('br_districts') }}
left join cte_sum_tode on 1=1
left join cte_sum_bevoelkerung on 1=1
where
    dbt_valid_to is null
order by 
    AnteilAnSumTode desc