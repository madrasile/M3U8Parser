from rfc8216 import MediaAttributes, StreamInfAttributes, IFrameStreamInfAttributes, PlaylistMode, KeyAttributes
from exception import NotMasterPlaylistException, NoQualityResolutionException, SegmentNotEncrypted
import codecs
import common

def PlayListMaster(f):
    def wrapper(*args):
        if args[0].getType() == PlaylistType.MASTER:
            return f(*args)
        else:
            raise NotMasterPlaylistException
    return wrapper

class Manifest(object):

    def __init__(self):
        self.__media = []
        self.__streamInf = []
        self.__ifs = []
        self.__keys = []
        self.__segments = []
        self.__object = []
        self.__type = None
        self.__version = None
        self.__targetDuration = None
        self.__allowCache = None
        self.__playlistType = None
        self.__mediaSequence = None
        self.__bestStreamQuality = None

    def setVersion(self, version):
        self.__version = version

    def getVersion(self):
        return self.__version.getVersion()

    def setTargetDuration(self, targetDuration):
        self.__targetDuration = targetDuration

    def getTargetDuration(self):
        return self.__targetDuration.getTargetDuration()

    def setAllowCache(self, allowCache):
        self.__allowCache = allowCache

    def getAllowCache(self):
        return self.__allowCache.getAllowCache()

    def getAllowCacheBoolean(self):
        return self.__allowCache.getAllowCacheBoolean()

    def setPlaylistType(self, playlistType):
        self.__playlistType = playlistType

    def getPlaylistType(self):
        return self.__playlistType.getPlaylistType()

    def setMediaSequence(self, mediaSequence):
        self.__mediaSequence = mediaSequence

    def getMediaSequence(self):
        return self.__mediaSequence

    def addObject(self, obj):
        self.__object.append(obj)

    def getObjects(self, ind):
        return self.__object[ind]

    def addMedia(self, media):
        self.__media.append(media)

    def getMedias(self):
        return self.__media

    def addStreamInf(self, stream):
        self.__streamInf.append(stream)

    def getStreamInfs(self):
        return self.__streamInf

    def addIFrameStreamInf(self, ifs):
        self.__ifs.append(ifs)

    def getIFrameStreamInfs(self):
        return self.__ifs

    def addKey(self, key):
        self.__keys.append(key)

    def getKeys(self):
        return self.__keys

    def addSegment(self, segment):
        self.__segments.append(segment)

    def getSegments(self):
        return self.__segments

    def getBestStreamQuality(self):
        resolution = ()
        for stream in self.__streamInf:
            try:
                if stream.getResolutionTuple() > resolution:
                    self.__bestStreamQuality = stream
            except NoQualityResolutionException:
                pass
        return self.__bestStreamQuality

    def forceBestStreamQuality(self):
        if self.__bestStreamQuality == None:
            self.getBestStreamQuality()
        for stream in self.__streamInf:
            try:
                stream.getResolutionTuple()
                stream.setUrl(self.__bestStreamQuality.getUrl())
            except NoQualityResolutionException:
                pass

    def inspectMedias(self):
        i = 0
        for media in self.__media:
            media.inspect(i)
            i += 1

    def inspectStreamInfs(self):
        i = 0
        for streams in self.__streamInf:
            streams.inspect(i)
            i += 1

    def inspectStream(self):
        i = 0
        for ifs in self.__ifs:
            ifs.inspect(i)
            i += 1

    def setType(self, type):
        self.__type = type

    def getType(self):
        return self.__type

    # def toString(self):
    #     id = 0
    #     s = "Manifest type is %s\n" % self.__type.value
    #     s += "Media are :\n"
    #     for media in self.__media:
    #         s += "\tInternal ID = %s" % id
    #         s += "\t%s\n"
    #         id+=1

    def __str__(self):
        s = "#EXTM3U"
        for object in self.__object:
            #print(str(object))
            s += "\n%s" % str(object)
        return s

    def write(self, path):
        file = codecs.open(path, "w", "utf-8")
        file.write(self.__str__())
        file.close()

class Tag(object):

    def __init__(self, attributes, tagAttributes):
        self.attributes = attributes
        for param in [x.value for x in tagAttributes]:
            if param not in attributes.keys():
                self.attributes[param] = None

