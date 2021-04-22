from django.shortcuts import render
from repo_sum import Tool
from .models import Repo

# Create your views here.

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
                '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', repo_name)
            x = float('{:.2f}'.format(float(output[2][1][0])))
            y = float('{:.2f}'.format(float(output[2][1][1])))
            z = float('{:.2f}'.format(float(output[2][1][2])))
            return render(request, 'index.html',
                          {'Pull_Requests': output[0], 'Commits': output[1],
                           'Issues_normal': output[2][0], 'Issues_percent': (x, y, z)})


def home(request):
    return render(request, 'index.html')
