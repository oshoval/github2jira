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

import time
import requests

from datetime import datetime

from config import Config

SECONDS_PER_WEEK = 604800
# max github pages to process
GITHUB_MAX_PAGES = 20
# process upto x weeks back
MAX_DELTA_WEEKS = 4


class GithubConfig(Config):
    def __init__(self):
        super().__init__(
            ["GITHUB_TOKEN", "GITHUB_OWNER", "GITHUB_REPO", "GITHUB_LABEL"]
        )


class Issue:
    @staticmethod
    def filter(issue, expected_label):
        if expected_label == "":
            return True
        for label in issue["labels"]:
            if label["name"] == expected_label:
                return True
        return False

    @staticmethod
    def age_relevant(issue, max_delta):
        epoch_time_now = int(time.time())
        TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
        timestamp = issue["created_at"]
        epoch = int(datetime.strptime(timestamp, TIME_FORMAT).timestamp())
        return (epoch_time_now - epoch) < (max_delta * SECONDS_PER_WEEK)


class Github:
    def __init__(self, cfg):
        self.owner = cfg.vars["GITHUB_OWNER"]
        self.repo = cfg.vars["GITHUB_REPO"]
        self.expected_label = cfg.vars["GITHUB_LABEL"]
        self.query_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/issues"
        self.headers = {"Authorization": f"token {cfg.vars['GITHUB_TOKEN']}"}

    def issues(self):
        for page in range(1, GITHUB_MAX_PAGES):
            params = {"state": "open", "page": page, "per_page": "100"}
            r = requests.get(self.query_url, headers=self.headers, params=params)
            issues = r.json()

            if len(issues) == 0:
                return

            for issue in issues:
                if "pull" in issue["html_url"]:
                    continue

                if Issue.filter(issue, self.expected_label) and Issue.age_relevant(
                    issue, MAX_DELTA_WEEKS
                ):
                    yield (issue)
