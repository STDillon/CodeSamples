from http.client import BadStatusLine
from urllib.error import URLError
import twitter
import json
import sys
import time
def oauth_login():
    CONSUMER_KEY = 'bTiIJlQihrOTcb6jDiA7C0Dtk '
    CONSUMER_SECRET = 'RGeqpLAnlnhGZMeOH3mBvPUYg3CmuYTUTC25oMEQ1iNEY1aJVE'
    OAUTH_TOKEN = '1099418492082839552-a4OOwpTP6EjYQojvLDKdR70EmIqytt'
    OAUTH_TOKEN_SECRET = 'pOtK9x1SBtdeRQZT86Iy74PpxscWko1fWIdnuYVpYculB'
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api
twitter_api = oauth_login()

'''
# 1. choose a user and get her info
screen_name = 'Pokka_Peach'
response_info = twitter_api.users.show(screen_name=screen_name)
print('INFO:\n', json.dumps(response_info, sort_keys=True, indent=1))


# 2. get her friends list
response_frds = twitter_api.friends.ids(screen_name=screen_name, count=5000)
print ('\nFRIENDS LIST:\n', json.dumps(response_frds, indent=1,sort_keys=True))
friends = response_frds["ids"]
print('got {0} friends for {1}'.format(len(friends), screen_name))
# 2. get his followers list
response_followers = twitter_api.followers.ids(screen_name=screen_name, count=5000)
print ('\nFOLLOWERS LIST:\n', json.dumps(response_followers, indent=1,sort_keys=True))
followers = response_followers["ids"]
print('got {0} followers for {1}'.format(len(followers), screen_name))
'''

# 3. use the above two lists to find reciporical friends
def get_rf(screen_name):
    fds = (twitter_api.friends.ids(screen_name=screen_name, count=5000))['ids']
    folrs = (twitter_api.followers.ids(screen_name=screen_name, count=5000))['ids']
    rf = set(fds) & set(folrs)
    return rf
'''
print('\nRECIPROCAL FRIENDS LIST:\n')
reciprocal_friends = get_rf('Pokka_Peach')
for people in reciprocal_friends:
    print(people)
print('got {0} reciprocal friends for {1}'.format(len(reciprocal_friends), screen_name))
'''
# 4. top 5 popular friends
# retrieve profiles of reciprocal friends

def make_twitter_request(twitter_api_func, max_errors=10, *args, **kw):
    # A nested helper function that handles common HTTPErrors. Return an updated
    # value for wait_period if the problem is a 500 level error. Block until the
    # rate limit is reset if it's a rate limiting issue (429 error). Returns None
    # for 401 and 404 errors, which requires special handling by the caller.
    def handle_twitter_http_error(e, wait_period=2, sleep_when_rate_limited=True):

        if wait_period > 3600:  # Seconds
            print('Too many retries. Quitting.', file=sys.stderr)
            raise e

        # See https://developer.twitter.com/en/docs/basics/response-codes
        # for common codes

        if e.e.code == 401:
            print('Encountered 401 Error (Not Authorized)', file=sys.stderr)
            return None
        elif e.e.code == 404:
            print('Encountered 404 Error (Not Found)', file=sys.stderr)
            return None
        elif e.e.code == 429:
            print('Encountered 429 Error (Rate Limit Exceeded)', file=sys.stderr)
            if sleep_when_rate_limited:
                print("Retrying in 15 due to twitter's API constraints", file=sys.stderr)
                sys.stderr.flush()
                time.sleep(60 * 15 + 5)
                print('Alright, it\'s go time once again, ready to retry.', file=sys.stderr)
                return 2
            else:
                raise e  # Caller must handle the rate limiting issue
        elif e.e.code in (500, 502, 503, 504):
            print('Encountered {0} Error. Retrying in {1} seconds'.format(e.e.code, wait_period), file=sys.stderr)
            time.sleep(wait_period)
            wait_period *= 1.5
            return wait_period
        else:
            raise e

    # End of nested helper function

    wait_period = 2
    error_count = 0

    while True:
        try:
            return twitter_api_func(*args, **kw)
        except twitter.api.TwitterHTTPError as e:
            error_count = 0
            wait_period = handle_twitter_http_error(e, wait_period)
            if wait_period is None:
                return
        except URLError as e:
            error_count += 1
            time.sleep(wait_period)
            wait_period *= 1.5
            print("URLError encountered. Continuing.", file=sys.stderr)
            if error_count > max_errors:
                print("Too many consecutive errors...bailing out.", file=sys.stderr)
                raise
        except BadStatusLine as e:
            error_count += 1
            time.sleep(wait_period)
            wait_period *= 1.5
            print("BadStatusLine encountered. Continuing.", file=sys.stderr)
            if error_count > max_errors:
                print("Too many consecutive errors...bailing out.", file=sys.stderr)
                raise


def get_user_profile(twitter_api, screen_names=None, user_ids=None):
    # Must have either screen_name or user_id (logical xor)
    assert (screen_names != None) != (user_ids != None), "Must have screen_names or user_ids, but not both"

    items_to_info = {}

    items = screen_names or user_ids

    while len(items) > 0:

        # Process 100 items at a time per the API specifications for /users/lookup.
        # See http://bit.ly/2Gcjfzr for details.

        items_str = ','.join([str(item) for item in items[:100]])
        items = items[100:]

        if screen_names:
            response = make_twitter_request(twitter_api.users.lookup,
                                            screen_name=items_str)
        else:  # user_ids
            response = make_twitter_request(twitter_api.users.lookup,
                                            user_id=items_str)

        for user_info in response:
            if screen_names:
                items_to_info[user_info['screen_name']] = user_info
            else:  # user_ids
                items_to_info[user_info['id']] = user_info

    return items_to_info


def get_top5(rf):
    top5s = []
    for id in list(rf):
        [one_rf] = list(get_user_profile(twitter_api, user_ids=[id]).values())
        top5s.append((one_rf['id'], one_rf['followers_count']))
        top5s.sort(key=lambda x: x[1], reverse=True)
    return [person[0] for person in top5s[:5]]
'''
a = get_top5(reciprocal_friends)
print('\nTOP 5 POPULAR FRIENDS:\n')
for i in a:
    print(i)

print('\n\n####################################################################')'''
# 5. crawl 100 nodes
'''
screen_name = 'DWade'
level = 0
max_level = 2
while level < max_level:
    for n in screen_name:
        rf = get_rf(screen_name)
        f = get_top5(rf)
    print('level {0} friends:\n'.format(level), len(f), '\n', f)
    level += 1
    screen_name = []
    for n in f:
        screen_name.append(twitter_api.users.show(user_id=str(n))['screen_name'])
    if len(f) > 100:
        break
'''


screen_name = 'katyperry'
response = make_twitter_request(twitter_api.followers.ids, screen_name=screen_name, count=5000)
ids = next_queue = response['ids']
level = 1
max_level = 3
while level < max_level: level += 1
(queue, next_queue) = (next_queue, [])
for id in queue:
    response = make_twitter_request(twitter_api.followers.ids, user_id=id, count = 5000)
    next_queue += response['ids']
    ids += next_queue
print(ids)


# END OF PROGRAM
