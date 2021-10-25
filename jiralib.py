#!/usr/bin/env python3

import os

from jira import JIRA

def issue_exists(repo, id):
    query = f"[Git:{repo}-{id}]"
    return False

def create_issue(repo, id, title):
    # TODO know to return link to new issue
    return True

def init():
    jira_token = os.getenv('JIRA_TOKEN')

    if jira_token == None:
        print("Error: cant find JIRA_TOKEN")
        sys.exit(1)
    
    jiraOptions = {'server': "https://nmstate.atlassian.net"}
    
    jira = JIRA(options = jiraOptions, 
                basic_auth = ("oshoval@redhat.com", jira_token))

    return jira

def main():
    print("hello jira")

if __name__ == '__main__':
    main()