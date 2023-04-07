{% snapshot br_districts %}

{{ config(
    target_database='bright-aloe-381618',
    target_schema='de_zoomcamp_2023_project_dataset',
    alias='br_districts',
    labels = {'layer': 'bronze'},

    strategy='check',
    check_cols=['name', 'county', 'population', 'cases', 'deaths', 'casesPerWeek', 'deathsPerWeek', 'stateAbbreviation', 'recovered', 'weekIncidence', 'casesPer100k', 'delta_cases', 'delta_deaths', 'delta_recovered', 'delta_weekIncidence'],
    unique_key='allgemeiner_gemeinde_schluessel',
) }}

/* 
    - this model renames some columns to more understandable "business view"
*/

with source_data as (

    select
        cast(ags as string) as allgemeiner_gemeinde_schluessel
        , cast(name as string) as name
        , cast(county as string) as county
        , cast(population as numeric) as population
        , cast(cases as numeric) as cases
        , cast(deaths as INT64) as deaths
        , cast(casesPerWeek as INT64) as casesPerWeek
        , cast(deathsPerWeek as INT64) as deathsPerWeek
        , cast(stateAbbreviation as string) as stateAbbreviation
        , cast(recovered as numeric) as recovered
        , cast(weekIncidence as FLOAT64) as weekIncidence
        , cast(casesPer100k as FLOAT64) as casesPer100k
        , cast(delta_cases as INT64) as delta_cases
        , cast(delta_deaths as INT64) as delta_deaths
        , cast(delta_recovered as INT64) as delta_recovered
        , FORMAT('%f', delta_weekIncidence) as delta_weekIncidence
    from 
        {{ ref('stg_districts') }}

)

select *
from source_data

{% endsnapshot %}