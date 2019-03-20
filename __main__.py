import requests
from lxml import html
from settings import *
import json
import telegram
from time import sleep


def get_json(url):
    r = requests.get(url, headers=HEADERS)
    tree = html.fromstring(r.content)
    # We extract the JSON from html page and get the correct script
    script = tree.xpath("//script[@type='text/javascript']//text()")[3]
    script = script.replace("window._sharedData = ", "", 1)
    script = script[:len(script)-1]
    return json.loads(script)


def get_posts(url):
    j = get_json(url)
    posts = j["entry_data"]["ProfilePage"][0]\
        ["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]

    for post in posts:
        post = post["node"]

        yield {
            "shortcode": post["shortcode"],
            "image": post["display_url"],
            "text": post["edge_media_to_caption"]["edges"][0]["node"]["text"]
        }


def check_alredy_seen(shortcode):
    with open("already_seen.txt", "r") as f:
        for line in f.readlines():
            if shortcode in line:
                return True

        return False


def add_already_seen(shortcode):
    with open("already_seen.txt", "a") as f:
        f.write(shortcode + "\n")


if __name__ == '__main__':
    # Initialize BOT
    bot = telegram.Bot(token=BOT_TOKEN)

    # We first need to save all the posts to file
    for post in get_posts(INSTAGRAM_BASE_URL):
        if not check_alredy_seen(post["shortcode"]):
            add_already_seen(post["shortcode"])
            print("Added", post["shortcode"], "to the already_seen list")

    while True:
        for post in get_posts(INSTAGRAM_BASE_URL):
            if not check_alredy_seen(post["shortcode"]):
                bot.send_photo(
                    chat_id=CHAT_ID,
                    photo=post["image"],
                    caption=post["text"]
                )

                add_already_seen(post["shortcode"])
                print("Added", post["shortcode"], "to the already_seen list")

        sleep(SLEEP_TIME)
