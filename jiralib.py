#!/usr/bin/env python3

from jira import JIRA

from common import get_envvar


class Jira:
    def __init__(self,
                 server,
                 username,
                 token,
                 project,
                 project_id,
                 component):
        self.project = project
        self.project_id = project_id
        self.server = server
        self.component = component

        jiraOptions = {"server": self.server}
        self.jira = JIRA(options=jiraOptions, basic_auth=(username, token))

    def issue_exists(self, repo, id):
        query = f'project={self.project} AND text ~ "GITHUB:{repo}-{id}"'
        issues = self.jira.search_issues(query)
        return len(issues) != 0

    def create_issue(self, repo, issue_id, title, body):
        issue_dict = dict()
        issue_dict["project"] = dict({"id": self.project_id})
        issue_dict["summary"] = f"[GITHUB:{repo}-{issue_id}] {title}"
        issue_dict["description"] = body
        issue_dict["issuetype"] = dict({"name": "Task"})
        if self.component != "":
            issue_dict["components"] = [dict({"name": self.component})]

        issue = self.jira.create_issue(issue_dict)
        return issue


def main():
    print("jiralib self test")

    server = get_envvar("JIRA_SERVER")
    username = get_envvar("JIRA_USERNAME")
    token = get_envvar("JIRA_TOKEN")
    project = get_envvar("JIRA_PROJECT")
    project_id = get_envvar("JIRA_PROJECT_ID")
    jira_component = get_envvar("JIRA_COMPONENT", "")

    jira = Jira(server, username, token, project, project_id, jira_component)
    res = jira.issue_exists("kubevirt", "123")
    if not res:
        raise AssertionError()
    print("OK")


if __name__ == "__main__":
    main()
