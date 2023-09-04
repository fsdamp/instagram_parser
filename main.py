from typing import List, Dict

from instaloader import NodeIterator, Post, Profile, Instaloader


class InstagramParser:
    def __init__(self, username: str):
        self.client: Profile = self._load_client(username)
        self.post_iterator = self.client.get_posts()

    def __iter__(self):
        return self

    def __next__(self) -> Dict:
        try:
            post = next(self.post_iterator)
            return self._reformat_post(post)
        except StopIteration:
            raise StopIteration

    def get_posts_as_list(self) -> List[Dict]:

        data = []
        for post in self.post_iterator:
            data.append(self._reformat_post(post))
        return data

    def _reformat_post(self, post: Post) -> Dict:
        if post.typename in ['GraphImage', 'GraphSidecar']:
            return {
                'title': post.title,
                'caption': post.caption,
                'caption_hashtags': post.caption_hashtags,
                'media_id': post.mediaid,
                'owner_id': post.owner_id,
                'date_utc': post.date_utc,
                'typename': post.typename,
                'media_count': post.mediacount,
                'images': self._get_node_images(post) if post.typename == 'GraphSidecar' else [post.url]
            }
        else:
            return {}

    @staticmethod
    def _get_node_images(post):
        return [i.display_url for i in post.get_sidecar_nodes()]

    @staticmethod
    def _load_client(username: str) -> Profile:
        loader = Instaloader()
        client = Profile.from_username(loader.context, username)
        return client


# Пример использования
from pprint import pprint

scrape = InstagramParser(username='foxybeauty_salon')
posts = scrape.get_posts_as_list()
pprint(posts)

iterator = InstagramParser(username='foxybeauty_salon')
print(iterator.__next__())
print(iterator.__next__())
