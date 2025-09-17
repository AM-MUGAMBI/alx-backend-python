#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('utils.get_json')
    def test_org(self, org_name, mock_get_json):
        expected_payload = {"login": org_name, "repos_url": f"https://api.github.com/orgs/{org_name}/repos"}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)

        # Clear memoize cache for org (attribute name may vary, adjust accordingly)
        if hasattr(client, "_org_cache"):
            delattr(client, "_org_cache")
        # Or if your memoize caches with the method name as attribute:
        if hasattr(client, "org"):
            # Since org is property with memoize, try removing the cached attribute
            # Check what attribute memoize uses to cache (might be _org or similar)
            # Common approach: delete the cached attribute:
            try:
                del client.__dict__["org"]
            except KeyError:
                pass

        # Now access org
        result = client.org

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected_payload)
