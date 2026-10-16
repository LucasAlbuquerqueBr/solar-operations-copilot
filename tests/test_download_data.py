"""Integrity and failed-download behavior; no network or large dataset required."""
import hashlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from tools.download_data import download_file, verify_file


class SourceIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / 'source.csv'
        self.payload = b'timestamp,power\n2021-01-01,12\n'
        self.item = {'bytes': len(self.payload), 'sha256': hashlib.sha256(self.payload).hexdigest(), 'url': 'https://example.invalid/data'}

    def test_missing_and_corrupt_files_fail(self):
        self.assertFalse(verify_file(self.path, self.item))
        self.path.write_bytes(b'x' * len(self.payload))
        self.assertFalse(verify_file(self.path, self.item))

    def test_valid_file_skips_network(self):
        self.path.write_bytes(self.payload)
        with patch('tools.download_data.urlopen') as fetch:
            download_file(self.path, self.item)
            fetch.assert_not_called()

    def test_valid_download_is_installed(self):
        with patch('tools.download_data.urlopen', return_value=io.BytesIO(self.payload)):
            download_file(self.path, self.item)
        self.assertTrue(verify_file(self.path, self.item))
        self.assertFalse(self.path.with_suffix('.csv.part').exists())

    def test_bad_download_preserves_existing_file(self):
        self.path.write_bytes(b'previous content')
        with patch('tools.download_data.urlopen', return_value=io.BytesIO(b'bad')):
            with self.assertRaises(ValueError):
                download_file(self.path, self.item)
        self.assertEqual(self.path.read_bytes(), b'previous content')
        self.assertFalse(self.path.with_suffix('.csv.part').exists())


if __name__ == '__main__':
    unittest.main()
