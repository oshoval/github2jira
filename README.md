# github2jira
Scrap github issues and create Jira tickets

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

2. Run `./create_ticket.py` in order to fetch github issues and create a ticket for them

## Running as k8s payload

### One time configuration: Build docker image for the script

1. Run `docker build -f Dockerfile -t <image> .`  
once its done, push it to your image repository, or rename and push to a local registry.

### Deploy as k8s payload

1. Create secret.txt with the exports from the section above (include the export command).

2. Create a configmap for the txt file
`kubectl create configmap git-token --from-file=secret.txt`

3. Deploy either a pod or a CronJob (see manifests folder).
