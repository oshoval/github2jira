#!/usr/bin/env python3

import requests
import os
import json
import sys
from datetime import datetime
import time

import jiralib

# process upto this x weeks back
max_delta_weeks = 4
SECONDS_PER_WEEK = 604800
# how many tickets can be opened on each cycle
flood_protection_limit = 3

def check_time(epoch_time_now, created_at, max_delta):
    epoch = int(datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ").timestamp())
    return epoch_time_now - epoch < max_delta

def process_issues(jira, repo, query_url, headers):
    issues_created = 0
    epoch_time_now = int(time.time())

    for n in range(1, 20):
        params = {
            "state": "open", "page" : n, "per_page": "100"
        }

        r = requests.get(query_url, headers=headers, params=params)
        data = r.json()

        if len(data) == 0:
            break

        #print(json.dumps(data, sort_keys=True, indent=4))
        for element in data:
            html_url = element["html_url"]
            id = element["number"]
            title = element["title"]

            if "pull" in html_url:
                continue

            is_network = False
            for label in element["labels"]:
                if label["name"] == "sig/network":
                    is_network = True
                    break
            
            if is_network:
                if jiralib.issue_exists(jira, "PG", id) == False:

                    if check_time(epoch_time_now, element["created_at"], max_delta_weeks*SECONDS_PER_WEEK) == False:
                        return
                       
                    print("creating issue for", element["html_url"], title)
                    res = jiralib.create_issue(jira, "PG", id, title, "link")
                    if res == True:
                        print(f"issue {id} created")
                        issues_created += 1
                        if issues_created == flood_protection_limit:
                            print("flood protection limit reached, exiting")
                            sys.exit(0)

def main():
    jira = jiralib.init()

    token = os.getenv('GITHUB_TOKEN')

    if token == None:
        print("Error: cant find GITHUB_TOKEN")
        sys.exit(1)

    owner = "kubevirt"
    repo = "kubevirt"
    query_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {'Authorization': f'token {token}'}

    process_issues(jira, repo, query_url, headers)

if __name__ == '__main__':
    main()






