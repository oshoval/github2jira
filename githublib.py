#!/usr/bin/env python3

import os
import sys
import requests
import json

class Github:
    def __init__(self, owner, repo):
        self.owner = owner
        self.repo = repo
        
        token = os.getenv('GITHUB_TOKEN')
        if token == None:
            print("Error: cant find GITHUB_TOKEN")
            sys.exit(1)

        self.query_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        self.headers = {'Authorization': f'token {token}'}
        
    def get_issues(self, page):
        params = {
            "state": "open", "page" : page, "per_page": "100"
        }

        r = requests.get(self.query_url, headers=self.headers, params=params)
        data = r.json()
        return data

def main():
    print("githublib")
    github = Github("kubevirt", "kubevirt")
    data = github.get_issues(1)
    print(json.dumps(data[0], sort_keys=True, indent=4))

if __name__ == '__main__':
    main()