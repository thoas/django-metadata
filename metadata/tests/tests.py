from django.test import TestCase
from django.utils import timezone as datetime

from exam import fixture, before, Exam

from metadata.connection import client

from .models import Poll


class MetadataTest(Exam, TestCase):
    @before
    def flush_database(self):
        client.flushdb()

    @fixture
    def poll(self):
        return Poll.objects.create(question='What\'s your favorite color', pub_date=datetime.now())

    def test_basic_storing(self):
        self.poll.metadata['key'] = 'value'

        poll = self.poll.refresh()

        assert poll.metadata['key'] == 'value'

        self.poll.metadata = {
            'key': 'valeur'
        }

        poll = self.poll.refresh()

        assert poll.metadata['key'] == 'valeur'

    def test_get_or_set(self):
        assert self.poll.metadata.get_or_set('key', lambda: 'value') == 'value'

        assert self.poll.metadata['key'] == 'value'

        assert self.poll.metadata.get_or_set('key', lambda: 'test') == 'value'

    def test_delete_key(self):
        self.poll.metadata['key'] = 'value'

        self.poll.metadata['key'] = None

        poll = self.poll.refresh()

        self.assertNotIn('key', poll.metadata)

        poll.metadata['key'] = 'value'

        poll = self.poll.refresh()

        self.assertIn('key', poll.metadata)

        poll.metadata = {
            'key': None
        }

        poll = self.poll.refresh()

        self.assertNotIn('key', poll.metadata)

        with self.assertRaises(KeyError):
            poll.metadata['key']

        assert poll.metadata.get('key', None) is None

        poll.metadata = {
            'key': None
        }

        del poll.metadata['key']

        with self.assertRaises(KeyError):
            poll.metadata['key']

        assert poll.metadata.get('key', None) is None

    def test_wildcard_delete(self):
        self.poll.metadata['key_1'] = 'value'
        self.poll.metadata['key_2'] = 'value'
        self.poll.metadata['key_3'] = 'value'
        self.poll.metadata['diff_key_3'] = 'value'

        del self.poll.metadata['key_*']

        poll = self.poll.refresh()

        values = poll.metadata.keys()

        assert values == ['diff_key_3']

        self.poll.metadata['key_3'] = 'value'

        poll = self.poll.refresh()

        values = poll.metadata.keys()

        assert sorted(values) == sorted(['diff_key_3', 'key_3'])

        del self.poll.metadata['*key*']

        poll = self.poll.refresh()

        values = poll.metadata.keys()

        assert len(values) == 0

    def test_iteration(self):
        keys = {
            'key1': 'value',
            'key2': 'value',
        }

        self.poll.metadata = keys

        poll = self.poll.refresh()

        for k, v in poll.metadata.items():
            assert keys[k] == v

    def test_incr(self):
        self.poll.metadata.incr('key', 2)

        poll = self.poll.refresh()

        assert int(poll.metadata['key']) == 2

    def test_values(self):
        keys = {
            'key1': 'value1',
            'key2': 'value2',
        }

        self.poll.metadata = keys

        poll = self.poll.refresh()

        self.assertIn('value2', poll.metadata.values())
        self.assertIn('value1', poll.metadata.values())

    def test_keys(self):
        keys = {
            'key1': 'value1',
            'key2': 'value2',
        }

        self.poll.metadata = keys

        poll = self.poll.refresh()

        self.assertIn('key2', poll.metadata.keys())
        self.assertIn('key1', poll.metadata.keys())
