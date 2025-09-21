#!/usr/bin/env python3
"""Unit and integration tests for client.py
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized_class
from fixtures import TEST_PAYLOAD
from client import GithubOrgClient


@parameterized_class(('org_payload', 'repos_payload',
                      'expected_repos', 'apache2_repos'),
                     TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient with fixtures"""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get"""
        patcher = patch('client.requests.get')
        cls.mock_get = patcher.start()
        cls.addClassCleanup(patcher.stop)

    def test_public_repos(self):
        """Test that public_repos returns expected repo names"""
        self.mock_get.return_value.json.side_effect = [
            self.org_payload, self.repos_payload
        ]
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_has_license(self):
        """Test that has_license works as expected"""
        client = GithubOrgClient("google")
        self.assertTrue(client.has_license(
            {"license": {"key": "apache-2.0"}}, "apache-2.0"))
        self.assertFalse(client.has_license(
            {"license": {"key": "other"}}, "apache-2.0"))


if __name__ == "__main__":
    unittest.main()
