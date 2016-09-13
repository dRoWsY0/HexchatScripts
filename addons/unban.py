import hexchat

__module_name__ = 'NWOunban'
__module_author__ = 'NewellWorldOrder'
__module_version__ = '1.0'
__module_description__ = 'Auto unban and rejoin script'

limit = 0

def rejoin(word, word_eol, userdata):
    hexchat.command('TIMER 1 RAW JOIN %s' % word[1])
    hexchat.hook_server('474', unban, userdata = word[1])
    return hexchat.EAT_PLUGIN

def timereset(userdata):
    global limit
    limit = 0
    return 0

def unban(word, word_eol, userdata):
    global limit
    if limit == 0:
        nick = hexchat.get_info('nick')
        hexchat.command('RAW PRIVMSG ChanServ :UNBAN %s %s' % (userdata, nick))
        hexchat.command('timer 1 RAW JOIN %s' % userdata)
        limit = 1
        hexchat.hook_timer(2000, timereset)
    return hexchat.EAT_PLUGIN

hexchat.hook_print('You Kicked', rejoin)

def nwo_unloaded(userdata):
    hexchat.emit_print('Notice', '', '%s v%s by %s unloaded' % (__module_name__, __module_version__, __module_author__))
    return hexchat.EAT_ALL
hexchat.emit_print('Notice', '', '%s v%s by %s loaded' % (__module_name__, __module_version__, __module_author__))
hexchat.hook_unload(nwo_unloaded)
