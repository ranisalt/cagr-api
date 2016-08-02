from aiohttp import web
from collections import defaultdict
from configparser import ConfigParser
from hubstorage import HubstorageClient


config = ConfigParser()
config.read('shub.cfg')

shub_cfg = config['shub']


class Hub:
    def __init__(self, project: str, spider: str):
        hc = HubstorageClient(auth=shub_cfg.get('apikey'))
        key = next(hc.get_project(project).jobq.list(spider=spider)).get('key')
        self.job = hc.get_job(key)

    def items(self):
        return self.job.items.list()


class Subject:
    def __init__(self, _id: str, name: str, hours: int, classes: dict):
        self._id = _id
        self.name = name
        self.hours = hours
        self.classes = classes


api = Hub(shub_cfg.get('project'), shub_cfg.get('spider'))


async def get_items(campus: str=None, subject: str=None, name: str=None)-> dict:
    filtered = api.items()
    if campus is not None:
        filtered = (s for s in filtered if s['campus'] == campus)
    if subject is not None:
        filtered = (s for s in filtered if s['id'] == subject)
    if name is not None:
        filtered = (s for s in filtered if name in s['name'])
    return filtered
