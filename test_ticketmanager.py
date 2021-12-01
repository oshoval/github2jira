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

from github2jira.ticketmanager import TicketManager, FLOOD_PROTECTION_LIMIT
from github2jira.githublib import Issue


class JiraMock:
    def __init__(self):
        self.counter = 0

    def issue_exists(self, git_issue):
        self.counter += 1
        return self.counter % 2 != 0

    def create_issue(self, git_issue):
        return


def test_ticketmanager_create():
    jira = JiraMock()
    ticket_manager = TicketManager(jira)

    raw_issue = {}
    raw_issue["html_url"] = "dummy"
    git_issue = Issue(raw_issue)

    issues_created = 0
    for i in range(FLOOD_PROTECTION_LIMIT * 3):
        ticket_manager.create(git_issue)

    assert ticket_manager.issues_created == FLOOD_PROTECTION_LIMIT