"EXT-X-MEDIA Class"
class Media(Tag):

    # KeyError Exception
    def __init__(self, mediaDict, **kwargs):
        super().__init__(mediaDict, MediaAttributes)

    def __str__(self):
        s = "#EXT-X-MEDIA:"
        for key in self.attributes.keys():
            if self.attributes[key] != None:
                s += "%s=%s," % (key, self.attributes[key])
        return s[:-1]

    def inspect(self, *args):
        if len(args) == 1:
            print("\nX-MEDIA %s - Attributes" % args[0])
        else:
            print("\nX-MEDIA - Attributes")
        for key in self.attributes.keys():
            print("\t%s = %s" % (key, str(self.attributes[key])))

    def getType(self):
        return self.attributes[MediaAttributes.TYPE.value]

    def setType(self, type):
        self.attributes[MediaAttributes.TYPE.value] = type

    def getUri(self):
        return self.attributes[MediaAttributes.URI.value]

    def setUri(self, uri):
        self.attributes[MediaAttributes.URI.value] = common.quote(uri)

    def getGroupId(self):
        return self.attributes[MediaAttributes.GROUP_ID.value]

    def setGroupId(self, groupId):
        self.attributes[MediaAttributes.GROUP_ID.value] = common.quote(groupId)

    def getLanguage(self):
        return self.attributes[MediaAttributes.LANGUAGE.value]

    def setLanguage(self, language):
        self.attributes[MediaAttributes.LANGUAGE.value] = common.quote(language)

    def getAssocLanguage(self):
        return self.attributes[MediaAttributes.ASSOC_LANGUAGE.value]

    def setAssocLanguage(self, assocLanguage):
        self.attributes[MediaAttributes.ASSOC_LANGUAGE.value] = common.quote(assocLanguage)

    def getName(self):
        return self.attributes[MediaAttributes.NAME.value]

    def setName(self, name):
        self.attributes[MediaAttributes.NAME.value] = common.quote(name)

    def isDefault(self):
        return True if self.attributes[MediaAttributes.AUTOSELECT.value] == "YES" else False

    def setDefault(self, bool):
        if bool == True:
            self.attributes[MediaAttributes.DEFAULT.value] = "YES"
        else:
            self.attributes[MediaAttributes.DEFAULT.value] = "NO"

    def isAutoSelect(self):
        return True if self.attributes[MediaAttributes.AUTOSELECT.value] == "YES" else False

    def setAutoSelect(self, bool):
        if bool == True:
            self.attributes[MediaAttributes.AUTOSELECT.value] = "YES"
        else:
            self.attributes[MediaAttributes.AUTOSELECT.value] = "NO"

    def isForced(self):
        return True if self.attributes[MediaAttributes.FORCED.value] == "YES" else False

    def setForced(self, bool):
        if bool == True:
            self.attributes[MediaAttributes.FORCED.value] = "YES"
        else:
            self.attributes[MediaAttributes.FORCED.value] = "NO"

    def getInStreamId(self):
        return self.attributes[MediaAttributes.INSTREAM_ID.value]

    def setInSteamId(self, id):
        self.attributes[MediaAttributes.INSTREAM_ID.value] = common.quote(id)

    def getCharacteristics(self):
        return self.attributes[MediaAttributes.CHARACTERISTICS.value]

    def setCharacteristics(self, characteristics):
        self.attributes[MediaAttributes.CHARACTERISTICS.value] = common.quote(characteristics)

    def getChannels(self):
        return self.attributes[MediaAttributes.CHANNELS.value]

    def setChannels(self, channels):
        self.attributes[MediaAttributes.CHANNELS.value] = common.quote(channels)

