import requests
import os
import sys


def get_release(repo, r_tag):
    data = requests.get(f'https://api.github.com/repos/{repo}/releases/latest').json()
    if data['tag_name'] != r_tag:
        assets = requests.get(data['assets_url']).json()
        return assets[0]['browser_download_url']
    else:
        return False


def last_release_tag(repo):
    data = requests.get(f'https://api.github.com/repos/{repo}/releases/latest').json()
    return data['tag_name']


def have2update(r_tag):
    exename = sys.argv[0]
    return not exename.endswith('py') and r_tag != last_release_tag(r_tag)


def download_release(repo, r_tag):
    exename = sys.argv[0]
    if exename.endswith('py'):
        return False
    else:
        input(exename)
    try:
        url = get_release(repo, r_tag)
        if url:
            data = requests.get(url)
            f = open(exename, 'wb')
            f.write(data.content)
            f.close()
            return True
    except Exception as e:
        print(e)
        return False


def restart():
    os.execl(sys.executable, sys.executable, *sys.argv)