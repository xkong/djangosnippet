# coding: utf-8
#
# xiaoyu <xiaokong1937@gmail.com>
#
# 2014/11/27
#
"""
Second-level-URL Dispatcher

Second-level-URL is the first directory after the domain in a URL.For
instance, in the URL `http://ninan.sinaapp.com/note/author/xiaoyu/` ,
`note` is the second-level-URL.
We use this dispatcher to dispatch URLs to the specific app, adding a
new property to the `request` object with second-level-URL name in it.

Put this middleware *before* django.middleware.common.CommonMiddleware.
In your settings.py, add `SAFE_URLS` as a list stands for the
second-level-URLs you don't want to dispatch.
In your setiings.py, add `PREFIX_PORTION_NAME` as a string that stands for
the cookie name of prefix_protion(alternative).
In your views.py, write views to handler the result.

def someview(request):
    prefix = getattr(settings, 'PREFIX_PORTION_NAME', 'script-prefix-protion')
    prefix_protion = request.COOKIES.get(prefix, '')
    if prefix_protion:
        do_something()

"""
from django.conf import settings


class SecondLevelURLDispatherMw(object):
    """
    Dispatch URLs to the specific app.

    """
    def process_request(self, request):
        host = request.get_host()
        old_url = [host, request.path]
        new_url = old_url[:]
        rewrite_urls = getattr(settings, 'REWRITE_URLS', [])
        safe_url_prefix = getattr(settings, 'SAFE_URL_PREFIX', [])
        prefix_portion_name = getattr(settings,
                                      'PREFIX_PORTION_NAME',
                                      'script-prefix-portion')
        if not rewrite_urls:
            return
        url_splices = new_url[1].split('/')
        if len(url_splices) < 3:
            return
        if url_splices[1] in safe_url_prefix:
            return
        if url_splices[2] not in rewrite_urls:
            return
        else:
            request.COOKIES[prefix_portion_name] = url_splices[1]
            url_splices.pop(1)
            request.path_info = '/'.join(splice for splice in url_splices)