"EXT-X-STREAM-INF Class"
class StreamInf(Tag):

    def __init__(self, streamInfDict, url):
        super().__init__(streamInfDict, StreamInfAttributes)
        self.url = url

    def __str__(self):
        s = "#EXT-X-STREAM-INF:"
        for key in self.attributes.keys():
            if self.attributes[key] != None:
                s += "%s=%s," % (key, self.attributes[key])
        return "%s\n%s" % (s[:-1], self.url)

    def inspect(self, *args):
        if len(args) == 1:
            print("\nX-STREAM-INF %s - Attributes" % args[0])
        else:
            print("\nX-STREAM-INF - Attributes")
        for key in self.attributes.keys():
            print("\t%s = %s" % (key, str(self.attributes[key])))
        print("\tURL = %s" % self.url)

    def getUrl(self):
        return self.url

    def setUrl(self, url):
        self.url = url

    def getBandwith(self):
        return self.attributes[StreamInfAttributes.BANDWIDTH.value]

    def setBandwitch(self, bandwidth):
        self.attributes[StreamInfAttributes.BANDWIDTH.value] = bandwidth

    def getAverageBandwidth(self):
        return self.attributes[StreamInfAttributes.AVERAGE_BANDWIDTH.value]

    def setAverageBandwidth(self, averageBandwidth):
        self.attributes[StreamInfAttributes.AVERAGE_BANDWIDTH.value] = averageBandwidth

    def getCodecs(self):
        return self.attributes[StreamInfAttributes.CODECS.value]

    def setCodecs(self, codecs):
        self.attributes[StreamInfAttributes.CODECS.value] = common.quote(codecs)

    def getResolution(self):
        if self.attributes[StreamInfAttributes.RESOLUTION.value] == None:
            raise NoQualityResolutionException
        return self.attributes[StreamInfAttributes.RESOLUTION.value]

    def getResolutionTuple(self):
        if self.attributes[StreamInfAttributes.RESOLUTION.value] == None:
            raise NoQualityResolutionException
        width, height = self.attributes[StreamInfAttributes.RESOLUTION.value].split('x')
        return width, height

    def setResolution(self, width, height):
        self.attributes[StreamInfAttributes.RESOLUTION.value] = \
        "%sx%s" % (width, height)

    def getFrameRate(self):
        return self.attributes[StreamInfAttributes.FRAME_RATE.value]

    def setFrameRate(self, frameRate):
        self.attributes[StreamInfAttributes.FRAME_RATE.value] = frameRate

    def getHDCPLevel(self):
        return self.attributes[StreamInfAttributes.HDCP_LEVEL.value]

    def setHDCPLevel(self, HDCPLevel):
        self.attributes[StreamInfAttributes.HDCP_LEVEL.value] = HDCPLevel

    def getAudio(self):
        return self.attributes[StreamInfAttributes.AUDIO.value]

    def setAudio(self, audio):
        self.attributes[StreamInfAttributes.AUDIO.value] = common.quote(audio)

    def getVideo(self):
        return self.attributes[StreamInfAttributes.VIDEO.value]

    def setVideo(self, video):
        self.attributes[StreamInfAttributes.VIDEO.value] = common.quote(video)

    def getSubtitles(self):
        return self.attributes[StreamInfAttributes.SUBTITLES.value]

    def setSubtitles(self, subtitles):
        self.attributes[StreamInfAttributes.SUBTITLES.value] = common.quote(subtitles)

"EXT-X-I-FRAME-STREAM-INF Class"
class IFrameSteamInf(Tag):
    def __init__(self, iframeStreamDict):
        super().__init__(iframeStreamDict, IFrameStreamInfAttributes)

    def __str__(self):
        s = "#EXT-X-I-FRAME-STREAM-INF:"
        for key in self.attributes.keys():
            if self.attributes[key] != None:
                s += "%s=%s," % (key, self.attributes[key])
        return s[:-1]

    def inspect(self, number):
        print("\nX-I-FRAME-STREAM-INF %s - Attributes" % number)
        for key in self.attributes.keys():
            print("\t%s = %s" % (key, str(self.attributes[key])))

    def getBandwith(self):
        return self.attributes[IFrameStreamInfAttributes.BANDWIDTH.value]

    def setBandwitch(self, bandwidth):
        self.attributes[IFrameStreamInfAttributes.BANDWIDTH.value] = bandwidth

    def getAverageBandwidth(self):
        return self.attributes[IFrameStreamInfAttributes.AVERAGE_BANDWIDTH.value]

    def setAverageBandwidth(self, averageBandwidth):
        self.attributes[IFrameStreamInfAttributes.AVERAGE_BANDWIDTH.value] = averageBandwidth

    def getCodecs(self):
        return self.attributes[IFrameStreamInfAttributes.CODECS.value]

    def setCodecs(self, codecs):
        self.attributes[IFrameStreamInfAttributes.CODECS.value] = common.quote(codecs)

    def getResolution(self):
        return self.attributes[IFrameStreamInfAttributes.RESOLUTION.value]

    def getResolutionTuple(self):
        width, height = self.attributes[IFrameStreamInfAttributes.RESOLUTION.value].split('x')
        return width, height

    def setResolution(self, width, height):
        self.attributes[IFrameStreamInfAttributes.RESOLUTION.value] = \
            "%sx%s" % (width, height)

    def getHDCPLevel(self):
        return self.attributes[IFrameStreamInfAttributes.HDCP_LEVEL.value]

    def setHDCPLevel(self, HDCPLevel):
        self.attributes[IFrameStreamInfAttributes.HDCP_LEVEL.value] = HDCPLevel

    def getVideo(self):
        return self.attributes[IFrameStreamInfAttributes.VIDEO.value]

    def setVideo(self, video):
        self.attributes[IFrameStreamInfAttributes.VIDEO.value] = common.quote(video)

