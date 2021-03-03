import pandas as pd
import github
from github import Github

# Creating Instance of Pygithub api
g = Github('794cdba5b660650157f1ac7f15727a4e46f66361')

repoNames = []

# Reading the csv file which has names of the repos we want to extract info from
df = pd.read_csv('repo_names.csv')

cnt = 0

df1 = pd.DataFrame({'Repo Name': [], 'Commits': [], 'Open Issues': [], 'Closed Issues': [], 'Pull Requests': []})

# Looping over all the repo names
for repoName in df['repo_names']:

    try:
        repo = g.get_repo(repoName)
    except github.GithubException:
        continue

    # Fetching commits, open issues, closed issues, pull requests of a repo
    commits = repo.get_commits()
    openIssues = repo.get_issues(state = 'open')
    closedIssues = repo.get_issues(state='closed')
    prs = repo.get_pulls(state = 'closed')

    # Filtering repos that don't have commits or issues or pull requests
    if (commits.totalCount == 0 or openIssues.totalCount == 0 or closedIssues.totalCount == 0 or prs.totalCount == 0):
        continue

    cnt  = cnt + 1

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

    d = {'Repo Name': repoNameFiltered, 'Commits': commitsFiltered, 'Open Issues': openIssuesFiltered, 'Closed Issues': closedIssuesFiltered, 'Pull Requests': prsFiltered}
    df2 = pd.DataFrame(data= d)
    df1 = df1.append(df2, ignore_index = True)

    if cnt == 50:
        break;

# Exporting extracted data to csv file
df1.to_csv('Dataset1-50.csv')