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

import github2jira.githublib as githublib


def mockenv(**envvars):
    return mock.patch.dict(os.environ, envvars)


class GithubEnvMock:
    TOKEN = "dummy"
    OWNER = "owner"
    REPO = "repo"
    LABEL = "sig/network"


@mockenv(
    GITHUB_TOKEN=GithubEnvMock.TOKEN,
    GITHUB_OWNER=GithubEnvMock.OWNER,
    GITHUB_REPO=GithubEnvMock.REPO,
    GITHUB_LABEL=GithubEnvMock.LABEL,
)
def test_config_load():
    cfg = githublib.config()
    print(cfg)
    assert cfg.vars == {
        githublib.GithubEnv.TOKEN: GithubEnvMock.TOKEN,
        githublib.GithubEnv.OWNER: GithubEnvMock.OWNER,
        githublib.GithubEnv.REPO: GithubEnvMock.REPO,
        githublib.GithubEnv.LABEL: GithubEnvMock.LABEL,
    }


def test_config_load_fail_missing_var():
    with pytest.raises(NameError):
        githublib.config()
