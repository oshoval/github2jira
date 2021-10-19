# github2jira
Scrap github issues and create Jira tickets

1. Create github token https://github.com/settings/tokens
2. `export GITHUB_TOKEN="your_token"`
3. Run `./create_ticket.py` in order to list sig/network issues

# Build docker image for the script

1. Run `docker build -f Dockerfile -t quay.io/oshoval/github:latest .`
once its done, push it to quay, or rename and push a local registry.

# Run as k8s payload

1. Create secret.txt with the following contents
`export GITHUB_TOKEN=<GIT_TOKEN>`

2. Create a configmap for the txt file
`kubectl create configmap git-token --from-file=secret.txt`

3. Create a pod (good for testing)
```
apiVersion: v1
kind: Pod
metadata:
  name: github
  namespace: default
spec:
  containers:
  - image: quay.io/oshoval/github:latest
    name: github
    command:
    - /bin/bash
    - -c
    - sleep infinity
    volumeMounts:
      - name: configs
        mountPath: /app/secret.txt
        subPath: secret.txt
  volumes:
     - name: configs
       configMap:
         name: git-token
```

or a CronJob
```
apiVersion: batch/v1
kind: CronJob
metadata:
  name: cron-github
spec:
  schedule: "0 */1 * * *"
  successfulJobsHistoryLimit: 1
  failedJobsHistoryLimit: 1
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: github
            image: quay.io/oshoval/github:latest
            imagePullPolicy: IfNotPresent
            command:
            - /bin/sh
            - -c
            - date; source /app/secret.txt; ./github2jira/create_ticket.py 
            volumeMounts:
              - name: configs
                mountPath: /app/secret.txt
                subPath: secret.txt
          restartPolicy: Never
          volumes:
            - name: configs
              configMap:
                name: git-token
```
