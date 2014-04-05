try:
    import unittest2 as unittest
except ImportError:
    import unittest

import sunlight
from sunlight.service import EntityDict, EntityList
from sunlight.errors import BadRequestException


class TestCongress(unittest.TestCase):

    def setUp(self):
        self.bioguide_id = 'L000551'
        self.thomas_id = '01501'
        self.ocd_id = 'ocd-division/country:us/state:ca/cd:13'
        self.lat = 35.933333
        self.lon = -79.033333

    def test_get_badpath(self):
        with self.assertRaises(BadRequestException):
            resp = sunlight.congress.get(['foo', 'bar'])

    def test__get_url(self):
        url = sunlight.congress._get_url(['bills'],
                                         sunlight.config.API_KEY)

        expected_url = "{base_url}/bills?apikey={apikey}".format(
            base_url='https://congress.api.sunlightfoundation.com',
            apikey=sunlight.config.API_KEY)

        self.assertEqual(url, expected_url)

    def test_pathlist__get_url(self):
        url = sunlight.congress._get_url(['legislators', 'locate'],
                                         sunlight.config.API_KEY)

        expected_url = "{base_url}/legislators/locate?apikey={apikey}".format(
            base_url='https://congress.api.sunlightfoundation.com',
            apikey=sunlight.config.API_KEY)

        self.assertEqual(url, expected_url)

    def test_legislator(self):
        results = sunlight.congress.legislator(self.bioguide_id)
        self.assertIsNotNone(results)
        page = results._meta.get('page', None)
        self.assertIsNotNone(page)
        if page:
            self.assertEqual(page.get('page', None), 1)
            self.assertEqual(page.get('count', None), 1)
        self.assertIsInstance(results, EntityDict)

    def test_legislator_thomas_id(self):
        results = sunlight.congress.legislator(self.thomas_id, id_type='thomas')
        self.assertIsNotNone(results)
        page = results._meta.get('page', None)
        self.assertIsNotNone(page)
        if page:
            self.assertEqual(page.get('page', None), 1)
            self.assertEqual(page.get('count', None), 1)
        self.assertIsInstance(results, EntityDict)

    def test_legislator_ocd_id(self):
        results = sunlight.congress.legislator(self.ocd_id, id_type='ocd')
        self.assertIsNotNone(results)
        page = results._meta.get('page', None)
        self.assertIsNotNone(page)
        if page:
            self.assertEqual(page.get('page', None), 1)
            self.assertEqual(page.get('count', None), 1)
        self.assertIsInstance(results, EntityDict)

    def test_legislator_bad_bioguideid(self):
        results = sunlight.congress.legislator('foo')
        self.assertIsNone(results)

    def test_legislators(self):
        results = sunlight.congress.legislators()
        page = results._meta.get('page', None)
        self.assertIsNotNone(page)
        if page:
            self.assertEqual(page.get('page', None), 1)
            self.assertEqual(page.get('count', None), 20)
        self.assertNotEqual(len(results), 0)

    def test_all_legislators_in_office(self):
        results = sunlight.congress.all_legislators_in_office()
        page = results._meta.get('page', None)
        self.assertIsNotNone(page)
        if page:
            # In this case, page should be None
            self.assertEqual(page.get('page', 0), None)
            # Should be more then 20, but I don't want to compare to 538, do I?
            self.assertGreater(page.get('count', None), 100)
        self.assertNotEqual(len(results), 0)

    def test_locate_legislators_by_lat_lon(self):
        results = sunlight.congress.locate_legislators_by_lat_lon(self.lat, self.lon)
        count = results._meta.get('count', None)
        # For a state, there should be 2 senators and 1 representative.
        self.assertEqual(len(results), 3)
        self.assertEqual(len(results), count)

    def test_locate_districts_by_zip(self):
        results = sunlight.congress.locate_districts_by_zip(27514)
        count = results._meta.get('count', None)
        # There is a potential for more than 3 legislators to match on a zipcode
        self.assertNotEqual(len(results), 0)
        self.assertEqual(len(results), count)

    def test_search_bills(self):
        results = sunlight.congress.search_bills('Affordable Care Act')
        page = results._meta.get('page', None)
        self.assertIsNotNone(page)
        if page:
            self.assertEqual(page.get('page', None), 1)
            self.assertEqual(page.get('count', None), 20)
        self.assertNotEqual(len(results), 0)

    def test_committees(self):
        results = sunlight.congress.committees()
        page = results._meta.get('page', None)
        self.assertIsNotNone(page)
        if page:
            self.assertEqual(page.get('page', None), 1)
            self.assertEqual(page.get('count', None), 20)
        self.assertNotEqual(len(results), 0)

    def test_amendments(self):
        results = sunlight.congress.amendments()
        page = results._meta.get('page', None)
        self.assertIsNotNone(page)
        if page:
            self.assertEqual(page.get('page', None), 1)
            self.assertEqual(page.get('count', None), 20)
        self.assertNotEqual(len(results), 0)

    def test_votes(self):
        results = sunlight.congress.votes()
        page = results._meta.get('page', None)
        self.assertIsNotNone(page)
        if page:
            self.assertEqual(page.get('page', None), 1)
            self.assertEqual(page.get('count', None), 20)
        self.assertNotEqual(len(results), 0)

    def test_floor_updates(self):
        results = sunlight.congress.floor_updates()
        page = results._meta.get('page', None)
        self.assertIsNotNone(page)
        if page:
            self.assertEqual(page.get('page', None), 1)
            self.assertEqual(page.get('count', None), 20)
        self.assertNotEqual(len(results), 0)

    def test_hearings(self):
        results = sunlight.congress.hearings()
        page = results._meta.get('page', None)
        self.assertIsNotNone(page)
        if page:
            self.assertEqual(page.get('page', None), 1)
            self.assertEqual(page.get('count', None), 20)
        self.assertNotEqual(len(results), 0)

    def test_nominations(self):
        results = sunlight.congress.nominations()
        page = results._meta.get('page', None)
        self.assertIsNotNone(page)
        if page:
            self.assertEqual(page.get('page', None), 1)
            self.assertEqual(page.get('count', None), 20)
        self.assertNotEqual(len(results), 0)


class TestCapitolWords(unittest.TestCase):

    def setUp(self):
        self.phrases_kwargs = {
            'entity_type': 'legislator',
            'entity_value':  'L000551'
        }

    def test__get_url(self):
        url = sunlight.capitolwords._get_url(['phrases'],
                                             sunlight.config.API_KEY,
                                             **self.phrases_kwargs)

        expected_url = '{base_url}/phrases.json?apikey={apikey}&{args}'.format(
            base_url='http://capitolwords.org/api/1',
            apikey=sunlight.config.API_KEY,
            args=sunlight.service.safe_encode(self.phrases_kwargs)).strip('&')

        self.assertEqual(url, expected_url)

    def test_dates(self):
        results = sunlight.capitolwords.dates('Obamacare')
        self.assertNotEqual(len(results), 0)

    def test_phrases_by_entity(self):
        results = sunlight.capitolwords.phrases_by_entity('state',
                                                          phrase='Obamacare')
        self.assertNotEqual(len(results), 0)

    def test_legislator_phrases(self):
        results = sunlight.capitolwords.phrases(
            self.phrases_kwargs['entity_type'],
            self.phrases_kwargs['entity_value'])

        self.assertNotEqual(len(results), 0)

    def test_text(self):
        results = sunlight.capitolwords.text('Christmas')
        self.assertNotEqual(len(results), 0)


if __name__ == '__main__':
    unittest.main()
