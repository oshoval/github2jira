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

import sys

import argparse

from ticket import Ticket
from jiralib import JiraConfig
from githublib import GithubConfig


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dryrun", default=False, action="store_true")
    args = parser.parse_args()

    if args.dryrun:
        print("INFO: dryrun mode enabled")

    github_config = GithubConfig()
    assert github_config.Load()

    jira_config = JiraConfig()
    assert jira_config.Load()

    ticket = Ticket(github_config, jira_config, args.dryrun)

    for issue in ticket.github.issues():
        ticket.create_jira_issue(issue)
        if ticket.flood_protection_reached():
            print("Flood protection limit reached, exiting")
            sys.exit(0)


if __name__ == "__main__":
    main()
