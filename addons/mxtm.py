import hexchat
import praw

__module_name__ = 'mxtm'
__module_author__ = 'NewellWorldOrder'
__module_version__ = '1.0'
__module_description__ = 'Links random mxtm photoshop'

r = praw.Reddit(user_agent='HexchatMXTMPhotoshopsGrabber')
limit = 0

def enablemxtm(word, word_eol, userdata):
    hexchat.set_pluginpref('mxtm', 'yes')
    print('mxtm enabled')
    return hexchat.EAT_ALL
    
def disablemxtm(word, word_eol, userdata):
    hexchat.del_pluginpref('mxtm')
    print('mxtm disabled >:')
    return hexchat.EAT_ALL

def timereset(userdata):
    global limit
    limit = 0
    return 0

def mxtm(word, word_eol, userdata):
    status = hexchat.get_pluginpref('mxtm')
    global limit
    if limit == 0 and word[1] == '!mxtm' and status == 'yes':
        context = hexchat.get_info('channel')
        if context == '##mxtmfanclub' or context == '#Chat' or context == '##dogecoin-bots':
            link = r.get_random_submission(subreddit='mxtmphotoshopbattles')
            hexchat.command('say %s – %s' % (link, link.url))
            limit = 1
            hexchat.hook_timer(2000, timereset)
        
    return hexchat.EAT_NONE

hexchat.hook_command('enablemxtm', enablemxtm, help='/enablemxtm turns mxtm on')
hexchat.hook_command('disablemxtm', disablemxtm, help='/disablemxtm turns mxtm off')
hexchat.hook_print('Channel Message', mxtm)

def mxtm_unloaded(userdata):
    hexchat.emit_print('Notice', '', '%s v%s by %s unloaded' % (__module_name__, __module_version__, __module_author__))
    return hexchat.EAT_ALL
hexchat.emit_print('Notice', '', '%s v%s by %s loaded' % (__module_name__, __module_version__, __module_author__))
hexchat.hook_unload(mxtm_unloaded)
