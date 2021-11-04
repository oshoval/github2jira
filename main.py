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

import argparse

from github2jira.ticketmanager import TicketManager
import github2jira.jiralib as jiralib
import github2jira.githublib as githublib


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dryrun", default=False, action="store_true")
    parser.add_argument("--issue")
    args = parser.parse_args()

    jira = jiralib.Jira(jiralib.config())

    if args.dryrun:
        print("INFO: dryrun mode enabled")
        jira = jiralib.DryRunJira(jira)

    github = githublib.Github(githublib.config())
    ticket_manager = TicketManager(jira)

    if args.issue is None:
        create_jira_tickets(github, ticket_manager)
    else:
        create_jira_ticket(args.issue, github, ticket_manager)


def create_jira_tickets(github, ticket_manager):
    for issue in github.issues():
        ticket_manager.create(issue)


def create_jira_ticket(issue, github, ticket_manager):
    issue = github.issue_by_id(issue)
    if issue is not None:
        ticket_manager.create(issue)
    else:
        print("Issue not found")


if __name__ == "__main__":
    main()
