# -*- coding: utf-8 -*-
import oauth2 as oauth
from django.test import TestCase

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
