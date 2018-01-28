
**HTTP Live Streaming Manifest Parser**
===
This is a simple HLS Manifest Parser written in Python 3.6, no
dependency is required.<br>
It is made for a personal use and provide some extra function as I need.

This parser was made using [RFC 8216](https://tools.ietf.org/html/rfc8216)<br>
This is the final RFC not a draft and some Tags were removed from
previous versions of the protocol HLS but for retro compatibilities
I decided to maintain them.

[TOC]

Tags
====

Supported
---------

- #EXTM3U
- #EXT_X_VERSION
- #EXT_X_MEDIA
- #EXT_X_STREAM_INF
- #EXT_X_TARGETDURATION
- #EXT_X_ALLOW_CACHE
- #EXT_X_MEDIA_SEQUENCE
- #EXT_X_PROGRAM_DATE_TIME
- #EXTINF
- #EXT_X_ENDLIST
- #EXT_X_KEY
- #EXT_X_I_FRAME_STREAM_INF
- #EXT_X_PLAYLIST_TYPE

Not supported
-------------

- #EXT-X-BYTERANGE
- #EXT-X-DISCONTINUITY
- #EXT-X-MAP
- #EXT-X-DATERANGE
- #EXT-X-DISCONTINUITY-SEQUENCE
- #EXT-X-I-FRAMES-ONLY
- #EXT-X-SESSION-DATA
- #EXT-X-SESSION-KEY
- #EXT-X-INDEPENDENT-SEGMENTS
- #EXT-X-START

Documentation
=============

Usage
-----

There are three way to create manifest object :
- From link : `parser = M3U8Parser(link = theLink)`
- From file : `parser = M3U8Parser(file = theFile)`
- From string : `parser = M3U8Parser(string = theString)`

Then you can Parse the manifest : `manifest = parser.parse()`


> Note : This is still under development and some features like multikey
> is not supported yet