# -*- coding: utf-8 -*-

import simplejson as json

from collections import UserList

from soundcloud.client import Client as BaseClient, make_request


class Resource(object):
    """Object wrapper for resources.

    Provides an object interface to resources returned by the Soundcloud API.
    """
    def __init__(self, obj):
        self.obj = obj
        if hasattr(self, 'origin'):
            if self.origin is None:
                self.origin = None
            else:
                self.origin = Resource(self.origin)

    def __getstate__(self):
        return self.obj.items()

    def __setstate__(self, items):
        if not hasattr(self, 'obj'):
            self.obj = {}
        for key, val in items:
            self.obj[key] = val

    def __getattr__(self, name):
        if self.obj and name in self.obj:
            return self.obj.get(name)

        raise AttributeError

    def fields(self):
        return self.obj

    def keys(self):
        return self.obj.keys()


class ResourceList(UserList):
    """Object wrapper for lists of resources."""
    def __init__(self, resources=None):
        if resources is None:
            resources = []

        data = []
        for resource in resources:
            data.append(Resource(resource))

        super(ResourceList, self).__init__(data)


def wrapped_resource(response):
    """Return a response wrapped in the appropriate wrapper type.

    Lists will be returned as a ```ResourceList``` instance,
    dicts will be returned as a ```Resource``` instance.
    """
    # decode response text, assuming utf-8 if unset
    response_content = response.content.decode(response.encoding or 'utf-8')

    try:
        content = json.loads(response_content)
    except ValueError:
        # not JSON
        content = response_content

    if isinstance(content, list):
        result = ResourceList(content)
    else:
        result = Resource(content)
        if hasattr(result, 'collection'):
            result.collection = ResourceList(result.collection)

    result.raw_data = response_content

    for attr in ('encoding', 'url', 'status_code', 'reason'):
        setattr(result, attr, getattr(response, attr))

    return result


class Client(BaseClient):

    def _request(self, method, resource, **kwargs):
        """Given an HTTP method, a resource name and kwargs, construct a
        request and return the response.
        """
        url = self._resolve_resource_name(resource)

        if hasattr(self, 'access_token'):
            kwargs.update(dict(oauth_token=self.access_token))
        if hasattr(self, 'client_id'):
            kwargs.update(dict(client_id=self.client_id))

        kwargs.update({
            'verify_ssl': self.options.get('verify_ssl', True),
            'proxies': self.options.get('proxies', None)
        })
        return wrapped_resource(make_request(method, url, kwargs))
