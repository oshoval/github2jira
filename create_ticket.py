#!/usr/bin/env python3

import requests
import os
import json
import configparser
import sys

import jira

# cfg file name
cfg_file = 'status.cfg'
# process upto this id in case no status.cfg exists
last = '6300'
# how many tickets can be opened on each cycle
flood_protection_limit = 3

def init_db(config):
    global last
    try:
        last = config.get('DEFAULT', 'last')
    except configparser.NoOptionError:
        print("db doesn't exists, adding initial value")
        config['DEFAULT']['last'] = last
        with open(cfg_file, 'w') as configfile:
            config.write(configfile)

    return last

def update_db(config, last):
    config['DEFAULT']['last'] = last
    with open(cfg_file, 'w') as configfile:
        config.write(configfile)

def process_issues(owner, repo, query_url, headers):
    issues_created = 0

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

            if id <= int(last):
                return

            is_network = False
            for label in element["labels"]:
                if label["name"] == "sig/network":
                    is_network = True
                    break
            
            if is_network:
                #print(id, element["html_url"], title)
                if jira.issue_exists(repo, id) == False:
                    print("creating issue for", element["html_url"], title)
                    res = jira.create_issue(repo, id, title)
                    if res == True:
                        print(f"issue {id} created")
                        issues_created += 1
                        if issues_created == flood_protection_limit:
                            print("flood protection limit reached, exiting")
                            sys.exit(0)

def main():
    config = configparser.ConfigParser()
    config.read(cfg_file)
    last = init_db(config)

    token = os.getenv('GITHUB_TOKEN')

    if token == None:
        print("Error: cant find GITHUB_TOKEN")
        sys.exit(1)

    owner = "kubevirt"
    repo = "kubevirt"
    query_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {'Authorization': f'token {token}'}

    process_issues(owner, repo, query_url, headers)

if __name__ == '__main__':
    main()