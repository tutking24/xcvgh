
from tests import IGittTestCase
from IGitt.Utils import Cache
from IGitt.Utils import LimitedSizeDict


class CacheTestCase(IGittTestCase):

    def test_LimitedSizeDict(self):
        store = LimitedSizeDict(size_limit=10)
        for i in range(100):
            store[i] = i + 1

        # assert that even after inserting large data, the dict only retains
        # latest 10 entries
        self.assertEqual(len(store), 10)

    def test_cache_validation_entityTag(self):
        with self.assertRaises(TypeError):
            Cache.validate({'entityTag': 10})

    def test_cache_validation_links(self):
        with self.assertRaises(TypeError):
            Cache.validate({'links': 10})

    def test_cache_validation_lastFetched(self):
        with self.assertRaises(ValueError):
            Cache.validate({'lastFetched': 'Tue, 10 March 2021'})

        with self.assertRaises(TypeError):
            Cache.validate({'lastFetched': None})

    def test_cache_validation_fromWebhook(self):
        with self.assertRaises(TypeError):
            Cache.validate({'fromWebhook': None})
