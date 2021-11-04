#!/usr/bin/env python3

import sys
import argparse

from common import get_envvar
from jiralib import Jira
from githublib import Github

# max github pages to process
GITHUB_MAX_PAGES = 20
# process upto x weeks back
max_delta_weeks = 4
# how many tickets can be opened on each cycle
flood_protection_limit = 3


def process_issue(jira, github, issue, dryrun):
    html_url = issue["html_url"]

    if "pull" in html_url:
        return False

    if not github.check_labels(issue):
        return False

    issue_id = issue["number"]
    if not jira.issue_exists(github.repo, issue_id):
        if not github.check_time(issue, max_delta_weeks):
            return False

        if not dryrun:
            created_issue = jira.create_issue(
                github.repo, issue_id, issue["title"], html_url
            )
            issue_url = f"{jira.server}/browse/{created_issue}"
            print(f"Created issue {issue_url} for {html_url}")
        else:
            print(f"Dry Run Created issue for {html_url}")
        return True
    else:
        print("Issue for", html_url, "already exists")

    return False


def loop(jira, github, dryrun):
    issues_created = 0

    for page in range(1, GITHUB_MAX_PAGES):
        issues = github.get_issues(page)
        if len(issues) == 0:
            break

        for issue in issues:
            res = process_issue(jira, github, issue, dryrun)
            if res:
                issues_created += 1
                if issues_created == flood_protection_limit:
                    print("Flood protection limit reached, exiting")
                    sys.exit(0)


def main():
    server = get_envvar("JIRA_SERVER")
    username = get_envvar("JIRA_USERNAME")
    token = get_envvar("JIRA_TOKEN")
    project = get_envvar("JIRA_PROJECT")
    project_id = get_envvar("JIRA_PROJECT_ID")
    jira_component = get_envvar("JIRA_COMPONENT")

    github_token = get_envvar("GITHUB_TOKEN")
    github_owner = get_envvar("GITHUB_OWNER")
    github_repo = get_envvar("GITHUB_REPO")
    github_label = get_envvar("GITHUB_LABEL")

    parser = argparse.ArgumentParser()
    parser.add_argument("--dryrun", default=False, action="store_true")
    args = parser.parse_args()

    if args.dryrun:
        print("INFO: dryrun mode enabled")

    github = Github(github_token, github_owner, github_repo, github_label)
    jira = Jira(server, username, token, project, project_id, jira_component)

    loop(jira, github, args.dryrun)


if __name__ == "__main__":
    main()
