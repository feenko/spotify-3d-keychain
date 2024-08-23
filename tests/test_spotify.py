import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest

from helpers.utils import SpotifyLinkParser


class TestSpotifyLinkParser(unittest.TestCase):
    def test_valid_song(self):
        link = "https://open.spotify.com/track/5Q6f5I2abTY6yD9QhvYwwc"
        self.assertEqual(
            SpotifyLinkParser.parse_link(link), ("track", "5Q6f5I2abTY6yD9QhvYwwc")
        )

    def test_valid_song_with_query(self):
        link = "https://open.spotify.com/track/5Q6f5I2abTY6yD9QhvYwwc?si=1"
        self.assertEqual(
            SpotifyLinkParser.parse_link(link), ("track", "5Q6f5I2abTY6yD9QhvYwwc")
        )

    def test_valid_song_with_trailing_slash(self):
        link = "https://open.spotify.com/track/5Q6f5I2abTY6yD9QhvYwwc/"
        self.assertEqual(
            SpotifyLinkParser.parse_link(link), ("track", "5Q6f5I2abTY6yD9QhvYwwc")
        )

    def test_valid_song_extra_parts(self):
        link = "https://open.spotify.com/track/5Q6f5I2abTY6yD9QhvYwwc/extra"
        self.assertEqual(
            SpotifyLinkParser.parse_link(link), ("track", "5Q6f5I2abTY6yD9QhvYwwc")
        )

    def test_valid_album(self):
        link = "https://open.spotify.com/album/3hKJwp7JljeG4AH9RZoSA0"
        self.assertEqual(
            SpotifyLinkParser.parse_link(link), ("album", "3hKJwp7JljeG4AH9RZoSA0")
        )

    def test_valid_artist(self):
        link = "https://open.spotify.com/artist/2aDaFARm4U9hf5DI9Fhbnh"
        self.assertEqual(
            SpotifyLinkParser.parse_link(link), ("artist", "2aDaFARm4U9hf5DI9Fhbnh")
        )

    def test_valid_playlist(self):
        link = "https://open.spotify.com/playlist/37i9dQZF1DZ06evO4vY1Xy"
        self.assertEqual(
            SpotifyLinkParser.parse_link(link), ("playlist", "37i9dQZF1DZ06evO4vY1Xy")
        )

    def test_invalid_link_type(self):
        link = "https://open.spotify.com/invalid/5Q6f5I2abTY6yD9QhvYwwc"
        self.assertIsNone(SpotifyLinkParser.parse_link(link))

    def test_invalid_empty_link(self):
        link = ""
        self.assertIsNone(SpotifyLinkParser.parse_link(link))

    def test_invalid_malformed_link(self):
        link = "not_a_spotify_link"
        self.assertIsNone(SpotifyLinkParser.parse_link(link))

    def test_invalid_link_without_id(self):
        link = "https://open.spotify.com/track/"
        self.assertIsNone(SpotifyLinkParser.parse_link(link))


if __name__ == "__main__":
    unittest.main()
