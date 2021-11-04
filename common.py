#!/usr/bin/env python3

import os
import sys


def get_envvar(name, default_value=None):
    value = os.getenv(name, default_value)
    if value is None:
        print(f"Error: cant find {name}, exiting")
        sys.exit(1)
    return value


def main():
    print("common self test")
    get_envvar("JIRA_TOKEN")


if __name__ == "__main__":
    main()
