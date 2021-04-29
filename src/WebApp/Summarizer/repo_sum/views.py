from django.shortcuts import render
from repo_sum import Tool
from .models import Repo

# Create your views here.

def get_access_token(str):
    token = ''
    i = 0
    while(i < len(str)):
        token = token+str[i]+str[i+1]
        i = i+3
    return token

# Function for handling the request to summarize github repo
def summarizer_output(request):
    repo_name = request.POST['reponame']
    print(repo_name)
    if repo_name:
        try:
            data = Repo.objects.get(RepoName=repo_name)
            return render(request, 'index.html',
                          {'Pull_Requests': data.pullRequests, 'Commits': data.commits,
                           'Issues_normal': (data.issues_beginner, data.issues_intermediate, data.issues_expert),
                           'Issues_percent': (data.issues_per_beginner, data.issues_per_intermediate, data.issues_per_expert)})
        except:
            output = Tool.run_tool(
                get_access_token('gh1p_1iW1XD17Q1sN17Z1NH14U1bP15c1mq1co18t18Q1T81Br11W1Ds13E1'), repo_name)

            x = float('{:.2f}'.format(float(output[2][1][0])))
            y = float('{:.2f}'.format(float(output[2][1][1])))
            z = float('{:.2f}'.format(float(output[2][1][2])))

            # Saving obtained result in database
            new_entry = Repo(RepoName=repo_name, commits= output[1], pullRequests= output[0],
                             issues_beginner= output[2][0][0], issues_intermediate= output[2][0][1], issues_expert= output[2][0][2],
                             issues_per_beginner= x, issues_per_intermediate= y, issues_per_expert= z)
            new_entry.save()

            return render(request, 'index.html',
                          {'Pull_Requests': output[0], 'Commits': output[1],
                           'Issues_normal': output[2][0], 'Issues_percent': (x, y, z)})


def home(request):
    return render(request, 'index.html')
