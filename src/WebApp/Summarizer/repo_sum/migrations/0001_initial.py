# Generated by Django 3.2 on 2021-04-21 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Repo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RepoName', models.CharField(max_length=255, unique=True)),
                ('commits', models.TextField()),
                ('pullRequests', models.TextField()),
                ('issues_beginner', models.IntegerField()),
                ('issues_intermediate', models.IntegerField()),
                ('issues_expert', models.IntegerField()),
                ('issues_per_beginner', models.FloatField()),
                ('issues_per_intermediate', models.FloatField()),
                ('issues_per_expert', models.FloatField()),
            ],
        ),
    ]
