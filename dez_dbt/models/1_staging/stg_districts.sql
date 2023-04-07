{{ config(
    materialized='table',
    alias='stg_districts',
    labels = {'layer': 'staging'}
) }}

/* 
    - this model casts all columns to the expected datatypes
    - the columns names remain as this shows the "source view" of the data
*/

with source_data as (

    select
        cast(ags as string) as ags
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
        , cast(delta_weekIncidence as FLOAT64) as delta_weekIncidence
        , cast(_inserted_at as timestamp) as _inserted_at
    from 
        {{ source('rki', 'districts') }}
        --`de_zoomcamp_2023_project_dataset.districts`
    where
        ags is not null

)

select *
from source_data