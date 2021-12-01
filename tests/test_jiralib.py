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

import pytest

from github2jira.githublib import Issue
import tests.data as data
from github2jira.jiralib import Jira, config, JiraEnv


def mockenv(**envvars):
    return mock.patch.dict(os.environ, envvars)


@pytest.fixture
def JiraMock(monkeypatch):
    def mock_init(self, cfg):
        self.project = cfg.vars[JiraEnv.PROJECT]
        self.project_id = cfg.vars[JiraEnv.PROJECT_ID]
        self.server = cfg.vars[JiraEnv.SERVER]
        self.component = cfg.vars[JiraEnv.COMPONENT]
        self.Jira = None

    monkeypatch.setattr(Jira, "__init__", mock_init)


@mockenv(
    JIRA_SERVER="dummy",
    JIRA_USERNAME="dummy",
    JIRA_TOKEN="dummy",
    JIRA_PROJECT="dummy",
    JIRA_PROJECT_ID=data.PROJECT_ID,
    JIRA_COMPONENT=data.COMPONENT,
)
def test_jira_create_issue_data(JiraMock):
    jira = Jira(config())
    issue = Issue(data.raw_issue())
    issue_data = jira._create_issue_data(issue)
    assert issue_data == {
        "project": {"id": data.PROJECT_ID},
        "summary": f"[GITHUB:{data.REPO}-{data.ISSUE_ID}] {data.TITLE}",
        "description": f"https://github.com/owner/{data.REPO}/issues/{data.ISSUE_ID}",
        "issuetype": {"name": "Task"},
        "components": [{"name": data.COMPONENT}],
    }
