# -*- coding: utf-8 -*-

from enum import Enum

"""This class enumerate all the tags present in the RFC 8216 (describe the version 6 of the HLS protocol)
RFC 8216 : https://tools.ietf.org/html/rfc8216
I left some tags that are in previous versions of the protocol"""


"""Curtom tags"""
class PlaylistMode(Enum):
    MASTER = 0
    MEDIA = 1

class MediaAttributes(Enum):
    TYPE = "TYPE"
    URI = "URI"
    GROUP_ID = "GROUP-ID"
    LANGUAGE = "LANGUAGE"
    ASSOC_LANGUAGE = "ASSOC-LANGUAGE"
    NAME = "NAME"
    DEFAULT = "DEFAULT"
    AUTOSELECT = "AUTOSELECT"
    FORCED = "FORCED"
    INSTREAM_ID = "INSTREAM-ID"
    CHARACTERISTICS = "CHARACTERISTICS"
    CHANNELS = "CHANNELS"

class StreamInfAttributes(Enum):
    BANDWIDTH = "BANDWIDTH"
    AVERAGE_BANDWIDTH = "AVERAGE-BANDWIDTH"
    CODECS = "CODECS"
    RESOLUTION = "RESOLUTION"
    FRAME_RATE = "FRAME-RATE"
    HDCP_LEVEL = "HDCP-LEVEL"
    AUDIO = "AUDIO"
    VIDEO = "VIDEO"
    SUBTITLES = "SUBTITLES"
    CLOSED_CAPTIONS = "CLOSED-CAPTIONS"
    PROGRAM_ID = "PROGRAM-ID"

class IFrameStreamInfAttributes(Enum):
    BANDWIDTH = "BANDWIDTH"
    AVERAGE_BANDWIDTH = "AVERAGE-BANDWIDTH"
    CODECS = "CODECS"
    RESOLUTION = "RESOLUTION"
    HDCP_LEVEL = "HDCP-LEVEL"
    VIDEO = "VIDEO"
    PROGRAM_ID = "PROGRAM-ID"
    URL = "URL"

class KeyAttributes(Enum):
    METHOD = "METHOD"
    URI = "URI"
    IV = "IV"
    KEYFORMAT = "KEYFORMAT"
    KEYFORMATVERSIONS = "KEYFORMATVERSIONS"

class PlaylistTag(Enum):
    EXTM3U = "#EXTM3U"
    EXT_X_VERSION = "#EXT-X-VERSION"
    EXT_X_MEDIA = "#EXT-X-MEDIA"
    EXT_X_STREAM_INF = "#EXT-X-STREAM-INF"
    EXT_X_TARGETDURATION = "#EXT-X-TARGETDURATION"
    EXT_X_ALLOW_CACHE = "#EXT-X-ALLOW-CACHE"
    EXT_X_MEDIA_SEQUENCE = "#EXT-X-MEDIA-SEQUENCE"
    EXT_X_PROGRAM_DATE_TIME = "#EXT-X-PROGRAM-DATE-TIME"
    EXTINF = "#EXTINF"
    EXT_X_ENDLIST = "#EXT-X-ENDLIST"
    EXT_X_KEY = "#EXT-X-KEY"
    EXT_X_I_FRAME_STREAM_INF = "#EXT-X-I-FRAME-STREAM-INF"
    EXT_X_PLAYLIST_TYPE = "#EXT-X-PLAYLIST-TYPE"