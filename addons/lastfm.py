import hexchat
import requests

__module_name__ = 'last.fm'
__module_author__ = 'NewellWorldOrder'
__module_version__ = '2.0'
__module_description__ = 'Announces current song playing in Last.FM'

def setUSER(word, word_eol, userdata):
    hexchat.set_pluginpref('user', word[1])
    return hexchat.EAT_ALL
    
def setKEY(word, word_eol, userdata):
    hexchat.set_pluginpref('apikey', word[1])
    return hexchat.EAT_ALL
    
def np(word, word_eol, userdata):
    USER = hexchat.get_pluginpref('user')
    APIKEY = hexchat.get_pluginpref('apikey')
    r=requests.get(r'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=%s&api_key=%s&format=json' % (USER, APIKEY))
    data = r.json()

    nowPlaying = data['recenttracks']['track'][0]['@attr']['nowplaying']
    if nowPlaying == "true":
        songArtist = data['recenttracks']['track'][0]['artist']['#text']
        songName = data['recenttracks']['track'][0]['name']
        songAlbum = data['recenttracks']['track'][0]['album']['#text']
        hexchat.command('me \00306now playing \00311%s \00306by \00313%s \00306from \00309%s' % (songName, songArtist, songAlbum))

    return hexchat.EAT_ALL

hexchat.hook_command('setuser', setUSER)
hexchat.hook_command('setkey', setKEY)
hexchat.hook_command('np', np)
