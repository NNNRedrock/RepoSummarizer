import pandas as pd
import github
from github import Github
# Creating an Instance of Github api using github access tokens
g = Github('e25440702e702765b44c3697a9fedd33cae92c3c')

try:
    test_repo = 'Netflix/iep'
    # Fetching repo data
    repo = g.get_repo(test_repo)
    print(repo.name)
    # Fetching commits data
    commits = repo.get_commits()
    # Fetching OpenIssues data
    openIssues = repo.get_issues(state='open')
    closedIssues = repo.get_issues(state='closed')
    prs = repo.get_pulls(state='closed')

    commitcnt = commits.totalCount
    openIssuescnt = openIssues.totalCount
    closedIssuescnt = closedIssues.totalCount
    prscnt = prs.totalCount

    if commits[0].commit.message:
        print(commits[0].commit.message)
    else:
        print("Nan")

    if prs[0].body:
        print(prs[0].body, prscnt)
    else:
        print("Nan")

except github.GithubException:
    pass
