import hexchat
import requests

__module_name__ = 'last.fm'
__module_author__ = 'NewellWorldOrder'
__module_version__ = '2.0'
__module_description__ = 'Announces current song playing in Last.FM'

def setUSER(word, word_eol, userdata):
    hexchat.set_pluginpref('user', word[1])
    print('Username set to "%s"' % word[1])
    return hexchat.EAT_ALL
    
def setKEY(word, word_eol, userdata):
    hexchat.set_pluginpref('apikey', word[1])
    print('API key set to "%s"' % word[1])
    return hexchat.EAT_ALL
    
def resetUSER(word, word_eol, userdata):
    print('Username reset (old username=%s)' % hexchat.get_pluginpref('user'))
    hexchat.del_pluginpref('user')
    return hexchat.EAT_ALL
    
def resetKEY(word, word_eol, userdata):
    print('API key reset (old API key=%s)' % hexchat.get_pluginpref('apikey'))
    hexchat.del_pluginpref('apikey')
    return hexchat.EAT_ALL

def np(word, word_eol, userdata):
    USER = hexchat.get_pluginpref('user')
    APIKEY = hexchat.get_pluginpref('apikey')
    if USER and APIKEY:
        r=requests.get(r'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=%s&api_key=%s&format=json' % (USER, APIKEY))
        data = r.json()
        try:
            nowplaying = data['recenttracks']['track'][0]['@attr']['nowplaying']
            songArtist = data['recenttracks']['track'][0]['artist']['#text']
            songName = data['recenttracks']['track'][0]['name']
            songAlbum = data['recenttracks']['track'][0]['album']['#text']
            hexchat.command('me \00306now playing \00311%s \00306by \00313%s \00306from \00309%s' % (songName, songArtist, songAlbum))
        except:
            print('No song playing')
        return hexchat.EAT_ALL
    if not USER:
        print('Use /setuser <last.fm username> to set a username for the plugin to fetch song data from')
    if not APIKEY:
        print('Use /setapikey <last.fm API key> to set a API key for the plugin to fetch song data from')
    return hexchat.EAT_ALL

hexchat.hook_command('setuser', setUSER, help='/setuser <last.fm username> sets the username the plugin uses to fetch your song information')
hexchat.hook_command('setapikey', setKEY, help='/setapikey <last.fm API key> sets the API key the plugin uses to fetch your song information')
hexchat.hook_command('resetuser', resetUSER, help='/resetuser resets the username the plugin uses to fetch your song information')
hexchat.hook_command('resetapikey', resetKEY, help='/resetapikey resets the API key the plugin uses to fetch your song information')
hexchat.hook_command('np', np)

def lfm_unloaded(userdata):
    hexchat.emit_print('Notice', '', '%s v%s by %s unloaded' % (__module_name__, __module_version__, __module_author__))
    return hexchat.EAT_ALL
hexchat.emit_print('Notice', '', '%s v%s by %s loaded' % (__module_name__, __module_version__, __module_author__))
hexchat.hook_unload(lfm_unloaded)
