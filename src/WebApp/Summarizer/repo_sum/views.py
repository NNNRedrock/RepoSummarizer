
from django.shortcuts import render
# import Summarizer_Release_01
# from base_summarizer import BaseSummarizer
# from Summarizer_Release_01.lsa_summarizer import LsaSummarizer
# from Summarizer_Release_01.summarization import run_summarization
# from Summarizer_Release_01.Tool import run_tool

from repo_sum import Tool

# Create your views here.


def summarizer_output(request):
    repo_name = request.POST['reponame']
    output = [1]
    print(repo_name)
    if repo_name:
        output = Tool.run_tool(
            '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', repo_name)
        return render(request, 'index.html', {'Pull_Requests': output[0], 'Commits': output[1], 'Issues_normal': output[2][0], 'Issues_percent': output[2][1]})
    # return render(request, 'index.html', {'summarize':output[0]})


def home(request):
    return render(request, 'index.html')
