import sys, os, time, requests, github
from github import Github
from github import Label


# https://pygithub.readthedocs.io/en/latest/examples/Issue.html#create-issue-with-labels


def reset_repo(repo_name, debug=False):
    repo = git.get_repo("liuyal/" + repo_name)
    if "test_repo" in repo_name.lower() and debug:
        repo.delete()
        git.get_user().create_repo(repo_name)


def copy_repo(repo, reference_repo):
    for item in repo.get_labels(): item.delete()
    for item in repo.get_milestones(): item.delete()
    for item in reference_repo.get_labels(): repo.create_label(item.name, item.color, description=item.raw_data["description"])
    for item in reference_repo.get_milestones(): repo.create_milestone(title=item.title, state=item.state, description=item.description)


def save_labels(labels):
    file = open("labels.csv", 'a+')
    file.truncate(0)
    file.write("name,color,description\n")
    for item in labels: file.write(item.name + "," + item.color + "," + item.description + "\n")
    file.close()


def load_labels(file_name):
    labels = []
    file = open(file_name, 'r+')
    labels_text = file.read().split("\n")[1:-1]
    file.close()

    for line in labels_text:
        name = line.split(",")[0]
        color = line.split(",")[1]
        description = line.split(",")[2]
        label = Label
        label.name = name
        label.color = color
        label.description = description
        labels.append(label)

    return labels


def create_issues(repo, labels, milestones, issues):
    for issue in issues:
        title = issue.split(",")[0]
        description = issue.split(",")[1]
        assignee = issue.split(",")[2]
        label_list = issue.split(",")[3].split(":")
        milestone = issue.split(",")[4]
        issue_labels = []

        for item in label_list:
            for label_item in labels:
                if item.lower() == label_item.name.lower(): issue_labels.append(label_item)

        for item in milestones:
            if item.title.lower() == milestone.lower():
                milestone = item
                break

        print(title + "|" + description + "|" + assignee + "|" + milestone.title)
        print(issue_labels)

        repo.create_issue(title=title, body=description, labels=issue_labels, assignee=assignee, milestone=milestone)


if __name__ == "__main__":
    file = open(os.getcwd() + os.sep + "issues.csv", "r")
    issues = file.read().split("\n")[1:-1]
    file.close()

    file =  open("E:\Files\Stuff\MISC\git.token", "r")
    token = file.read()
    file.close()

    git = Github(token)
    repo_name = "TEST_REPO"
    try:
        repo = git.get_repo("liuyal/" + repo_name)
    except:
        repo = git.get_user().create_repo(repo_name)

    # reset_repo(repo_name)

    labels = repo.get_labels()
    milestones = repo.get_milestones()

    copy_repo(repo, git.get_repo("liuyal/" + "Tiny_GPS_Logger"))

    create_issues(repo, labels, milestones, issues)
