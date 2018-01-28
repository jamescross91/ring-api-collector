## Ring API Collector
Lambda function to query the Ring API and put data in a DyanmoDB table for later querying plus an API for querying it

### Deployment
Expects a `secrets.yml` in the root directory file containing your Ring.com username and password formatted like this:
```
USER: emailaddress@gmail.com
PASS: ringpassword
```

You can test locally with `serverless invoke local -f collect`.  When you're ready to deploy the stack run `serverless deploy -v`

