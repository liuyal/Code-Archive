import sys, os, time, requests
from github import Github

# https://pygithub.readthedocs.io/en/latest/examples/Issue.html#create-issue-with-labels
debug = False

file = open(os.getcwd() + os.sep + "git.token", "r")
token = file.read()
file.close()

file = open(os.getcwd() + os.sep + "issues.csv", "r")
issues = file.read().split("\n")
issues.pop(0)
file.close()

git = Github(token)

repo_name = "Tiny_GPS_Logger"

try:
    repo = git.get_repo("liuyal/" + repo_name)
    if "test_repo" in repo_name.lower() and debug == True:
		repo.delete()
		user = git.get_user()
		repo = user.create_repo(repo_name)
except:
    user = git.get_user()
    repo = user.create_repo(repo_name)

# labels = repo.get_labels()
# for item in labels:
#     item.delete()
#
gps_repo = git.get_repo("liuyal/" + repo_name)
gps_labels = gps_repo.get_labels()
#
# for item in gps_labels:
#     repo.create_label(item.name, item.color, description=item.raw_data["description"])

for item in issues:
    title = item.split(",")[0]
    description = item.split(",")[1]
    assignee = item.split(",")[2]
    label_list =item.split(",")[3].split(":")
    repo_lab = []
    for label in label_list:
        for label_item in gps_labels:
            if label.lower() == label_item.name.lower():
                repo_lab.append(label_item)

    print(title + "|" + description + "|" + assignee + "|" + item.split(",")[4])

    try:
        milestones = repo.create_milestone(item.split(",")[4])
    except:
        if "GNSS" in item.split(",")[4]:
            n = 1
        elif "Doc" in item.split(",")[4]:
            n = 4
        elif "Web" in item.split(",")[4]:
            n = 3
        elif "Android" in item.split(",")[4]:
            n = 2
        milestones = repo.get_milestone(number=n)
    repo.create_issue(title=title, body=description, labels=repo_lab, assignee=assignee, milestone=milestones)
