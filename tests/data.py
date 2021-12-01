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

import github2jira.githublib as githublib

PROJECT_ID = "100"
REPO = "repo"
ISSUE_ID = "10"
TITLE = "title"
COMPONENT = "dummy"


def raw_issue():
    ts_epoch = int(time.time()) - githublib.SECONDS_PER_WEEK * 0.5
    return {
        "html_url": f"https://github.com/owner/{REPO}/issues/{ISSUE_ID}",
        "number": ISSUE_ID,
        "labels": [{"name": "sig/network"}, {"name": "sig/compute"}],
        "title": TITLE,
        "url": f"https://api.github.com/repos/owner/{REPO}/issues/{ISSUE_ID}",
        "created_at": datetime.fromtimestamp(ts_epoch).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
