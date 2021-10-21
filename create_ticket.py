#!/usr/bin/env python3

import requests
import os
import json
import configparser
import sys

import jiralib

# cfg file name
cfg_file = 'status.cfg'
# process upto this id in case no status.cfg exists
last = '6300'
# how many tickets can be opened on each cycle
flood_protection_limit = 3

jira_token = ""

def init_db(config):
    global last
    try:
        last = config.get('DEFAULT', 'last')
    except configparser.NoOptionError:
        print("db doesn't exists, adding initial value")
        config['DEFAULT']['last'] = last
        with open(cfg_file, 'w') as configfile:
            config.write(configfile)

    return last

def update_db(config, last):
    config['DEFAULT']['last'] = last
    with open(cfg_file, 'w') as configfile:
        config.write(configfile)

def process_issues(owner, repo, query_url, headers):
    issues_created = 0

    for n in range(1, 20):
        params = {
            "state": "open", "page" : n, "per_page": "100"
        }

        r = requests.get(query_url, headers=headers, params=params)
        data = r.json()

        if len(data) == 0:
            break

        #print(json.dumps(data, sort_keys=True, indent=4))
        for element in data:
            html_url = element["html_url"]
            id = element["number"]
            title = element["title"]

            if "pull" in html_url:
                continue

            if id <= int(last):
                return

            is_network = False
            for label in element["labels"]:
                if label["name"] == "sig/network":
                    is_network = True
                    break
            
            if is_network:
                #print(id, element["html_url"], title)
                if jiralib.issue_exists(repo, id) == False:
                    print("creating issue for", element["html_url"], title)
                    res = jiralib.create_issue(repo, id, title)
                    if res == True:
                        print(f"issue {id} created")
                        issues_created += 1
                        if issues_created == flood_protection_limit:
                            print("flood protection limit reached, exiting")
                            sys.exit(0)


def create_issue(jira):
    issue_dict=dict()
    issue_dict['project']=dict({'id':'10001'})
    issue_dict['summary']="[GITHUB:PG-123] Foo"
    issue_dict['description']="Bla"
    issue_dict['issuetype']=dict({'name':'Task'})

    issue = jira.create_issue(issue_dict)
    print(issue)

# works
def test():
    # import the installed Jira library
    from jira import JIRA
    
    # Specify a server key. It is your  domain 
    # name link.
    jiraOptions = {'server': "https://nmstate.atlassian.net"}
    
    # Get a JIRA client instance, Pass 
    # Authentication parameters
    # and  Server name.
    # emailID = your emailID
    # token = token you receive after registration
    jira = JIRA(options = jiraOptions, 
                basic_auth = ("oshoval@redhat.com", jira_token))
    
    # While fetching details of a single issue,
    # pass its UniqueID or Key.
    singleIssue = jira.issue('PLAYG-1')
    print('{}: {}:{}'.format(singleIssue.key,
                            singleIssue.fields.summary,
                            singleIssue.fields.reporter.displayName))

    create_issue(jira)
 


def main():
    config = configparser.ConfigParser()
    config.read(cfg_file)
    last = init_db(config)

    token = os.getenv('GITHUB_TOKEN')

    if token == None:
        print("Error: cant find GITHUB_TOKEN")
        sys.exit(1)

    owner = "kubevirt"
    repo = "kubevirt"
    query_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {'Authorization': f'token {token}'}

    process_issues(owner, repo, query_url, headers)



def iterateDictIssues(oIssues, listInner):

	# Now,the details for each Issue, maybe
	# directly accessible, or present further,
	# in nested dictionary objects.
	for key, values in oIssues.items():
		# If key is 'fields', get its value,
		# to fetch the 'summary' of issue.
		if(key == "fields"):

			# Since type of object is Json str,
			# convert to dictionary object.
			fieldsDict = dict(values)

			# The 'summary' field, we want, is
			# present in, further,nested dictionary
			# object. Hence,recursive call to
			# function 'iterateDictIssues'.
			iterateDictIssues(fieldsDict, listInner)

		# If key is 'reporter',get its value,
		# to fetch the 'reporter name' of issue.
		elif (key == "reporter"):

			# Since type of object is Json str
			# convert to dictionary object.
			reporterDict = dict(values)

			# The 'displayName', we want,is present
			# in,further, nested dictionary object.
			# Hence,recursive call to function 'iterateDictIssues'.
			iterateDictIssues(reporterDict, listInner)

		# Issue keyID 'key' is directly accessible.
		# Get the value of key "key" and append
		# to temporary list object.
		elif(key == 'key'):
			#print(values)
			keyIssue = values
			listInner.append(keyIssue)

		# Get the value of key "summary",and,
		# append to temporary list object, once matched.
		elif(key == 'summary'):
			#print(values)            
			keySummary = values
			listInner.append(keySummary)

		# Get the value of key "displayName",and,
		# append to temporary list object,once matched.
		elif(key == "displayName"):
			keyReporter = values
			listInner.append(keyReporter)


# works
def test3():
    # Import the required libraries
    import requests
    from requests.auth import HTTPBasicAuth
    import json
    import pandas as pd

    # URL to Search all issues.
    url = "https://nmstate.atlassian.net/rest/api/2/search"

    # Create an authentication object,using
    # registered emailID, and, token received.
    auth = HTTPBasicAuth("oshoval@redhat.com", jira_token)

    # The Header parameter, should mention, the
    # desired format of data.
    headers = {
        "Accept": "application/json"
    }
    # Mention the JQL query.
    # Here, all issues, of a project, are
    # fetched,as,no criteria is mentioned.
    query = {
        'jql': 'project =Playground'
    }

    # Create a request object with above parameters.
    response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=auth,
        params=query
    )

    # Get all project issues,by using the
    # json loads method.
    projectIssues = json.dumps(json.loads(response.text),
                            sort_keys=True,
                            indent=4,
                            separators=(",", ": "))

    # The JSON response received, using
    # the requests object,
    # is an intricate nested object.
    # Convert the output to a dictionary object.
    dictProjectIssues = json.loads(projectIssues)

    # We will append,all issues,in a list object.
    listAllIssues = []

    # The Issue details, we are interested in,
    # are "Key" , "Summary" and "Reporter Name"
    keyIssue, keySummary, keyReporter = "", "", ""

    # Iterate through the API output and look
    # for key 'issues'.
    for key, value in dictProjectIssues.items():

        # Issues fetched, are present as list elements,
        # against the key "issues".
        if(key == "issues"):

            # Get the total number of issues present
            # for our project.
            totalIssues = len(value)

            # Iterate through each issue,and,
            # extract needed details-Key, Summary,
            # Reporter Name.
            for eachIssue in range(totalIssues):
                listInner = []

                # Issues related data,is nested
                # dictionary object.
                iterateDictIssues(value[eachIssue], listInner)

                # We append, the temporary list fields,
                # to a final list.
                listAllIssues.append(listInner)

    # Prepare a dataframe object,with the final
    # list of values fetched.
    dfIssues = pd.DataFrame(listAllIssues, columns=["Reporter",
                                                    "Summary",
                                                    "Key"])

    # Reframing the columns to get proper
    # sequence in output.
    columnTiles = ["Key", "Summary", "Reporter"]
    dfIssues = dfIssues.reindex(columns=columnTiles)
    print(dfIssues)
    #print(listAllIssues)


if __name__ == '__main__':
    jira_token = os.getenv('JIRA_TOKEN')

    if jira_token == None:
        print("Error: cant find JIRA_TOKEN")
        sys.exit(1)

    #test()
    test3()
    #main()






