#!/usr/bin/env python3

import os
import json
import sys
from datetime import datetime
import time

from jiralib import Jira
from githublib import Github

# process upto this x weeks back
max_delta_weeks = 4
SECONDS_PER_WEEK = 604800
# how many tickets can be opened on each cycle
flood_protection_limit = 3

# Github source
owner = "kubevirt"
repo = "kubevirt"

# Jira target
server = "https://nmstate.atlassian.net"
email = "oshoval@redhat.com"
project = "PLAYG"
project_id = "10001"

debug = 0

def check_time(epoch_time_now, created_at, max_delta):
    epoch = int(datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ").timestamp())
    return epoch_time_now - epoch < max_delta

def process_issue(jira, github, issue):
    html_url = issue["html_url"]
    issue_id = issue["number"]
    title = issue["title"]

    if "pull" in html_url:
        return False

    is_network = False
    for label in issue["labels"]:
        if label["name"] == "sig/network":
            is_network = True
            break

    if is_network == False:
        return False

    epoch_time_now = int(time.time())
    if jira.issue_exists(github.repo, issue_id) == False:
        if check_time(epoch_time_now, issue["created_at"], max_delta_weeks*SECONDS_PER_WEEK) == False:
            return False

        created_issue = jira.create_issue(github.repo, issue_id, title, issue["html_url"])
        print(f'Created issue {jira.server}/browse/{created_issue} for {issue["html_url"]}')
        return True
    else:
        print("Issue for", issue["html_url"], "already exists")

    return False

def loop(jira, github):
    issues_created = 0

    for page in range(1, 20):
        issues = github.get_issues(page)
        if len(issues) == 0:
            break

        if debug:
            print(json.dumps(issues, sort_keys=True, indent=4))

        for issue in issues:
            res = process_issue(jira, github, issue)
            if res == True:
                issues_created += 1
                if issues_created == flood_protection_limit:
                    print("Flood protection limit reached, exiting")
                    sys.exit(0)

def main():
    jira = Jira(server, email, project, project_id)
    github = Github(owner, repo)

    loop(jira, github)

if __name__ == '__main__':
    main()






