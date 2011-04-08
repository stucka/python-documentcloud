"""
Python library for interacting with the DocumentCloud API.

DocumentCloud's API can search, upload, edit and organize documents hosted
in its system. Public documents are available without an API key, but 
authorization is required to interact with private documents.

Further documentation:

    https://www.documentcloud.org/help/api

"""
import urllib, urllib2
import datetime
try:
    import json
except ImportError:
    import simplejson as json


class BaseAPIObject(object):
    """
    An abstract version of the objects returned by the API.
    """

    def __init__(self, d):
        self.__dict__ = d
    
    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.__str__())
    
    def __str__(self):
        return self.__unicode__().encode("utf-8")
    
    def __unicode__(self):
        return unicode(self.title)


class Document(BaseAPIObject):
    """
    A document returned by the API.
    """
    def __init__(self, d):
        self.__dict__ = d
        self.resources = Resource(d.get("resources"))
    
    def get_full_text_url(self):
        return self.resources.text
    full_text_url = property(get_full_text_url)
    
    def get_full_text(self):
        req = urllib2.Request(self.full_text_url)
        response = urllib2.urlopen(req)
        return response.read()
    full_text = property(get_full_text)
    
    def get_page_text_url(self, page):
        template = self.resources.page.get('text')
        url = template.replace("{page}", str(page))
        return url
    
    def get_page_text(self, page):
        url = self.get_page_text_url(page)
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        return response.read()
    
    #
    # Images
    #
    
    def get_pdf_url(self):
        return self.resources.pdf
    pdf_url = property(get_pdf_url)
    
    def get_pdf(self):
        req = urllib2.Request(self.pdf_url)
        response = urllib2.urlopen(req)
        return response.read()
    pdf = property(get_pdf)
    
    def get_small_image_url(self, page=1):
        template = self.resources.page.get('image')
        url = template.replace("{page}", str(page)).replace("{size}", "small")
        return url
    small_image_url = property(get_small_image_url)
    
    def get_thumbnail_image_url(self, page=1):
        template = self.resources.page.get('image')
        url = template.replace("{page}", str(page)).replace("{size}", "thumbnail")
        return url
    thumbnail_image_url = property(get_thumbnail_image_url)
    
    def get_large_image_url(self, page=1):
        template = self.resources.page.get('image')
        url = template.replace("{page}", str(page)).replace("{size}", "large")
        return url
    large_image_url = property(get_large_image_url)
    
    def get_small_image_url_list(self):
        return [self.get_small_image_url(i) for i in range(1, self.pages +1)]
    small_image_url_list = property(get_small_image_url_list)
    
    def get_thumbnail_image_url_list(self):
        return [self.get_thumbnail_image_url(i) for i in range(1, self.pages +1)]
    thumbnail_image_url_list = property(get_thumbnail_image_url_list)
    
    def get_large_image_url_list(self):
        return [self.get_large_image_url(i) for i in range(1, self.pages +1)]
    large_image_url_list = property(get_large_image_url_list)
    
    def get_small_image(self, page=1):
        url = self.get_small_image_url(page=page)
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        return response.read()
    small_image = property(get_small_image)
    
    def get_thumbnail_image(self, page=1):
        url = self.get_thumbnail_image_url(page=page)
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        return response.read()
    thumbnail_image = property(get_thumbnail_image)
    
    def get_large_image(self, page=1):
        url = self.get_large_image_url(page=page)
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        return response.read()
    large_image = property(get_large_image)


class Project(BaseAPIObject):
    """
    A project returned by the API.
    """
    pass


class Resource(BaseAPIObject):
    """
    The resources associated with a Document. Hyperlinks and such.
    """
    def __repr__(self):
        return '<%ss>' % self.__class__.__name__
    
    def __str__(self):
        return self.__unicode__().encode("utf-8")
    
    def __unicode__(self):
        return u''


class documentcloud(object):
    """
    The main public method for interacting with the API.
    """
    
    BASE_URL = u'https://www.documentcloud.org/api/'
    # For storing calls we've already made.
    # URLs will be keys, responses will be values
    _cache = {}

    #
    # Private methods
    #
    
    @staticmethod
    def _get_search_page(query, page, per_page):
        """
        Retrieve one page of search results from the DocumentCloud API.
        """
        url = documentcloud.BASE_URL + u'search.json'
        params = {
            'q': query,
            'page': page,
            'per_page': per_page,
        }
        params = urllib.urlencode(params)
        req = urllib2.Request(url, params)
        response = urllib2.urlopen(req)
        data = response.read()
        return json.loads(data).get("documents")

    # 
    # Public methods
    #

    class documents(object):
        """
        Methods for collecting Documents.
        """
        
        @staticmethod
        def search(query):
            """
            Retrieve all objects that make a search query.
            
            Example usage:
            
                >> documentcloud.documents.search('salazar')
                
            """
            page = 1
            document_list = []
            while True:
                results = documentcloud._get_search_page(query, page=page, per_page=1000)
                if results:
                    document_list += results
                    page += 1
                else:
                    break
            return [Document(d) for d in document_list]


if __name__ == '__main__':
    from pprint import pprint
    document_list = documentcloud.documents.search('ruben salazar')
    obj = document_list[0]
    pprint(obj.__dict__)
    pprint(obj.resources.__dict__)
    print obj.get_page_text(1)







