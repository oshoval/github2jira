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

from jiralib import Jira
from githublib import Github

# how many tickets can be opened on each cycle
FLOOD_PROTECTION_LIMIT = 3


class Ticket:
    def __init__(self, github_config, jira_config, dryrun):
        self.dryrun = dryrun
        self.issues_created = 0
        self.github = Github(github_config)
        self.jira = Jira(jira_config)

    def create_jira_issue(self, issue):
        issue_id = issue["number"]
        html_url = issue["html_url"]
        if not self.jira.issue_exists(self.github.repo, issue_id):
            if not self.dryrun:
                created_issue = self.jira.create_issue(self.github.repo, issue)
                issue_url = f"{self.jira.server}/browse/{created_issue}"
                print(f"Created issue {issue_url} for {html_url}")
            else:
                print(f"Dry Run Created issue for {html_url}")

            self.issues_created += 1
        else:
            print("Issue for", html_url, "already exists")

    def flood_protection_reached(self):
        return self.issues_created == FLOOD_PROTECTION_LIMIT
