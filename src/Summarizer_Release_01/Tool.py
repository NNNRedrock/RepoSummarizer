import pandas as pd
import github
import numpy as np
import requests as r
from bs4 import BeautifulSoup as bs
from github import Github
from summarization import run_summarization

## Write Beautiful soup function here and call it in get_issues_expertise_level function
def contributions(username):
    s = r.get('https://github.com/'+username+'/')
    content_user = bs(s.content,'html.parser')
    containers = content_user.findAll("h2", { "class":"f4 text-normal mb-2"})
    final_res = '0'
    if len(containers):
        res1 = str(containers[0]).split('>')[1].lstrip()
    #res2 = res1[1].lstrip()
        final_res = res1.split()[0]
    return final_res

#Calculating issues ex[ertise level
def get_issues_expertise_level(g, username):
    user = g.get_user(username)
    stars = user.get_starred().totalCount
    followers = user.followers
    contribute = int("".join(contributions(username).split(',')))

    base_expertise = (stars + followers + contribute) / 3
    # Normalizing base_expertise based in observed data (1500 observed as max score)
    base_expertise = base_expertise/max(1500, base_expertise)

    expertise_level = 4/(1+np.exp(-base_expertise)) - 2

    return expertise_level


#Generating issus expertise level
def generate_exp_level(g, closedByUserNames):

    dict = {'Easy': 0, 'Medium': 0, 'Hard': 0}

    for username in closedByUserNames:
        if len(username) < 17:
            continue
        trimmed_username = username[17:-2]
        exp_level = get_issues_expertise_level(g, trimmed_username)

        if exp_level >= 0 and exp_level <= 0.3:
            dict['Easy'] += 1
        elif exp_level > 0.3 and exp_level <= 0.6:
            dict['Medium'] += 1
        elif exp_level > 0.6 and exp_level <= 1:
            dict['Hard'] += 1

    print("Easy : ", dict['Easy'])
    print("Medium : ", dict['Medium'])
    print("Hard : ", dict['Hard'])

    print("Percentages: ")
    percent_easy = 100 * dict['Easy'] / (dict['Easy'] + dict['Medium'] + dict['Hard'])
    percent_medium = 100 * dict['Medium'] / (dict['Easy'] + dict['Medium'] + dict['Hard'])
    percent_hard = 100 * dict['Hard'] / (dict['Easy'] + dict['Medium'] + dict['Hard'])

    print("Easy : ", percent_easy)
    print("Medium : ", percent_medium)
    print("Hard : ", percent_hard)

def run_tool(access_token, repo_name):

    g = Github(access_token)

    try:
        repo = g.get_repo(repo_name)
    except github.GithubException:
        print("Invalid Repo Name")
        return

    print("\nFetching Commits, Prs and Issues")
    commits = repo.get_commits()
    openIssues = repo.get_issues(state = 'open')
    closedIssues = repo.get_issues(state='closed')
    prs = repo.get_pulls(state = 'closed')

    repoNameFiltered = []
    commitsFiltered = []
    openIssuesFiltered = []
    closedIssuesFiltered = []
    prsFiltered = []

    # Fetching count of commits, open issues, closed issues, prs
    commitcnt = commits.totalCount
    openIssuescnt = openIssues.totalCount
    closedIssuescnt = closedIssues.totalCount
    prscnt = prs.totalCount

    # Limit of extraction is 300 commits, 300 issues, 300 prs for a repo
    for j in range(0,300):

        repoNameFiltered.append(repo.name)

        # Filtering empty commit messages
        if j < commitcnt and commits[j].commit.message:
            commitsFiltered.append(commits[j].commit.message)
        else:
            commitsFiltered.append("Nan")

        # Filtering empty issue body
        if j < openIssuescnt and openIssues[j].body:
            openIssuesFiltered.append(openIssues[j].body)
        else:
            openIssuesFiltered.append("Nan")

        if j < closedIssuescnt:
            closedIssuesFiltered.append(str(closedIssues[j].closed_by))
        else:
            closedIssuesFiltered.append("Nan")

        # Filtering empty prs body
        if j < prscnt and prs[j].body:
            prsFiltered.append(prs[j].body)
        else:
            prsFiltered.append("Nan")

    print("Fetched Data Successfully")

    d = {'Repo Name': repoNameFiltered, 'Commits': commitsFiltered, 'Open Issues': openIssuesFiltered, 'Closed Issues': closedIssuesFiltered, 'Pull Requests': prsFiltered}
    df = pd.DataFrame(data= d)

    print("\nStarted the Summarization Process")

    run_summarization(df, 'Commits')
    run_summarization(df, 'Pull Requests')

    generate_exp_level(g, closedIssuesFiltered)
    print("Successfully completed Summarization")


if __name__ == "__main__":

    print("\n+-----------------------------------+")
    print("| Welcome to Github Repo Summarizer |")
    print("+-----------------------------------+\n")

    # access_token = input("Generate and Enter Github access token\n")

    repo_name = input("Enter the Name of Repo To Summarize\n")

    run_tool('e0b63cbec1fbb382c3bf4c03e0a9f3e851640ac5', repo_name)