"EXTINF Class"
class Segment(object):

    def __init__(self, duration, title, url, key):
        self.__duration = duration
        self.__title = title
        self.__url = url
        self.__key = key

    def __str__(self):
        s = "#EXTINF:%s,%s\n%s" % (self.__duration, self.__title, self.__url)
        return s

    def getDuration(self):
        return self.__duration

    def setDuration(self, duration):
        self.__duration = duration

    def getUrl(self):
        return self.__url

    def setUrl(self, url):
        self.__url = url

    def getTitle(self):
        return self.__title

    def setTitle(self, title):
        self.__title = title

    def isEncrypted(self):
        if self.__key != None:
            return True
        else:
            return False

    def getKey(self):
        if self.isEncrypted() != False:
            return self.__key
        else:
            raise SegmentNotEncrypted

"EXT-X-ENDLIST Class"
class EndList(object):

    def __init__(self):
        pass

    def __str__(self):
        s = "#EXT-X-ENDLIST"
        return s

"EXT_X_KEY Class"
class Key(Tag):

    def __init__(self, keyDict):
        super().__init__(keyDict, KeyAttributes)
        self.__segments = []

    def __str__(self):
        s = "#EXT-X-KEY:"
        for key in self.attributes.keys():
            if self.attributes[key] != None:
                s += "%s=%s," % (key, self.attributes[key])
        return s[:-1]

    def getMethod(self):
        return self.attributes[KeyAttributes.METHOD.value]

    def setMethod(self, method):
        self.attributes[KeyAttributes.METHOD.value] = method

    def getUrl(self):
        return self.attributes[KeyAttributes.URI.value]

    def setUrl(self, url):
        self.attributes[KeyAttributes.URI.value] = url

    def getIV(self):
        return self.attributes[KeyAttributes.IV.value]

    def setIV(self, iv):
        self.attributes[KeyAttributes.IV.value] = iv

    def addSegment(self, segment):
        self.__segments.append(segment)

    def getSegments(self):
        return self.__segments

"EXT-X-VERSION Class"
class Version(object):

    def __init__(self, version):
        self.__version = version

    def __str__(self):
        s = "#EXT-X-VERSION:%s" % self.__version
        return s

    def setVersion(self, version):
        self.__version = version

    def getVersion(self):
        return self.__version

"EXT-X-TARGETDURATION Class"
class TargetDuration(object):

    def __init__(self, targetDuration):
        self.__targetDuration = targetDuration

    def __str__(self):
        s = "#EXT-X-TARGETDURATION:%s" % self.__targetDuration
        return s

    def setTargetDuaration(self, targetDuration):
        self.__targetDuration = targetDuration

    def getTargetDuration(self):
        return self.__targetDuration

"EXT-X-ALLOW-CACHE Class"
class AllowCache(object):

    def __init__(self, allowCache):
        self.__allowCache = allowCache

    def __str__(self):
        s = "#EXT-X-ALLOW-CACHE:%s" % self.__allowCache
        return s

    def setAllowCache(self, boolean):
        if boolean == True:
            self.__allowCache = "YES"
        else:
            self.__allowCache = "NO"

    def getAllowCache(self):
        return self.__allowCache

    def getAllowCacheBoolean(self):
        if self.__allowCache == "YES":
            return True
        elif self.__allowCache == "NO":
            return False
        else:
            return None

"EXT-X-PLAYLIST-TYPE Class"
class PlaylistType(object):

    def __init__(self, type):
        self.__type = type

    def __str__(self):
        s = "#EXT-X-PLAYLIST-TYPE:%s" % self.__type
        return s

    def setType(self, type):
        self.__type = type

    def getType(self):
        return self.__type

"EXT-X-MEDIA-SEQUENCE Class"
class MediaSequence(object):

    def __init__(self, mediaSequence):
        self.__mediaSequence = mediaSequence

    def __str__(self):
        s = "#EXT-X-MEDIA-SEQUENCE:%s" % self.__mediaSequence
        return s

    def setMediaSequence(self, mediaSequence):
        self.__mediaSequence = mediaSequence

    def getMediaSequence(self):
        return self.__mediaSequence