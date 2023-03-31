**Taken from the dezoomcamp GitHub repository due to usefulness for further learners:** <br> <br>

**Refresh service-account's auth-token for this session** <br>
```gcloud auth application-default login```

**Initialize state file (.tfstate)** <br>
```terraform init```

**Check changes to new infra plan** <br>
```terraform plan -var="project=<your-gcp-project-id>"```

**Create new infra** <br>
```terraform apply -var="project=<your-gcp-project-id>"```

**Delete infra after your work, to avoid costs on any running services** <br>
```terraform destroy```


**The script parts to regarding the service accounts was mainly inspired by [this](https://tech.serhatteker.com/post/2022-07/gcp-service-account-with-terraform/) solution by Serhat Teker.** :clap: