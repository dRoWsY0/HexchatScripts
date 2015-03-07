import hexchat
import pylast

__module_name__ = 'last.fm'
__module_author__ = 'NewellWorldOrder'
__module_version__ = '1'
__module_description__ = 'Announces current song playing in Foobar for Windows'

API_KEY = "API_KEY"
API_SECRET = "API_SECRET_KEY"
lastfm_username = "username"
lastfm_password_hash = "md5hashofpassword"
lastfm_network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET, username=lastfm_username, password_hash=lastfm_password_hash)

def np(word, word_eol, userdata):
    title = lastfm_network.get_user(lastfm_username).get_now_playing().title
    artist = lastfm_network.get_user(lastfm_username).get_now_playing().artist
    
    hexchat.command('me now playing \00311%s \017by \00313%s.' % (title, artist))

    return hexchat.EAT_ALL

hexchat.hook_command('np', np)
