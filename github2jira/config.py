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


class Config:
    def __init__(self, var_names):
        self._vars = {name: None for name in var_names}

    @property
    def vars(self):
        return self._vars

    def Load(self):
        for var_name in self._vars.keys():
            value = os.getenv(var_name)
            if value is None:
                raise NameError(f"can't find {var_name}")
            self._vars[var_name] = value
