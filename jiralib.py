#!/usr/bin/env python3

def issue_exists(repo, id):
    query = f"[Git:{repo}-{id}]"
    return False

def create_issue(repo, id, title):
    # TODO know to return link to new issue
    return True

def main():
    print("hello jira")

if __name__ == '__main__':
    main()