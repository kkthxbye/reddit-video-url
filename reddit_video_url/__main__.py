from argparse import ArgumentParser
from json import loads
from typing import Dict, List, Optional, Union
from urllib.request import Request, urlopen
import sys


def extract_url(post: Union[List, Dict]) -> Optional[Union[Dict, List, str]]:
    if isinstance(post, List):
        post = dict(enumerate(post))

    return next((x for x in (
        v if k == 'fallback_url'
        else extract_url(v) if isinstance(v, (dict, list))
        else None
        for k, v in post.items()
    ) if x is not None), None)


def load_post_json(url: str, user_agent: Optional[str] = None) -> Optional[str]:
    req = Request(url.rstrip('/') + '.json', data=None, headers={
        'User-Agent': user_agent,
    })
    return urlopen(req).read()


if __name__ == '__main__':
    parser = ArgumentParser(description='Get reddit video url')
    parser.add_argument('url', metavar='URL', type=str, help='Post url')
    parser.add_argument('--user-agent',
                        help='User agent to scrape with',
                        default='Direct video URL scraper')
    args = parser.parse_args()

    sys.stdout.write(extract_url(loads(
        load_post_json(args.url, args.user_agent)
    )))

    # print(extract_url(loads(load_post_json(args.url, args.user_agent))))
