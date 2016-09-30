# -*- coding: utf-8 -*-

import os
import tempfile
from backpack import collect
from cachy import CacheManager
from collections import defaultdict

from ..player.library import Library as BaseLibrary
from ..player.album import Album
from ..player.playlist import Playlist
from ..player.artist import Artist
from ..player.track import Track
from ..player.list import List


class Library(BaseLibrary):

    def __init__(self, backend):
        super(Library, self).__init__(backend)

        self._playlists = None
        self._library = None

    @property
    def api(self):
        return self._backend.api

    def get_playlists(self):
        if self._playlists is not None:
            return self._playlists

        playlists_ = self.api.get_all_user_playlist_contents()

        playlists = []
        for playlist_ in playlists_:
            playlist = Playlist(self, playlist_['id'], playlist_['name'])
            for track_ in playlist_['tracks']:
                if track_['source'] == '1':
                    # We need to find our track :-(
                    track_ = self._search_track_in_library(track_['trackId'])

                track = Track(
                    self,
                    track_['id'], track_['title'], track_['artist'], track_['album'],
                    track_['trackNumber'], track_.get('discNumber', 0), metadata=track_
                )

                playlist.add_track(track)

            playlists.append(playlist)

        self._playlists = playlists

        return self._playlists

    def get(self):
        if self._library is not None:
            return self._library

        library = self.cache.remember(
            self.cache_key('library'),
            24 * 60,
            lambda: self.api.get_all_songs()
        )
        self._library = []
        artists_dict = defaultdict(list)
        albums_dict = defaultdict(list)
        artists = []
        albums = []
        for t in library:
            artist = t.get('artist', 'Unknown Artist')
            artists_dict[artist].append(t)

            album = t.get('album', 'Untitled Album')
            albums_dict[album].append(t)

        # With our dictionary of artists we can now loop through and partition in to albums
        for artist_, songs_of_artist in artists_dict.items():
            # Create a new default dict for each album in the same way that the artists were partitioned
            artist = Artist(self, artist_, artist_)
            albums_of_artist_dict = defaultdict(list)
            for i in songs_of_artist:
                album_name = i.get('album', 'Untitled Album')
                albums_of_artist_dict[album_name].append(i)

            for album, tracks_ in albums_of_artist_dict.items():
                album_name = album
                if album == "":
                    album_name = "Untitled Album"

                album = Album(self, album_name, album_name)
                tracks = []
                for track_ in tracks_:
                    tracks.append(
                        Track(self,
                              track_['id'], track_['title'], track_.get('artist', 'Unknwown Artist'), album_name,
                              track_.get('trackNumber', 1), track_.get('discNumber', 1), metadata=track_
                              )
                    )

                for track in collect(tracks).sort(lambda x: (x.disc_number, x.number)):
                    album.add_track(track)

                artist.add_album(album)

            artists.append(artist)

        for album_name, tracks_ in albums_dict.items():
            album = Album(self, album_name, album_name)
            tracks = []
            for track_ in tracks_:
                tracks.append(
                    Track(self,
                          track_['id'], track_['title'], track_.get('artist', 'Unknwown Artist'), album_name,
                          track_.get('trackNumber', 1), track_.get('discNumber', 1), metadata=track_
                          )
                )

            for track in collect(tracks).sort(lambda x: (x.disc_number, x.number)):
                album.add_track(track)

            albums.append(album)

        self._library = {
            'artists': collect(artists).sort(lambda a: a.name),
            'albums': collect(albums).sort(lambda a: a.name),
            '_default': library
        }

        return self._library

    def _search_track_in_library(self, track_id):
        for track in self.get()['_default']:
            if track['id'] == track_id:
                return track

    def get_url(self, track):
        return self.api.get_stream_url(track.id)

    def search(self, query):
        results = self.api.search(query)

        artists = []
        albums = []
        playlists = []

        # Albums
        for alb in results['albums_hits']:
            for in_lib_alb in self.get()['albums']:
                if in_lib_alb.id == alb['albumId']:
                    albums.append(in_lib_alb)

        # Artists
        for art in results['artists_hits']:
            for in_lib_art in self.get()['artists']:
                if in_lib_art.id == art['albumId']:
                    artists.append(in_lib_art)

        # Playlists
        for play in results['playlists_hits']:
            for in_lib_playlist in self.get_playlists():
                if in_lib_playlist.id == play['playlistId']:
                    playlists.append(in_lib_playlist)

        return List(
            'Search results for [{}]'.format(query),
            [List('Artists', artists),
             List('Albums', albums),
             List('Playlists', playlists)]
        )

    def __getitem__(self, item):
        return self._library[item]
