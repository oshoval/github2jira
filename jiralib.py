#!/usr/bin/env python3
#
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

from jira import JIRA

from config import Config


class JiraConfig(Config):
    def __init__(self):
        super().__init__(
            [
                "JIRA_SERVER",
                "JIRA_USERNAME",
                "JIRA_TOKEN",
                "JIRA_PROJECT",
                "JIRA_PROJECT_ID",
                "JIRA_COMPONENT",
            ]
        )


class Jira:
    def __init__(self, cfg):
        self.project = cfg.vars["JIRA_PROJECT"]
        self.project_id = cfg.vars["JIRA_PROJECT_ID"]
        self.server = cfg.vars["JIRA_SERVER"]
        self.component = cfg.vars["JIRA_COMPONENT"]

        jiraOptions = {"server": self.server}
        self.jira = JIRA(
            options=jiraOptions,
            basic_auth=(cfg.vars["JIRA_USERNAME"], cfg.vars["JIRA_TOKEN"]),
        )

    def issue_exists(self, repo, id):
        query = f'project={self.project} AND text ~ "GITHUB:{repo}-{id}"'
        issues = self.jira.search_issues(query)
        return len(issues) != 0

    def create_issue(self, repo, issue):
        issue_id = issue["number"]
        title = issue["title"]
        body = issue["html_url"]

        issue_dict = dict()
        issue_dict["project"] = dict({"id": self.project_id})
        issue_dict["summary"] = f"[GITHUB:{repo}-{issue_id}] {title}"
        issue_dict["description"] = body
        issue_dict["issuetype"] = dict({"name": "Task"})
        if self.component != "":
            issue_dict["components"] = [dict({"name": self.component})]

        issue = self.jira.create_issue(issue_dict)
        return issue
