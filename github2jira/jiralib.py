# This file is part of the github2jira project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright 2021 Red Hat, Inc.
#

import json

from jira import JIRA

from github2jira.config import Config


class JiraEnv:
    SERVER = "JIRA_SERVER"
    USERNAME = "JIRA_USERNAME"
    TOKEN = "JIRA_TOKEN"
    PROJECT = "JIRA_PROJECT"
    PROJECT_ID = "JIRA_PROJECT_ID"
    COMPONENT = "JIRA_COMPONENT"


_ENV_VAR_NAMES = [
    JiraEnv.SERVER,
    JiraEnv.USERNAME,
    JiraEnv.TOKEN,
    JiraEnv.PROJECT,
    JiraEnv.PROJECT_ID,
    JiraEnv.COMPONENT,
]


def config():
    c = Config(_ENV_VAR_NAMES)
    c.Load()
    return c


class Jira:
    def __init__(self, cfg):
        self.project = cfg.vars[JiraEnv.PROJECT]
        self.project_id = cfg.vars[JiraEnv.PROJECT_ID]
        self.server = cfg.vars[JiraEnv.SERVER]
        self.component = cfg.vars[JiraEnv.COMPONENT]

        if cfg.vars[JiraEnv.USERNAME] != "":
            self.jira = JIRA(
                server=self.server,
                basic_auth=(cfg.vars[JiraEnv.USERNAME], cfg.vars[JiraEnv.TOKEN]),
            )
        else:
            headers = JIRA.DEFAULT_OPTIONS["headers"].copy()
            headers["Authorization"] = f"Bearer {cfg.vars[JiraEnv.TOKEN]}"
            self.jira = JIRA(server=self.server, options={"headers": headers})

    def issue_exists(self, git_issue):
        repo = git_issue.repo
        id = git_issue.id
        query = f'project={self.project} AND text ~ "GITHUB:{repo}-{id}"'
        issues = self.jira.search_issues(query)
        return len(issues) != 0

    def create_issue(self, git_issue):
        issue_data = self._create_issue_data(git_issue)
        created_issue = self.jira.create_issue(issue_data)

        issue_url = f"{self.server}/browse/{created_issue}"
        print(f"Created issue {issue_url} for {git_issue.url}")

    def _create_issue_data(self, git_issue):
        issue_data = {
            "project": {"id": self.project_id},
            "summary": f"[GITHUB:{git_issue.repo}-{git_issue.id}] {git_issue.title}",
            "description": git_issue.url,
            "issuetype": {"name": "Task"},
        }

        if self.component != "":
            issue_data["components"] = [{"name": self.component}]

        return issue_data


class DryRunJira:
    def __init__(self, jira):
        self.jira = jira

    def issue_exists(self, git_issue):
        return self.jira.issue_exists(git_issue)

    def create_issue(self, git_issue):
        json_data = json.dumps(
            self.jira._create_issue_data(git_issue), sort_keys=True, indent=4
        )
        print(f"Dryrun would create the following for {git_issue.url}\n{json_data}")
