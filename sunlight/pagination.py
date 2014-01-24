import time
import logging

logger = logging.getLogger('sunlight.paginator')


def pageable(func):
    func.is_pageable = True
    return func


class PagingService(object):

    limit_attr = 'limit'
    page_attr = 'page'
    per_page_attr = 'per_page'

    delay = 0.1

    def __init__(self, service=None, delay=None):

        if service:
            self.service = service
        else:
            self.service = self.service_class()

        if not getattr(self.service, 'is_pageable', False):
            raise ValueError('service must be a pagable service')

        if delay is not None:
            self.delay = delay

    def __getattr__(self, name):

        attr = getattr(self.service, name, None)

        if callable(attr) and getattr(attr, 'is_pageable', False):

            def pagingfunc(*args, **kwargs):

                count = 0

                page = int(kwargs.get(self.page_attr, 1))
                per_page = int(kwargs.get(self.per_page_attr, 50))
                limit = int(kwargs.pop(self.limit_attr, per_page))

                per_page = min(limit, per_page)

                kwargs[self.per_page_attr] = per_page
                kwargs[self.page_attr] = 1

                stopthepresses = False

                while 1:

                    logger.debug('loading %s page %d' % (name, page))

                    kwargs[self.page_attr] = page
                    resp = attr(*args, **kwargs)

                    for rec in resp:

                        yield rec

                        count += 1

                        if count >= limit:
                            logger.debug('!   count exceeded limit, stopping')
                            stopthepresses = True
                            break

                    if count % per_page != 0:
                        logger.debug('!   %s returned less than number of requested results, stopping' % name)
                        stopthepresses = True

                    if stopthepresses:
                        break

                    page += 1
                    time.sleep(self.delay)

            return pagingfunc

        return attr
