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

# how many tickets can be opened on each cycle
FLOOD_PROTECTION_LIMIT = 3


class TicketManager:
    def __init__(self, jira):
        self.issues_created = 0
        self.jira = jira

    def create(self, issue):
        if not self.jira.issue_exists(issue):
            if self._flood_protection_reached():
                print("Flood protection reached, skipping creation of", issue.url)
                return

            self.jira.create_issue(issue)
            self.issues_created += 1
        else:
            print("Issue for", issue.url, "already exists")

    def _flood_protection_reached(self):
        return self.issues_created == FLOOD_PROTECTION_LIMIT
