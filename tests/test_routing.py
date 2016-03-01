import requests
import pytest
from lxml.html import fromstring


class TestRouting:
    ''' Handles the routing tests and assertion
        as well as the global pass/fail state
        the methods with test_ in their names will be run automatically.
    '''

    def root(self):
        '''Hack to get the root url initially'''
        return 'http://localhost:8775/'

    def status_code(self, url):
        ''' Gets http status codes of pages/urls '''
        try:
            r = requests.head(url)
            return r.status_code
        except requests.ConnectionError:
            return None

    def page_title(self, url):
        ''' Get the lexed title from the html '''
        try:
            r = requests.get(url)
            tree = fromstring(r.content)
            return tree.findtext('.//title')
        except requests.ConnectionError:
            return None

    def test_root_url_config_works(self):
        ''' Ensure root is configured '''
        assert (self.root() is not None and
                len(str(self.root())) > 5)

    def test_root_url_loads(self):
        assert (self.root() and
                (200 == self.status_code(self.root())))

    def test_root_url_has_right_title(self):
        title = 'Sample of main tinker page'
        assert (self.page_title(self.root()) == title)

    @pytest.mark.skipif("True")
    def test_root_url_has_right_title_without_trailing_slash(self):
        url = self.root()
        title = 'Sample of main tinker page'
        assert (self.page_title(url.rstrip('/')) == title)

    def test_urls_should_200(self):
        urls = [
            '', 'title-test.html'
        ]
        for url in urls:
            assert (str(self.root()) + url is not None and 200 ==
                    self.status_code(str(self.root()) + url))

    def test_urls_that_should_redirect(self):
        urls = [        ]
        for url in urls:
            full_uri = str(self.root()) + url
            assert str(self.root()) + url is not None
            assert isinstance(self.status_code(full_uri), int)
            assert url and (
                301 == self.status_code(str(self.root()) + url) or
                302 == self.status_code(str(self.root()) + url))

    def test_urls_should_404(self):
        urls = ['thisshould404', 'shoppinginthesudan',
                'js/doesnotexist.js']
        for url in urls:
            assert (404 == self.status_code(str(self.root()) + url))

    def test_urls_by_title(self):
        root = self.root()
        assert root is not None
        pages = {'title-test.html': 'Test',
                 }
        for url, title in pages.items():
            assert (bool(title) and bool(url) and
                    None is not self.page_title(root + url))
            assert (bool(title) and bool(url) and
                    title in self.page_title(root + url))
