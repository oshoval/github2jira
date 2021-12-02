# github2jira
github2jira automates mirroring of github issues to Jira tickets.

The tool scans github for issues that match the desired criteria,
and for each one of them creates a Jira ticket (unless it already exists).

## One time configuration
1. Create github token https://github.com/settings/tokens, refer it as `GITHUB_TOKEN`
2. Make sure you have a Jira bot access (either a user:pass or user:token), refer as `JIRA_USERNAME`,`JIRA_TOKEN`
3. Get your Jira project id, refer as `JIRA_PROJECT_ID`  
`curl -s -u JIRA_USERNAME:JIRA_TOKEN -X GET -H "Content-Type: application/json" <JIRA_SERVER>/rest/api/latest/project/<JIRA_PROJECT> | jq .id`

## Running manually

1. export the following envvars:
```
export JIRA_SERVER=<..> # for example https://nmstate.atlassian.net
export JIRA_PROJECT=<..> # name of the Jira project (ticket names are JIRA_PROJECT-#)
export JIRA_PROJECT_ID=<..> # see "One time configuration" section
export JIRA_COMPONENT=<..> # which component to set in the created tickets
export GITHUB_OWNER=<..> # the x of https://github.com/x/y
export GITHUB_REPO=<..> # the y of https://github.com/x/y
export GITHUB_LABEL=<..> # which label to filter

export JIRA_USERNAME=<..> # see "One time configuration" section
export JIRA_TOKEN=<..> # see "One time configuration" section
export GITHUB_TOKEN=<..> # see "One time configuration" section
```

For Jira basic auth set `JIRA_USERNAME=<USER>`, `JIRA_TOKEN<PASSWORD/TOKEN>`  
For Jira Personal Access Token set `JIRA_USERNAME=""`, `JIRA_TOKEN=<PAT>`

2. Run `./main.py` in order to fetch github issues and create a ticket for them

### Additional settings

`dryrun`: Use `./main.py --dryrun` in order to run the tool in dryrun mode.
dryrun mode will fetch github issues, and report what Jira tickets it would create,
but without creating them.

`--issue`: Use `./main.py --issue=<issue_id>` in order to create an issue for
a specified issue id.
No additional checks are performed in this case.

## Running as k8s payload

In order to have a fully automated mirroring process,
it is suggested to run the tool as a cron jon.

One of the methods to achieve it, is to run it as k8s CronJob payload.

### One time configuration: Build docker image for the script

1. From the project folder, run `docker build -f Dockerfile -t <image> .`  
once its done, push it to your image repository, or rename and push to a local registry.

### Deploy as k8s payload

1. Create secret.txt with the exports from the section above (include the export command).

2. Create a configmap or a secret with the needed variables.

configmap:

`kubectl create configmap github2jira-secret --from-file=secret.txt`  
Where secret.txt is a file in the format (see section above)
```
export JIRA_SERVER=<..>
```

secret:

Create a secret in the format:
```
apiVersion: v1
kind: Secret
metadata:
  name: github2jira-secret
type: Opaque
data:
  # list of all the env vars in the format:
  # ENV_VAR_NAME:BASE64_VALUE
```

Note:
In order to ease base64 encoding you can use the following command  
`cat secret.in | awk -F= '{printf("  "$1": "); system("echo -n " $2"| base64")}'`  
where `secret.in` is a list of `NAME=VALUE`, one per line.  
Empty lines are not allowed.  
The character `=` is not allowed as part of the VALUE.

It will print the data section that you can use as part of your secret.

3. Deploy either a pod or a CronJob (see [manifests](manifests) folder).  
There are two types of CronJobs, one for configmap and one for secret.

