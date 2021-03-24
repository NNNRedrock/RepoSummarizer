import pandas as pd
import github
from github import Github
from summarization import run_summarization


def run_tool(access_token, repo_name):

    g = Github(access_token)

    try:
        repo = g.get_repo(repo_name)
    except github.GithubException:
        print("Invalid Repo Name")
        return

    print("Fetching Commits, Prs and Issues")
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
            closedIssuesFiltered.append(closedIssues[j].closed_by)
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

    print("Started the Summarization Process")

    run_summarization(df, 'Commits')
    run_summarization(df, 'Pull Requests')

    print("Successfully completed Summarization")

print("\nWelcome to Github Repo Summarizer")

# access_token = input("Generate and Enter Github access token\n")

repo_name = input("Enter the Name of Repo To Summarize\n")

run_tool('e0b63cbec1fbb382c3bf4c03e0a9f3e851640ac5', repo_name)
