#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('utils.get_json')
    def test_org(self, org_name, mock_get_json):
        expected_payload = {
            "login": org_name,
            "repos_url": f"https://api.github.com/orgs/{org_name}/repos"
        }
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)

        # Clear memoize cache for org
        if hasattr(client, "_org_cache"):
            delattr(client, "_org_cache")
        if hasattr(client, "org"):
            try:
                del client.__dict__["org"]
            except KeyError:
                pass

        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self):
        mocked_payload = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }
        client = GithubOrgClient("google")

        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = mocked_payload
            repos_url = client._public_repos_url
            self.assertEqual(repos_url, mocked_payload["repos_url"])

    @patch('utils.get_json')
    def test_public_repos(self, mock_get_json):
        mocked_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": {"key": "bsd"}},
        ]
        mock_get_json.return_value = mocked_repos_payload

        client = GithubOrgClient("google")

        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_repos_url:
            mock_repos_url.return_value = (
                "https://api.github.com/orgs/google/repos"
            )

            repos = client.public_repos()
            expected_repos = ["repo1", "repo2", "repo3"]
            self.assertEqual(repos, expected_repos)

            mock_repos_url.assert_called_once()

        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/google/repos"
        )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license returns correct boolean"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)

    def test_has_license_none_key(self):
        """Test GithubOrgClient.has_license raises if license_key is None"""
        repo = {"license": {"key": "some_key"}}
        with self.assertRaises(AssertionError):
            GithubOrgClient.has_license(repo, None)
