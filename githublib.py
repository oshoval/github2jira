#!/usr/bin/env python3

import requests
import json
import time
from datetime import datetime

from common import get_envvar

SECONDS_PER_WEEK = 604800


class Github:
    def __init__(self, token, owner, repo, expected_label):
        self.owner = owner
        self.repo = repo
        self.expected_label = expected_label
        self.query_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        self.headers = {"Authorization": f"token {token}"}

    def get_issues(self, page):
        params = {"state": "open", "page": page, "per_page": "100"}

        r = requests.get(self.query_url, headers=self.headers, params=params)
        data = r.json()
        return data

    def check_labels(self, issue):
        if self.expected_label == "":
            return True
        for label in issue["labels"]:
            if label["name"] == self.expected_label:
                return True
        return False

    def check_time(self, issue, max_delta):
        epoch_time_now = int(time.time())
        TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
        epoch = int(
            datetime.strptime(issue["created_at"], TIME_FORMAT).timestamp()
        )
        return (epoch_time_now - epoch) < (max_delta * SECONDS_PER_WEEK)


def main():
    print("githublib self test")

    github_token = get_envvar("GITHUB_TOKEN")
    github_owner = get_envvar("GITHUB_OWNER")
    github_repo = get_envvar("GITHUB_REPO")

    github = Github(github_token, github_owner, github_repo, "")
    data = github.get_issues(1)
    print(json.dumps(data[0], sort_keys=True, indent=4))


if __name__ == "__main__":
    main()
