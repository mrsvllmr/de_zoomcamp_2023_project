# Topic and thought memory

- [x] Terraform (to create the GCP resources)
    - [x] main.tf <br>
    - [x] variables.tf <br>
    - [x] README.md <br>
- [ ] Script to create GCP Service Account and to create/set the roles needed (shoutout to https://github.com/MikhailKuklin/data-pipeline-COVID19-monitoring/blob/main/scripts/create_service_account.sh)

*Tomorrow*
    *- Compare sh script solution in "alternatives" to the current solution and use the best one (especially regarding the missing step of downloading/adding the json service account key to GOOGLE_APPLICATION_CREDENTIALS for authentication with Google Cloud SDK - seems to be easier with/included in the sh script solution*
    *- Check the order of the steps and check optimisation/simplification possibilities (regarding README / How to make it work)*
    ([from my point of view good solution for comparison](https://github.com/MikhailKuklin/data-pipeline-COVID19-monitoring/blob/main/prerequisites_readme.md)) <br> <br>

- [ ] Adding a CI CD pipeline, if applicable (see https://github.com/MikhailKuklin/data-pipeline-COVID19-monitoring/blob/main/.github/workflows/GHA.yml for a nice solution!)
- [ ] Possibly in a first step just a csv source; at an later stage then swtich to json files to learn how to deal with them via Python
- [ ] Save source data in parquet format in data lake
- [ ] Add unit test (see )
- [ ] Make sure following steps only run if the previous step(s) had been successfull
- [ ] Incremental load already in datalake (?)
- [ ] Partition the data within BigQuery (clustering might not be necessary)
- [ ] Check once again if all keys to be downloaded/uploaded are described correctly (no duplicates with commands etc.)
- [ ] Next step: Spark (batch and/or streaming)
- [ ] Check formerly added sections in README.md and compare to the new ones

> Note to me: specify next time with regard to the steps already implemented