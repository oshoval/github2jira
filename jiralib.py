#!/usr/bin/env python3

import os

from jira import JIRA

def issue_exists(jira, repo, id):
    query = f'project=PLAYG AND text ~ "GITHUB:{repo}-{id}"'
    issues = jira.search_issues(query)
    return len(issues) != 0

def create_issue(jira, repo, issue_id, title, link):
    issue_dict=dict()
    issue_dict['project']=dict({'id':'10001'})
    issue_dict['summary']=f"[GITHUB:{repo}-{issue_id}] {title}"
    issue_dict['description']=link
    issue_dict['issuetype']=dict({'name':'Task'})

    issue = jira.create_issue(issue_dict)
    print(issue) # TODO know to return link to new issue
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