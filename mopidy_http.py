#!/usr/bin/env python

"""Helper to send http POST requests to mopidy."""

from __future__ import print_function
import requests


URI_PATTERN = 'http://{server}:{port}/mopidy/rpc'
JSON_RPC = '2.0'
ID = '1'


class HttpMopidyException(Exception):
    """Error raised if post request worked by mopidy did not like it."""

    def __init__(self, error_params):
        """Create with content of field `error` of request response object"""
        super(HttpMopidyException, self).__init__(str(error_params))


class HttpMopidy(object):
    """see module doc."""

    def __init__(self, server='localhost', port=6680, debug=False):
        """Create instance."""
        self.server = server
        self.port = port
        self.debug = debug

    def _post_request(self, method, **params):
        """
        Send post request with given method and params.

        Internal helper for all other methods.

        Will raise exception if request failed.
        Will return result as `dict` if request succeeded.
        """
        data = dict(jsonrpc=JSON_RPC, id=ID, method=method, params=params)
        result = requests.post(URI_PATTERN.format(server=self.server,
                                                  port=self.port),
                               json=data)
        if not result.ok:
            result.raise_for_status()
        if self.debug:
            print('debug ch: {}'.format(result.json()))
        result = result.json()
        if 'error' in result:
            raise HttpMopidyException(result['error'])
        return result['result']

    def get_volume(self):
        """Get output volume (range [0..100])."""
        result = self._post_request('core.mixer.get_volume')
        return int(result)

    def set_volume(self, new_volume):
        """Set output volume (range [0..100])."""
        self._post_request('core.mixer.set_volume', volume=new_volume)

    def get_current_track(self):
        """Get mopidy uri for track that is currently playing/paused."""
        result = self._post_request('core.playback.get_current_track')
        return result['uri']

    def get_playlists(self):
        """
        Get list of references to available playlist.

        These are mopidy playlists, not spotify playlists!
        """
        result = self._post_request('core.playlists.as_list')
        return result

    def play(self):
        """Start playing currently active track on tracklist."""
        self._post_request('core.playback.play')

    def stop(self):
        """Stop playing."""
        self._post_request('core.playback.stop')

    def clear_tracklist(self):
        """Create new list of tracks to play."""
        self._post_request('core.tracklist.clear')

    def add_to_tracklist(self, uri):
        """Add track with given uri to tracklist."""
        self._post_request('core.tracklist.add', uri=uri)

    def play_single_track(self, uri):
        """Clears tracklist, adds given track, starts playing."""
        self.clear_tracklist()
        self.add_to_tracklist(uri)
        self.play()
