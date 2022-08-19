import os
from datetime import datetime, timedelta
from tabnanny import check
from github import Github

gh_url = "https://github.com"
token = os.environ["INPUT_REPO_TOKEN"]
gh = Github(token)
common_label=os.environ["COMMON_ISSUE_LABEL"]
from_repo_name = os.environ["GITHUB_REPOSITORY"]
to_repo_name=os.environ["TO_REPO"]


def check_issue_contain_label(issue_num,common_label):
    from_repo = gh.get_repo(from_repo_name)
    issue=from_repo.get_issue(issue_num)
    print(issue)
    for i in issue.labels:
        print(i)
        if i.name == common_label:
            return True
    return False

def send_issue_to_repo(issue_num,to_repo_name):
    from_repo = gh.get_repo(from_repo_name)
    issue=from_repo.get_issue(issue_num)
    print('issue is ',issue)
    to_repo = gh.get_repo(to_repo_name)
    print('to repo',to_repo)
    print('nnn',issue.title,issue.body,issue.labels)
    to_repo.create_issue(title=issue.title,body=issue.body,labels=issue.labels)


def main(issue_num,common_label):
    if check_issue_contain_label(issue_num,common_label):
        send_issue_to_repo(issue_num,to_repo_name)

if __name__ == "__main__":
    issue_num="33"
    if issue_num != "":
        issue_num = int(issue_num)
    main(issue_num,common_label)
    
