# -*- coding: utf-8 -*-
"""
Created: 9:47 PM on 2/23/20
Author: Mike Moger
Usage: https://patchstorage.com/docs/
"""

import os
import json
import urllib3
import certifi
import datetime
from furl import furl
from zoia_lib.patch import ZoiaPatch
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                           ca_certs=certifi.where())

manifest = {
    'categories': [
        {'id': 378,
            'self': 'https://patchstorage.com/api/alpha/categories/378',
            'description': '',
            'slug': 'composition',
            'name': 'Composition'},
        {'id': 77,
            'self': 'https://patchstorage.com/api/alpha/categories/77',
            'description': '',
            'slug': 'effect',
            'name': 'Effect'},
        {'id': 3317,
            'self': 'https://patchstorage.com/api/alpha/categories/3317',
            'description': '',
            'slug': 'game',
            'name': 'Game'},
        {'id': 1,
            'self': 'https://patchstorage.com/api/alpha/categories/1',
            'description': '',
            'slug': 'other',
            'name': 'Other'},
        {'id': 75,
            'self': 'https://patchstorage.com/api/alpha/categories/75',
            'description': '',
            'slug': 'sampler',
            'name': 'Sampler'},
        {'id': 76,
            'self': 'https://patchstorage.com/api/alpha/categories/76',
            'description': '',
            'slug': 'sequencer',
            'name': 'Sequencer'},
        {'id': 372,
            'self': 'https://patchstorage.com/api/alpha/categories/372',
            'description': '',
            'slug': 'sound',
            'name': 'Sound'},
        {'id': 74,
            'self': 'https://patchstorage.com/api/alpha/categories/74',
            'description': '',
            'slug': 'synthesizer',
            'name': 'Synthesizer'},
        {'id': 117,
            'self': 'https://patchstorage.com/api/alpha/categories/117',
            'description': '',
            'slug': 'utility',
            'name': 'Utility'},
        {'id': 91,
            'self': 'https://patchstorage.com/api/alpha/categories/91',
            'description': '',
            'slug': 'video',
            'name': 'Video'}
    ],
    'states': [
        {'id': 149,
            'self': 'https://patchstorage.com/api/alpha/states/149',
            'description': '',
            'slug': 'help-needed',
            'name': 'Help Needed'},
        {'id': 1098,
            'self': 'https://patchstorage.com/api/alpha/states/1098',
            'description': '',
            'slug': 'inactive',
            'name': 'Inactive'},
        {'id': 151,
            'self': 'https://patchstorage.com/api/alpha/states/151',
            'description': '',
            'slug': 'ready-to-go',
            'name': 'Ready to Go'},
        {'id': 150,
            'self': 'https://patchstorage.com/api/alpha/states/150',
            'description': '',
            'slug': 'work-in-progress',
            'name': 'Work in Progress'}
    ],
    'licenses': [
        {'id': 4184,
            'self': 'https://patchstorage.com/api/alpha/licenses/4184',
            'description': '',
            'slug': 'afl-3-0',
            'name': 'Academic Free License v3.0'},
        {'id': 4173,
            'self': 'https://patchstorage.com/api/alpha/licenses/4173',
            'description': '',
            'slug': 'apache-2-0',
            'name': 'Apache License 2.0'},
        {'id': 4185,
            'self': 'https://patchstorage.com/api/alpha/licenses/4185',
            'description': '',
            'slug': 'artistic-2-0',
            'name': 'Artistic license 2.0'},
        {'id': 4186,
            'self': 'https://patchstorage.com/api/alpha/licenses/4186',
            'description': '',
            'slug': 'bsl-1-0',
            'name': 'Boost Software License 1.0'},
        {'id': 4174,
            'self': 'https://patchstorage.com/api/alpha/licenses/4174',
            'description': '',
            'slug': 'bsd-2-clause',
            'name': 'BSD 2-Clause "Simplified" License'},
        {'id': 4175,
            'self': 'https://patchstorage.com/api/alpha/licenses/4175',
            'description': '',
            'slug': 'bsd-3-clause',
            'name': 'BSD 3-Clause "New" or "Revised" License'},
        {'id': 4187,
            'self': 'https://patchstorage.com/api/alpha/licenses/4187',
            'description': '',
            'slug': 'bsd-3-clause-clear',
            'name': 'BSD 3-clause Clear license'},
        {'id': 4190,
            'self': 'https://patchstorage.com/api/alpha/licenses/4190',
            'description': '',
            'slug': 'cc-by-4-0',
            'name': 'Creative Commons Attribution 4.0'},
        {'id': 4191,
            'self': 'https://patchstorage.com/api/alpha/licenses/4191',
            'description': '',
            'slug': 'cc-by-sa-4-0',
            'name': 'Creative Commons Attribution Share Alike 4.0'},
        {'id': 4188,
            'self': 'https://patchstorage.com/api/alpha/licenses/4188',
            'description': '',
            'slug': 'cc',
            'name': 'Creative Commons license family'}

    ]
}


