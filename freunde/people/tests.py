# -*- coding: utf-8 -*-
import oauth2 as oauth

from django.test import TestCase
from django.utils import simplejson as json

signiture_method = oauth.SignatureMethod_HMAC_SHA1()
consumer = oauth.Consumer('key', 'secret')
token = None

class SimpleTest(TestCase):
    fixtures = ['people']

    def get_headers(self, path, method='GET', params=None):
        url = 'http://testserver%s' % path
        params = params or {}

        req = oauth.Request.from_consumer_and_token(
            consumer,
            token,
            http_method=method,
            http_url=url,
            parameters=params)
        req.sign_request(signiture_method, consumer, token)

        headers = req.to_header()

        return { 'HTTP_AUTHORIZATION': headers.get('Authorization', '') }

    def test_people_self(self):
        """
        Tests people_self
        """
        params = {}
        path = '/people/1/@self'
        headers = self.get_headers(path, 'GET', params)
        res = self.client.get(path, params, **headers)
        self.failUnlessEqual(res.status_code, 200)

    def test_people_self_has_app(self):
        """
        Tests people_self
        """
        params = {}
        path = '/people/1/@self'
        headers = self.get_headers(path, 'GET', params)
        res = self.client.get(path, params, **headers)
        self.failUnlessEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertEquals(data['entry']['hasApp'], True)

        path = '/people/2/@self'
        headers = self.get_headers(path, 'GET', params)
        res = self.client.get(path, params, **headers)
        self.failUnlessEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertEquals(data['entry']['hasApp'], False)

    def test_people_me_self(self):
        """
        Tests /people/@me/@self
        """
        params = { 'xoauth_requestor_id': 1 }
        path = '/people/@me/@self'
        headers = self.get_headers(path, 'GET', params)
        res = self.client.get(path, params, **headers)
        self.failUnlessEqual(res.status_code, 200)

    def test_people_me_self_without_xoauth_requestor_id(self):
        """
        Tests /people/@me/@self without xoauth_requestor_id
        """
        params = {}
        path = '/people/@me/@self'
        headers = self.get_headers(path, 'GET', params)
        res = self.client.get(path, params, **headers)
        self.failUnlessEqual(res.status_code, 400)

    def test_people_friends_filter_by_error(self):
        """
        Tests /people/1/@friends, but filterBy value is invalid
        """
        path = '/people/1/@friends'
        params = { 'xoauth_requestor_id': 1,
                   'filterBy': 'spam',
                   }
        headers = self.get_headers(path, 'GET', params)
        res = self.client.get(path, params, **headers)
        self.assertEquals(res.status_code, 400)

    def test_people_friends_filter_by_has_app(self):
        """
        Tests /people/1/@friends filtered by hasApp
        """
        path = '/people/1/@friends'

        params = { 'xoauth_requestor_id': 1,
                   'filterBy'           : 'hasApp',
                   'count'              : 500,
                   }
        headers = self.get_headers(path, 'GET', params)
        res = self.client.get(path, params, **headers)
        self.assertEquals(res.status_code, 200)

        data1 = json.loads(res.content)
        self.assertEqual(all([x['hasApp'] for x in data1.get('entry')]), True)

        params = { 'xoauth_requestor_id': 1,
                   'count'              : 500,
                   }
        headers = self.get_headers(path, 'GET', params)
        res = self.client.get(path, params, **headers)
        self.assertEquals(res.status_code, 200)

        data2 = json.loads(res.content)
        self.assertEqual([x['id'] for x in data1.get('entry') if x['hasApp']],
                         [x['id'] for x in data2.get('entry') if x['hasApp']])

    def test_people_friends(self):
        """
        Tests /people/1/@friends
        """
        path = '/people/1/@friends'
        params = { 'xoauth_requestor_id': 1 }

        headers = self.get_headers(path, 'GET', params)
        res = self.client.get(path, params, **headers)
        self.assertEquals(res.status_code, 200)

        data = json.loads(res.content)
        self.assertEquals(data.get('totalResults'), 239)
        self.assertEquals(data.get('startIndex'), 0)
        self.assertEquals(data.get('itemPerPage'), 50)

        seq = []
        for x in xrange(0, 5):
            index = x * 10
            params = { 'xoauth_requestor_id': 1,
                       'count'              : 10,
                       'startIndex'         : index,
                       }
            headers = self.get_headers(path, 'GET', params)
            res = self.client.get(path, params, **headers)
            self.assertEquals(res.status_code, 200)

            tmp = json.loads(res.content)
            self.assertEquals(tmp.get('totalResults'), 239)
            self.assertEquals(tmp.get('startIndex'), index)
            self.assertEquals(tmp.get('itemPerPage'), 10)

            seq.extend(tmp.get('entry', []))

        self.assertEquals([x['id'] for x in data.get('entry', [])],
                          [x['id'] for x in seq])
