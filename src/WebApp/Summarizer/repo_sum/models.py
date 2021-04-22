from django.db import models

# Create your models here.

class Repo(models.Model):
    RepoName = models.CharField(unique=True, max_length=255)
    commits = models.TextField()
    pullRequests = models.TextField()
    issues_beginner = models.IntegerField()
    issues_intermediate = models.IntegerField()
    issues_expert = models.IntegerField()
    issues_per_beginner = models.FloatField()
    issues_per_intermediate = models.FloatField()
    issues_per_expert = models.FloatField()

    def __str__(self):
        return self.RepoName
