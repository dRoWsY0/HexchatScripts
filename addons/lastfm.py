import hexchat

try:
    import requests
except:
    print('LastFM: lastfm.py requres the requests python library. Link: http://docs.python-requests.org/en/latest/')

__module_name__ = 'last.fm'
__module_author__ = 'newellworldorder'
__module_version__ = '3.0'
__module_description__ = 'Announces current song playing in Last.FM'

HELPTEXT = '\002/LastFM help\017 for help.'
KEY = '6e54358934d2d0b1b926e25613384520'
COMMANDS = ['set','reset','print']
SETTINGS = ['user','base_color','track_color','artist_color','album_color']
COLORS = {'white': '00', 'black': '01', 'blue': '02', 'green': '03', 'lightred': '04', 'brown': '05',
           'purple': '06', 'orange': '07', 'yellow': '08', 'lightgreen': '09', 'cyan': '10', 'lightcyan': '11',
           'lightblue': '12', 'pink': '13', 'grey': '14', 'lightgrey': '15'}

def cleanOldVer():
    if hexchat.get_pluginpref('lfmnwo_user'):
        hexchat.set_pluginpref('lastfm_user', hexchat.get_pluginpref('lfmnwo_user'))
        hexchat.del_pluginpref('lfmnwo_user')
    if hexchat.get_pluginpref('lfmnwo_apikey'):
        hexchat.del_pluginpref('lfmnwo_apikey')
    return

def defaultColors():
    if not hexchat.get_pluginpref('lastfm_base_color'):
        hexchat.set_pluginpref('lastfm_base_color', 'purple')
    if not hexchat.get_pluginpref('lastfm_track_color'):
        hexchat.set_pluginpref('lastfm_track_color', 'lightcyan')
    if not hexchat.get_pluginpref('lastfm_artist_color'):
        hexchat.set_pluginpref('lastfm_artist_color', 'pink')
    if not hexchat.get_pluginpref('lastfm_album_color'):
        hexchat.set_pluginpref('lastfm_album_color', 'lightgreen')
    return

def genHelp():
    helpString = ('LastFM: You must set a last.fm username as user in order for this script to function.\n')
    helpString += ('LastFM:  To change the value of any setting, \002/LastFM set <setting> <value>\017.\n')
    helpString += ('LastFM:  To delete the value of any setting, \002/LastFM reset <setting>\017.\n')
    helpString += ('LastFM:  To print the value of any setting, \002/LastFM print <setting>\017.\n')
    helpString += ('LastFM:  To print the currently playing song of the chosen last.fm user, \002/np\017.\n')
    helpString += ('LastFM:  To print the currently playing song without colors, \002/np plain\017.\n')
    helpString += ('LastFM:  Available commands are:\n')
    helpString += ('LastFM:   \02%s\n' % '\017, \02'.join(COMMANDS))
    helpString += ('LastFM:  Available settings are:\n')
    helpString += ('LastFM:   \02%s\n' % '\017, \02'.join(SETTINGS))
    helpString += ('LastFM:  Available colors are:\n')
    printColors = []
    for k, v in COLORS.items():
        printColors.append('\03%s%s' % (v, k))
    helpString += ('LastFM:   \02%s' % '\017, \02'.join(printColors))
    return helpString
        
def nowPlaying(word, word_eol, userdata):
    USER = hexchat.get_pluginpref('lastfm_user')
    if USER:
        try:
            r=requests.get(r'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=%s&api_key=%s&format=json' % (USER, KEY))
            data = r.json()
            try:
                nowplaying = data['recenttracks']['track'][0]['@attr']['nowplaying']
                track = data['recenttracks']['track'][0]['name']
                artist = data['recenttracks']['track'][0]['artist']['#text']
                album = data['recenttracks']['track'][0]['album']['#text']
                if len(word) > 1 and word[1].lower() == 'plain':
                    if album:
                        hexchat.command('me now playing %s by %s from %s' % (track, artist, album))
                    else:
                        hexchat.command('me now playing %s by %s' % (track, artist))
                else:
                    bCol = '\003%s' % COLORS[hexchat.get_pluginpref('lastfm_base_color')]
                    track = '\003%s%s%s' % (COLORS[hexchat.get_pluginpref('lastfm_track_color')], track, bCol)
                    artist = '\003%s%s%s' % (COLORS[hexchat.get_pluginpref('lastfm_artist_color')], artist, bCol)
                    if album:
                        album = '\003%s%s%s' % (COLORS[hexchat.get_pluginpref('lastfm_album_color')], album, bCol)
                        hexchat.command('me %snow playing %s by %s from %s' % (bCol, track, artist, album))
                    else:
                        hexchat.command('me %snow playing %s by %s' % (bCol, track, artist))
            except:
                print('LastFM: No song playing')
        except:
            print('LastFM: Cannot connect to Last.fm')
    else:
        print('LastFM: Username not found. %s' % HELPTEXT)
    return hexchat.EAT_ALL

def lastFM(word, word_eol, userdata):
    try:
        if word[1].lower() == 'help':
            print(genHelp())
        elif word[1].lower() in COMMANDS:
            if word[2].lower() in SETTINGS:
                key = word[2].lower()
                prefKey = 'lastfm_%s' % key
                keyReadable = key.replace('_', ' ').title()
                if word[1].lower() == 'set':
                    try:
                        value = word[3].lower()
                        if 'color' in key and value.lower() not in COLORS.keys():
                            print('LastFM: Unknown color \02%s\017. %s' % (value.lower(), HELPTEXT))
                        else:
                            hexchat.set_pluginpref(prefKey, value)
                            print('LastFM: %s set to \002%s\017' % (key, value))
                    except:
                        print('LastFM: Syntax: \002/LastFM SET \037setting\037 \037value\017. %s' % HELPTEXT)
                elif word[1].lower() == 'reset':
                    if hexchat.get_pluginpref(prefKey):
                        prefValue = hexchat.get_pluginpref(prefKey)
                        hexchat.del_pluginpref(prefKey)
                        if 'color' in prefKey:
                            defaultColors()
                        print('LastFM: %s \002%s\017 removed.' % (keyReadable, prefValue))
                    else:
                        print('LastFM: Value for setting \002%s\017 not found. %s' % (keyReadable, HELPTEXT))
                elif word[1].lower() == 'print':
                    prefValue = hexchat.get_pluginpref(prefKey)
                    if hexchat.get_pluginpref(prefKey):
                        print('LastFM: The value of %s is \002%s\017.' % (keyReadable, prefValue))
                    else:
                        print('LastFM: Value for setting \002%s\017 not found. %s' % (keyReadable, HELPTEXT))
            else:
                print('LastFM: Unknown setting \002%s\017. %s' % (word[2], HELPTEXT))
        else:
            print('LastFM: Unknown command \002%s\017. %s' % (word[1], HELPTEXT))
    except:
        print('LastFM: Not enough parameters. %s' % HELPTEXT)
    return hexchat.EAT_ALL

cleanOldVer()
defaultColors()

hexchat.hook_command('lastfm', lastFM, help=genHelp())
hexchat.hook_command('np', nowPlaying, help=genHelp())

def lfm_unloaded(userdata):
    hexchat.emit_print('Notice', '', '%s v%s by %s unloaded' % (__module_name__, __module_version__, __module_author__))
    return hexchat.EAT_ALL
hexchat.emit_print('Notice', '', '%s v%s by %s loaded' % (__module_name__, __module_version__, __module_author__))
hexchat.hook_unload(lfm_unloaded)
