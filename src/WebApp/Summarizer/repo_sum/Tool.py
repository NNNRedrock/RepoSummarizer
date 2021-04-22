import pandas as pd
import github
import numpy as np
import requests as r
from bs4 import BeautifulSoup as bs
from github import Github
from repo_sum.summarization import run_summarization

# Function for scraping github website to get contributions of the user
def contributions(username):
    s = r.get('https://github.com/'+username+'/')
    content_user = bs(s.content,'html.parser')
    containers = content_user.findAll("h2", { "class":"f4 text-normal mb-2"})
    final_res = '0'
    if len(containers):
        res1 = str(containers[0]).split('>')[1].lstrip()
        final_res = res1.split()[0]
    return final_res

# Calculating issues expertise level
def get_issues_expertise_level(g, username):

    # Obtaining profile data using github api
    user = g.get_user(username)
    stars = user.get_starred().totalCount
    followers = user.followers

    contribute = int("".join(contributions(username).split(',')))

    base_expertise = (stars + followers + contribute) / 3

    # Normalizing base_expertise based on observed data (1500 observed as max score)
    base_expertise = base_expertise/max(1500, base_expertise)

    # Running Sigmoid function for getting the expertise level in range 0 to 1
    expertise_level = 4/(1+np.exp(-base_expertise)) - 2

    return expertise_level


# Outputting issues expertise level for given github username
def generate_exp_level(g, closedByUserNames):

    dict = {'Easy': 0, 'Medium': 0, 'Hard': 0}

    for username in closedByUserNames:
        if len(username) < 17:
            continue
        trimmed_username = username[17:-2]
        exp_level = get_issues_expertise_level(g, trimmed_username)

        # Classifying issues based on exp_level
        if exp_level >= 0 and exp_level <= 0.3:
            dict['Easy'] += 1
        elif exp_level > 0.3 and exp_level <= 0.6:
            dict['Medium'] += 1
        elif exp_level > 0.6 and exp_level <= 1:
            dict['Hard'] += 1

    # Calculating percentages
    percent_easy = 100 * dict['Easy'] / (dict['Easy'] + dict['Medium'] + dict['Hard'])
    percent_medium = 100 * dict['Medium'] / (dict['Easy'] + dict['Medium'] + dict['Hard'])
    percent_hard = 100 * dict['Hard'] / (dict['Easy'] + dict['Medium'] + dict['Hard'])
    return (dict['Easy'], dict['Medium'], dict['Hard']), (percent_easy, percent_medium,percent_hard)

# This is the main Function for running the tool
# which returns summarization of commits and pull requests and Issues expertise level
def run_tool(access_token, repo_name):

    # Using PyGithub api
    g = Github(access_token)

    # Checking whether Github repo is valid or not
    try:
        repo = g.get_repo(repo_name)
    except github.GithubException:
        print("Invalid Repo Name")
        return

    print("\nFetching Commits, Prs and Issues")

    commits = repo.get_commits()
    closedIssues = repo.get_issues(state='closed')
    prs = repo.get_pulls(state = 'closed')

    repoNameFiltered = []
    commitsFiltered = []
    closedIssuesFiltered = []
    prsFiltered = []

    # Fetching count of commits, closed issues, prs
    commitcnt = commits.totalCount
    closedIssuescnt = closedIssues.totalCount
    prscnt = prs.totalCount

    # Limit of extraction is 300 commits, 300 issues, 300 prs for a repo
    for j in range(0, 300):

        repoNameFiltered.append(repo.name)

        # Filtering empty commit messages
        if j < commitcnt and commits[j].commit.message:
            commitsFiltered.append(commits[j].commit.message)
        else:
            commitsFiltered.append("Nan")

        if j < closedIssuescnt:
            closedIssuesFiltered.append(str(closedIssues[j].closed_by))
        else:
            closedIssuesFiltered.append("Nan")

        # Filtering empty prs body
        if j < prscnt and prs[j].body:
            prsFiltered.append(prs[j].body)
        else:
            prsFiltered.append("Nan")

    d = {'Repo Name': repoNameFiltered, 'Commits': commitsFiltered, 'Closed Issues': closedIssuesFiltered, 'Pull Requests': prsFiltered}
    df = pd.DataFrame(data=d)

    # Calling run_summarization function in summarization.py
    return run_summarization(df, 'Commits'), run_summarization(df, 'Pull Requests'), generate_exp_level(g, closedIssuesFiltered)

