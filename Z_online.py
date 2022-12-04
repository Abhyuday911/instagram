import requests
import json
import random
import sys
from pprint import pprint
usernames = [sys.argv[1]]
# usernames = ['abhyuday911']
proxy = "http://username:password@proxy:port"

userSrc = []

# output = {}


def get_headers(username):
    headers = {
        "authority": "www.instagram.com",
        "method": "GET",
        "path": "/{0}/".format(username),
        "scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "upgrade-insecure-requests": "1",
        "Connection": "close",
        "user-agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"
        ])
    }
    return headers


def parse_data(username, user_data):

    if len(user_data['edge_owner_to_timeline_media']['edges']) > 0:
        for node in user_data['edge_owner_to_timeline_media']['edges']:
            if node['node']['thumbnail_src']:
                userSrc.append(
                    node['node']['thumbnail_src']
                )

    output = {
        "imgarr": userSrc,
        "posts": user_data["edge_owner_to_timeline_media"]["count"],
        "followers": user_data["edge_followed_by"]["count"],
        "following": user_data["edge_follow"]["count"],
        "fullname": user_data["full_name"],
        "username": user_data["username"],
        "data": user_data["biography"],
        "profilepic": user_data["profile_pic_url"]
    }
    print(json.dumps(output))


def main():
    for username in usernames:
        url = f"https://instagram.com/{username}/?__a=1&__d=dis"
        response = requests.get(url, headers=get_headers(username))
        # , proxies = {'http': proxy, 'https': proxy}
        if response.status_code == 200:
            try:
                resp_json = json.loads(response.text)
            except:
                print("Failed. Response not JSON")
                continue
            else:
                # print("HERE____________________________________________________")
                user_data = resp_json['graphql']['user']
                parse_data(username, user_data)
        elif response.status_code == 301 or response.status_code == 302:
            print("Failed. Redirected to login")
        else:
            print("Request failed. Status: " + str(response.status_code))


if __name__ == '__main__':
    main()
    # pprint(userSrc)
