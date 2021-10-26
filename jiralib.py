#!/usr/bin/env python3

import os
import sys

from jira import JIRA

class Jira:
    def __init__(self, server, email, project, project_id):
        self.project = project
        self.project_id = project_id
        self.server = server
        
        jira_token = os.getenv('JIRA_TOKEN')
        if jira_token == None:
            print("Error: cant find JIRA_TOKEN")
            sys.exit(1)
        
        jiraOptions = {'server': self.server}
        self.jira = JIRA(options = jiraOptions, basic_auth = (email, jira_token))

    def issue_exists(self, repo, id):
        query = f'project={self.project} AND text ~ "GITHUB:{repo}-{id}"'
        issues = self.jira.search_issues(query)
        return len(issues) != 0

    def create_issue(self, repo, issue_id, title, body):
        issue_dict=dict()
        issue_dict['project']=dict({'id':self.project_id})
        issue_dict['summary']=f"[GITHUB:{repo}-{issue_id}] {title}"
        issue_dict['description']=body
        issue_dict['issuetype']=dict({'name':'Task'})

        issue = self.jira.create_issue(issue_dict)
        return issue
                
def main():
    print("jiralib")
    jira = Jira("https://nmstate.atlassian.net", "oshoval@redhat.com", "PLAYG" , "10001")
    print(jira.issue_exists("kubevirt", "6500"))

if __name__ == '__main__':
    main()