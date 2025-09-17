#!/usr/bin/env python3
"""Unit tests for utils.access_nested_map and utils.get_json
"""
#!/usr/bin/env python3
"""Unit tests for utils.access_nested_map and utils.get_json
"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock

from utils import access_nested_map, get_json


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b'),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), repr(expected_key))


class TestGetJson(unittest.TestCase):
    """Tests for get_json."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        # Create a mock response object with a .json() method
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        # Patch requests.get in the utils module to return the mock response
        with patch('utils.requests.get', return_value=mock_response) as mock_get:
            result = get_json(test_url)

            # Check if requests.get was called once with the correct URL
            mock_get.assert_called_once_with(test_url)

            # Check if get_json returned the correct payload
            self.assertEqual(result, test_payload)

