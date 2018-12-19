import requests
import pandas as pd

def issues(repo):
    url = "https://api.github.com/repos/{}/issues".format(repo)
    issues = requests.get(url)
    
    issues_list = []
    for issue in issues.json():
        issues_dict = {'number':issue['number'],
                    'title':issue['title'],
                    'user_name':issue['user']['login']}
        issues_list.append(issues_dict)
    
    issues_df = pd.DataFrame(issues_list)

    return issues_df

issues("numpy/numpy")