class PatchStorage:

    def __init__(self):
        """initializes PatchStorage class"""

        # set defaults for query params
        self.url = 'https://patchstorage.com/api/alpha/'
        self.platform = '3003'  # ZOIA
        self.state = '151'  # Ready-to-Go
        # self.author = '2825'  # HPC, '2953' CHMJ

    @staticmethod
    def validate_str(s: str):
        if type(s) != 'str':
            return str(s)

    def validate_strlist(self, lst: list):
        return [self.validate_str(s) for s in lst]

    @staticmethod
    def validate_int(v: int):
        if type(v) != 'int':
            return int(v)

    def validate_intlist(self, lst: list):
        return [self.validate_int(v) for v in lst]

    @staticmethod
    def validate_date(date: str):
        try:
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
            return date.isoformat()
        except ValueError:
            raise ValueError('Incorrect data format, should be YYYY-MM-DD')

    def endpoint(self,
                 endpoint: str):
        """specify endpoint for query"""

        return os.path.join(self.url, endpoint)

    def search(self,
               more_params: dict = {}):
        """make query and output json body
        default args:
            - page (int): current page, default 1
            - per_page (int): max number to return, default 10
            - order (str enum): [asc, desc], order sort, default desc
            - orderby (str enum): [author, date, id, modified, slug, title
                                   relevance (must include search term)],
                                        order sort by, default date
        optional args:
            - search (str): search for given string
            - before (str): published before given ISO8601 date
            - after (str): published after given ISO8601 date
            - exclude (str): exclude specific id(s)
            - include (str): include specific id(s)
            - offset (int): offset by number of items
            - slug (str): [], search for given slug(s)
            - author (str): search for items by an author(s)
            - author_exclude (str): exclude specific author(s)
            - categories (int): [], search for items with a category(ies)
            - categories_exclude (int): [], exclude specific category(ies)
            - tags (int): [], search for items with tag(s)
            - tags_exclude (int): [], exclude specific tag(s)
            - platforms (int): [], search for items within a platform
            - platforms_exclude (int): [], exclude specific platform(s)
            - states (int): [], search for items with a given state
            - states_exclude (int); [], exclude specific state(s)

        see `manifest` dictionary for a breakdown of categories, states, and licenses
        """

        endpoint = self.endpoint('patches?/')

        # get param dict
        default_params = {
            'page': 1,
            'per_page': 25,
            'order': 'desc',
            'orderby': 'date',
            'platforms': self.platform,
            'states': self.state,
        }

        # check type of optional args
        for key in list(more_params.keys()):
            if key in ['before', 'after']:
                more_params[key] = self.validate_date(more_params[key])
            if key in ['search', 'exclude', 'include', 'order',
                       'orderby', 'slug', 'author', 'author_exclude']:
                more_params[key] = self.validate_str(more_params[key])
            if key in ['offset', 'categories', 'categories_exclude',
                       'tags', 'tags_exclude', 'page', 'platforms',
                       'platforms_exclude', 'states', 'states_exclude']:
                more_params[key] = self.validate_int(more_params[key])

        params = {**default_params, **more_params}

        # make request
        url = str(furl(endpoint).add(params))
        r = http.request('GET', url)

        return json.loads(r.data)

    def get_list(self,
                 more_params: dict = {}):
        """get list of returned objects"""

        body = self.search(more_params)

        return dict(zip([str(x['title']) for x in body],
                        [str(x['self']+'?/') for x in body]))

    def get_tags(self,
                 more_params: dict = {}):
        """get list of tags"""

        body = self.search(more_params)

        return dict(zip([str(x['title']) for x in body],
                        [str(x['tags']) for x in body]))

    def get_patch(self,
                  idx: str):
        """get Patch object"""

        endpoint = self.endpoint('patches/{}?/'.format(idx))

        # make request
        r = http.request('GET', endpoint)

        return json.loads(r.data)

    def download(self,
                 idx: str):
        """download file using patch id"""

        body = self.get_patch(idx)

        path = str(body['files'][0]['url'])
        fname = str(body['files'][0]['filename'])

        with open(fname, 'wb') as out:
            rr = http.request('GET', path)
            data = rr.data
            out.write(data)


def ZoiaPatchFromAPI(body):
    """Create ZoiaPatch objects from PS returns"""

    dct = {}
    for patch in body:
        dct[patch['id']] = ZoiaPatch(obj=patch)

    return dct


def get_all_tags():
    """get master dict of all tag id's and slugs"""

    ps = PatchStorage()
    search = {'orderby': 'title',
              'order': 'asc',
              'per_page': 100}

    tags = {}
    for page in range(1, 6):
        body = ps.search({**search, **{'page': page}})
        for patch in body:
            more = dict(zip([s['id'] for s in patch['tags']],
                            [s['slug'] for s in patch['tags']]))

            # remove any duplicate tags
            for idx in set(more).intersection(set(tags)):
                more.pop(idx, None)
            tags = {**tags, **more}

    with open('zoia_lib/common/tags.json', 'w') as f:
        json.dump(tags, f)
