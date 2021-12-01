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

import os
from unittest import mock

import responses

import github2jira.githublib as githublib
import tests.data as data


def mockenv(**envvars):
    return mock.patch.dict(os.environ, envvars)


def test_issue_properties():
    raw = data.raw_issue()
    issue = githublib.Issue(raw)

    assert issue.repo == data.REPO
    assert issue.id == raw["number"]
    assert issue.url == raw["html_url"]
    assert issue.title == raw["title"]
    assert issue.labels == ["sig/network", "sig/compute"]

    assert githublib.issue_in_time_window(issue, 1)
    assert not githublib.issue_in_time_window(issue, 0.2)


@mockenv(
    GITHUB_TOKEN="dummy",
    GITHUB_OWNER="owner",
    GITHUB_REPO="repo",
    GITHUB_LABEL="sig/network",
)
@responses.activate
def test_githublib_issues():
    github = githublib.Github(githublib.config())

    entry1 = data.raw_issue()
    entry2 = data.raw_issue()
    entry2["html_url"] = "https://github.com/kubevirt/kubevirt/issues/11"
    entry3 = data.raw_issue()
    entry3["labels"][0]["name"] = "sig/na"
    entry3["html_url"] = "https://github.com/kubevirt/kubevirt/issues/12"
    entry4 = data.raw_issue()
    entry4["html_url"] = "https://github.com/kubevirt/kubevirt/issues/13"

    responses.add(responses.GET, github.query_url, json=[entry1, entry2], status=200)
    responses.add(responses.GET, github.query_url, json=[entry3], status=200)
    responses.add(responses.GET, github.query_url, json=[entry4], status=200)
    responses.add(responses.GET, github.query_url, json=[], status=200)

    issues = list(github.issues())

    assert [
        githublib.Issue(entry1).raw_issue,
        githublib.Issue(entry2).raw_issue,
        githublib.Issue(entry4).raw_issue,
    ] == [issue.raw_issue for issue in issues]


@mockenv(
    GITHUB_TOKEN="dummy",
    GITHUB_OWNER="owner",
    GITHUB_REPO="repo",
    GITHUB_LABEL="sig/network",
)
@responses.activate
def test_githublib_issue_by_id_found():
    github = githublib.Github(githublib.config())

    entry = data.raw_issue()
    issue_id = 777
    responses.add(
        responses.GET, f"{github.query_url}/{issue_id}", json=entry, status=200
    )

    assert github.issue_by_id(issue_id).raw_issue == entry


@mockenv(
    GITHUB_TOKEN="dummy",
    GITHUB_OWNER="owner",
    GITHUB_REPO="repo",
    GITHUB_LABEL="sig/network",
)
@responses.activate
def test_githublib_issue_by_id_not_found():
    github = githublib.Github(githublib.config())

    issue_id_na = 1
    responses.add(
        responses.GET,
        f"{github.query_url}/{issue_id_na}",
        json={"message": "Not Found"},
        status=200,
    )

    assert github.issue_by_id(issue_id_na) is None
