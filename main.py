import os
from github import Github

gh_url = "https://github.com"
token = os.environ["GH_PAT"]
gh = Github(token)
common_label = os.environ["COMMON_ISSUE_LABEL"]
from_repo_name = os.environ["GITHUB_REPOSITORY"]
to_repo_name = os.environ["TO_REPO"]


def check_issue_contain_label(issue_num, common_label):
    from_repo = gh.get_repo(from_repo_name)
    issue = from_repo.get_issue(issue_num)
    for i in issue.labels:
        if i.name == common_label:
            return True
    return False


def get_10_issue_comment(issue):
    list_comments = []
    for i, ci in enumerate(issue.get_comments()):
        if i > 10:
            break
        list_comments.append(ci)
    return list_comments


def check_comment(list_comments):
    migrate = "Migrated to:{}".format(to_repo_name)
    if len(list_comments) == 0:
        return True
    for i in list_comments:
        if migrate in i.body:
            return False
    return True


def send_issue_to_repo(issue):

    to_repo = gh.get_repo(to_repo_name)
    new_body = issue.body
    return to_repo.create_issue(title=issue.title, body=new_body, labels=issue.labels)


def find_new_issue_number(son, pre):
    st = pre.find(son)
    if st != -1:
        st += len(son)
    return int(pre[st:])


def update_sync_issue(issue, list_comments):
    migrate = "Migrated to:{}#".format(to_repo_name)
    for i in list_comments:
        if migrate in i.body:
            number = find_new_issue_number(migrate, i.body)
            to_repo = gh.get_repo(to_repo_name)
            to_issue = to_repo.get_issue(number)
            to_issue.set_labels(*issue.labels)
            return True
    return False


def main(issue_num, common_label):
    if check_issue_contain_label(issue_num, common_label):
        from_repo = gh.get_repo(from_repo_name)
        issue = from_repo.get_issue(issue_num)
        list_comments = get_10_issue_comment(issue)
        if check_comment(list_comments):
            print(">>>>>>>>>> build a new issue >>>>>>>>>>")
            new_issue = send_issue_to_repo(issue)
            migrate = "Migrated to:{}#{}".format(to_repo_name, new_issue.number)
            issue.create_comment(migrate)
            print(">>>>>>>>>> build succeed >>>>>>>>>>")
        else:
            print(">>>>>>>>>> update issue labels >>>>>>>>>>")
            if update_sync_issue(issue, list_comments):
                print(">>>>>>>>>> update succeed >>>>>>>>>>")
            else:
                print(">>>>>>>>>> update failed >>>>>>>>>>")


if __name__ == "__main__":
    issue_num = os.environ["IU_NUM"]
    if issue_num != "":
        issue_num = int(issue_num)
    print(">>> issue number: {}".format(issue_num))
    main(issue_num, common_label)
