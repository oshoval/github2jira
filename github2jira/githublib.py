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
from datetime import datetime

import requests

from github2jira.config import Config

SECONDS_PER_WEEK = 7 * 24 * 60 * 60
# max github pages to process
GITHUB_MAX_PAGES = 20
# process upto x weeks back
MAX_DELTA_WEEKS = 4


class GithubEnv:
    TOKEN = "GITHUB_TOKEN"
    OWNER = "GITHUB_OWNER"
    REPO = "GITHUB_REPO"
    LABEL = "GITHUB_LABEL"


_ENV_VAR_NAMES = [GithubEnv.TOKEN, GithubEnv.OWNER, GithubEnv.REPO, GithubEnv.LABEL]


def config():
    c = Config(_ENV_VAR_NAMES)
    c.Load()
    return c


class Issue:
    def __init__(self, issue):
        self._issue = issue

    @property
    def repo(self):
        return self._issue["html_url"].split("/")[4]

    @property
    def id(self):
        return self._issue["number"]

    @property
    def url(self):
        return self._issue["html_url"]

    @property
    def title(self):
        return self._issue["title"]

    @property
    def epoch(self):
        TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
        timestamp = self._issue["created_at"]
        return int(datetime.strptime(timestamp, TIME_FORMAT).timestamp())

    @property
    def raw_issue(self):
        return self._issue

    @property
    def labels(self):
        return [l["name"] for l in self._issue["labels"]]

    def __eq__(self, other):
        return self._issue == other._issue


class Github:
    def __init__(self, cfg):
        owner = cfg.vars[GithubEnv.OWNER]
        repo = cfg.vars[GithubEnv.REPO]
        self.query_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        self.headers = {"Authorization": f"token {cfg.vars[GithubEnv.TOKEN]}"}
        self.expected_label = cfg.vars[GithubEnv.LABEL]

    def issue_by_id(self, issue_id):
        r = requests.get(f"{self.query_url}/{issue_id}", headers=self.headers)
        issue = r.json()
        if issue.get("url", None) is None:
            return None
        return Issue(issue)

    def issues(self):
        return self._filter(self._open_issues())

    def _filter(self, issues):
        for issue in issues:
            if "pull" in issue.url:
                continue

            if self.expected_label in issue.labels and issue_in_time_window(
                issue, MAX_DELTA_WEEKS
            ):
                yield issue

    def _open_issues(self):
        for page in range(1, GITHUB_MAX_PAGES):
            params = {"state": "open", "page": page, "per_page": "100"}
            r = requests.get(self.query_url, headers=self.headers, params=params)
            issues = r.json()

            if len(issues) == 0:
                return

            for issue in issues:
                yield Issue(issue)


def issue_in_time_window(issue, max_delta_weeks):
    epoch = issue.epoch
    epoch_time_now = int(time.time())
    return (epoch_time_now - epoch) < (max_delta_weeks * SECONDS_PER_WEEK)
