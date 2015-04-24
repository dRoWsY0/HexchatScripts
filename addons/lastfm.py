import hexchat

try:
    import requests
except:
    print('lastfm.py requres the requests python library. Link: http://docs.python-requests.org/en/latest/')

__module_name__ = 'last.fm'
__module_author__ = 'NewellWorldOrder'
__module_version__ = '2.0'
__module_description__ = 'Announces current song playing in Last.FM'

def lfmHelp(word, word_eol, userdata):
    print('Last.FM by NewellWorldOrder: /np displays the song you are listening to. Use /help lastfmuser and /help lastfmapi for configuration information.')
    return hexchat.EAT_ALL

def setUSER(word, word_eol, userdata):
    if word[1].lower() == 'set':
        hexchat.set_pluginpref('lfmnwo_user', word[2])
        print('Username set to "%s"' % word[2])
    if word[1].lower() == 'reset':
        print('Username reset (old username=%s)' % hexchat.get_pluginpref('lfmnwo_user'))
        hexchat.del_pluginpref('lfmnwo_user')
    return hexchat.EAT_ALL
    
def setKEY(word, word_eol, userdata):
    if word[1].lower() == 'set':
        hexchat.set_pluginpref('lfmnwo_apikey', word[2])
        print('API key set to "%s"' % word[2])
    if word[1].lower() == 'reset':
        print('API key reset (old API key=%s)' % hexchat.get_pluginpref('lfmnwo_apikey'))
        hexchat.del_pluginpref('lfmnwo_apikey') 
    return hexchat.EAT_ALL

def np(word, word_eol, userdata):
    USER = hexchat.get_pluginpref('lfmnwo_user')
    APIKEY = hexchat.get_pluginpref('lfmnwo_apikey')
    if USER and APIKEY:
        try:
            r=requests.get(r'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=%s&api_key=%s&format=json' % (USER, APIKEY))
            data = r.json()
            try:
                nowplaying = data['recenttracks']['track'][0]['@attr']['nowplaying']
                songName = data['recenttracks']['track'][0]['name']
                songArtist = data['recenttracks']['track'][0]['artist']['#text']
                songAlbum = data['recenttracks']['track'][0]['album']['#text']
                if songAlbum:
                     songAlbum = ('\00306from \00309%s' % songAlbum)
                hexchat.command('me \00306now playing \00311%s \00306by \00313%s %s' % (songName, songArtist, songAlbum))
            except:
                print('Last.FM: No song playing')
        except:
            print('Error: Cannot connect to Last.fm')
    if not USER:
        print('Use /lastfmuser set <last.fm username> to set a username for the plugin to fetch song data from')
    if not APIKEY:
        print('Use /lastfmapi set <last.fm API key> to set a API key for the plugin to fetch song data from')
    return hexchat.EAT_ALL

hexchat.hook_command('lastfm', lfmHelp, help='/np sends your currently playing song according to last.fm. Use /help lastfmuser and /help lastfmapi for configuration information.')
hexchat.hook_command('lastfmuser', setUSER, help='/lastfmuser set <last.fm username> sets the username the plugin uses to fetch your song information. Use /lastfmuser reset to reset it.')
hexchat.hook_command('lastfmapi', setKEY, help='/lastfmapi set <last.fm API key> sets the API key the plugin uses to fetch your song information. Use /lastfmapi reset to reset it.')
hexchat.hook_command('np', np, help='/np sends your currently playing song according to last.fm.')

def lfm_unloaded(userdata):
    hexchat.emit_print('Notice', '', '%s v%s by %s unloaded' % (__module_name__, __module_version__, __module_author__))
    return hexchat.EAT_ALL
hexchat.emit_print('Notice', '', '%s v%s by %s loaded' % (__module_name__, __module_version__, __module_author__))
hexchat.hook_unload(lfm_unloaded)
