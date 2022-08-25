import os
from github import Github

gh_url = "https://github.com"
token = os.environ["GH_PAT"]
gh = Github(token)
common_label=os.environ["COMMON_ISSUE_LABEL"]
from_repo_name = os.environ["GITHUB_REPOSITORY"]
to_repo_name=os.environ["TO_REPO"]


def check_issue_contain_label(issue_num,common_label):
    from_repo = gh.get_repo(from_repo_name)
    issue=from_repo.get_issue(issue_num)
    for i in issue.labels:
        if i.name == common_label:
            return True
    return False

def generate_latest_100_issues(repo):
    list_issues = []
    for i, ci in enumerate(repo.get_issues()):
        if i > 100:
            break
        list_issues.append(ci)
    return list_issues

def check_is_existed(issue,list_issues):
    migrate="Migrated from:{}#{}".format(from_repo_name,issue.number)
    for each in list_issues:
        if each.body is None:
            continue
        if migrate in each.body:
            return True,each
    return False,-1


def send_issue_to_repo(issue_num,to_repo_name):
    from_repo = gh.get_repo(from_repo_name)
    issue=from_repo.get_issue(issue_num)
    to_repo = gh.get_repo(to_repo_name)

    list_issues = generate_latest_100_issues(to_repo)
    res = check_is_existed(issue,list_issues)
    if res[0] is not False:
        print('>>>>>>>>>> issue is existed,update it >>>>>>>>>>')
        res[1].set_labels(*issue.labels)
    else:
        print('>>>>>>>>>> build a new issue >>>>>>>>>>')
        new_body=issue.body
        migrate="Migrated from:{}#{}".format(from_repo_name,issue.number)
        new_body += "\n\n{}".format(migrate)
        to_repo.create_issue(title=issue.title,body=new_body,labels=issue.labels)


def main(issue_num,common_label):
    if check_issue_contain_label(issue_num,common_label):
        send_issue_to_repo(issue_num,to_repo_name)

if __name__ == "__main__":
    issue_num = os.environ["IU_NUM"]
    if issue_num != "":
        issue_num = int(issue_num)
    print(">>> issue number: {}".format(issue_num))
    main(issue_num,common_label)
    
