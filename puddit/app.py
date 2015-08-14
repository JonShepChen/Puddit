import requests
import json
import time
from bs4 import BeautifulSoup

#Which subreddits would you like to monitor? (subreddits max)

already_pushed = []
loop_count = 0
pb_request_url = 'https://api.pushbullet.com/v2/pushes'
authorization = 'Bearer v1s0QnhullE8cI6AB6fEwUpBIrEr2vPEGeujw1WWxXJy8'
content_type = 'application/json'
pb_request_headers = {'Authorization': authorization, 'Content-Type': content_type}
pb_request_body = {"type":"link"}

target_subreddit = input("Subreddit you would like to monitor: ")
reddit_request_url = 'http://www.reddit.com/r/{0}/new.json?count=25&sort=new'.format(target_subreddit)

print("Monitoring Subreddit - " + target_subreddit)

while(True):
    reddit_response = requests.get(reddit_request_url, headers={'User-Agent': "PudditAgent"})
    reddit_response_json = json.loads(reddit_response.text)
    push_list = []

    for post in reddit_response_json['data']['children']:
        post_data = post['data']
        post_id = post_data['name']
        post_elasped_time = int(time.time()) - int(post_data['created_utc'])

        if post_elasped_time < 180 and post_id not in already_pushed:
            post_title = post_data['title']
            post_url = post_data['url']
            push_list.append((post_id, post_title, post_url))
            already_pushed.append(post_id)

    for post in push_list:
        pb_request_body['title'] = post[1]
        pb_request_body['url'] = post[2]
        requests.post(pb_request_url, headers=pb_request_headers, data=json.dumps(pb_request_body))
        print("New Post! - " + post[1])

    loop_count += 1
    time.sleep(5)

    if loop_count > 200:
        already_pushed = []
        loop_count = 0

