import sys
import codecs
import re
import common
import time

from m3u8 import Manifest, Segment, Media, StreamInf, IFrameSteamInf, Key, Version, AllowCache, TargetDuration\
    ,PlaylistType, MediaSequence, EndList
from rfc8216 import PlaylistTag, PlaylistMode

class M3U8Parser(object):

    def __init__(self, rManifest):
        self.__rManifest = rManifest
        self.__currentKey = None

    def parseManifest(self):
        self.__manifest = Manifest()
        man = self.__rManifest.splitlines()
        #print(len(man))
        n = len(man)
        i = 0
        while ( i < n):
            try:
                command, statement = man[i].split(':',1)
            except ValueError:
                command = man[i]

            if command == PlaylistTag.EXT_X_VERSION.value:
                self.parseVersion(statement)

            elif command == PlaylistTag.EXT_X_TARGETDURATION.value:
                self.parseTargetDuration(statement)

            elif command == PlaylistTag.EXT_X_ALLOW_CACHE.value:
                self.parseAllowCache(statement)

            elif command == PlaylistTag.EXT_X_PLAYLIST_TYPE.value:
                self.parsePlaylistType(statement)

            elif command == PlaylistTag.EXT_X_MEDIA_SEQUENCE.value:
                self.parseMediaSequence(statement)

            elif command == PlaylistTag.EXT_X_PROGRAM_DATE_TIME:
                pass

            elif command == PlaylistTag.EXT_X_KEY.value:
                self.parseKey(statement)

            elif command == PlaylistTag.EXT_X_MEDIA.value:
                self.parseMedia(statement)

            elif command == PlaylistTag.EXT_X_STREAM_INF.value:
                i += 1
                self.__manifest.setType(PlaylistMode.MASTER)
                self.parseStreamInf(statement, man[i])

            elif command == PlaylistTag.EXT_X_I_FRAME_STREAM_INF.value:
                self.parseIFrameStreamInf(statement)

            elif command == PlaylistTag.EXTINF.value:
                i += 1
                self.parseSegment(statement, man[i])

            elif command == PlaylistTag.EXT_X_ENDLIST.value:
                self.parseEndList()

            i += 1

        #self.__manifest.write("manifest.mnff")
        return self.__manifest

    def parseAttributes(self, statement):
        attributes = {}
        regex = "\"([^\"]+)\""
        matchs = re.findall(regex, statement)
        statement = re.sub(regex, "DUMMY", statement)
        statement = statement.split(',')

        i = 0
        for state in statement:
            param, exec = state.split('=')
            if exec == "DUMMY":
                exec = common.quote(matchs[i])
                i += 1
            attributes[param] = exec

        return attributes

    def parseVersion(self, statement):
        v = Version(statement)
        self.__manifest.setVersion(v)
        self.__manifest.addObject(v)

    def parseTargetDuration(self, statement):
        t = TargetDuration(statement)
        self.__manifest.setTargetDuration(t)
        self.__manifest.addObject(t)

    def parseAllowCache(self, statement):
        a = AllowCache(statement)
        self.__manifest.setAllowCache(a)
        self.__manifest.addObject(a)

    def parsePlaylistType(self, statement):
        p = PlaylistType(statement)
        self.__manifest.setPlaylistType(p)
        self.__manifest.addObject(p)

    def parseMediaSequence(self, statement):
        m = MediaSequence(statement)
        self.__manifest.setMediaSequence(m)
        self.__manifest.addObject(m)

    def parseMedia(self, statement):
        media = self.parseAttributes(statement)
        m = Media(media)
        self.__manifest.addMedia(m)
        self.__manifest.addObject(m)

    def parseStreamInf(self, statement, url):
        streamInf = self.parseAttributes(statement)
        s = StreamInf(streamInf, url)
        self.__manifest.addStreamInf(s)
        self.__manifest.addObject(s)

    def parseIFrameStreamInf(self, statement):
        iFrame = self.parseAttributes(statement)
        ifs = IFrameSteamInf(iFrame)
        self.__manifest.addIFrameStreamInf(ifs)
        self.__manifest.addObject(ifs)

    def parseSegment(self, statement, url):
        duration, title = statement.split(',', 1)
        s = Segment(duration=duration, url=url, title=title, key=self.__currentKey)
        if self.__currentKey != None:
            self.__currentKey.addSegment(s)
        self.__manifest.addSegment(s)
        self.__manifest.addObject(s)

    def parseKey(self, statement):
        key = self.parseAttributes(statement)
        k = Key(key)
        self.__manifest.addKey(k)
        self.__manifest.addObject(k)
        self.__currentKey = k

    def parseEndList(self):
        self.__manifest.addObject(EndList())

start_time = time.time()
a = M3U8Parser(codecs.open(sys.argv[1], 'r', 'utf-8').read())
m = a.parseManifest()
end_read = time.time() - start_time
m.write("test.mnff")
end_write = time.time() - start_time

print("Read = %s" % end_read)
print("Write = %s" % end_write)