import hexchat
import pylast

__module_name__ = 'last.fm'
__module_author__ = 'NewellWorldOrder'
__module_version__ = '1'
__module_description__ = 'Announces current song playing in Foobar for Windows'

API_KEY = "7708894264808d07c54730658c42b6e5"
API_SECRET = "a7916004c04083ca31d97fdc1e2e9255"
lastfm_username = "brnwng"
lastfm_password_hash = "0366c0f551dc1e5a2854731822c62b71"
lastfm_network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET, username=lastfm_username, password_hash=lastfm_password_hash)

def np_cb(word, word_eol, userdata):
    title = lastfm_network.get_user(lastfm_username).get_now_playing().title
    artist = lastfm_network.get_user(lastfm_username).get_now_playing().artist
    
    hexchat.command('me now playing \00311%s \017by \00313%s.' % (title, artist))

    return hexchat.EAT_ALL

hexchat.hook_command('np', np_cb)
