import hexchat

__module_name__ = 'NWOutils'
__module_author__ = 'NewellWorldOrder'
__module_version__ = '1'
__module_description__ = 'Stealth op commands'

def op_make(word, word_eol, userdata):
    chan = hexchat.get_info('channel')
    if len(word) < 2:
        hexchat.command('cs op %s' % chan)
    else:
        hexchat.command('cs op {} {}'.format(chan, word_eol[1]))
    return hexchat.EAT_ALL

def op_remove(word, word_eol, userdata):
    chan = hexchat.get_info('channel')
    if len(word) < 2:
        hexchat.command('cs deop %s' % chan)
    else:
        hexchat.command('cs deop {} {}'.format(chan, word_eol[1]))
    return hexchat.EAT_ALL

def op_kick(word, word_eol, userdata):
    users = hexchat.get_list('users')
    chan = hexchat.get_info('channel')
    if len(word) > 1:
        hexchat.command('cs op %s' % chan)
        hexchat.command('timer 1 kickban %s' % word_eol[1])
        hexchat.command('timer 1 cs deop %s' % chan)

    return hexchat.EAT_ALL

def op_whois(word, word_eol, userdata):
    chan = hexchat.get_info('channel')
    bUser = word[2]
    hexchat.command('cs op %s' % chan)
    hexchat.command('timer 1 unban *!*@%s' % bUser)
    hexchat.command('timer 1.5 invite %s' % userdata)
    hexchat.command('timer 1.7 cs deop %s' % chan)
    
    return hexchat.EAT_ALL

def op_unkick(word, word_eol, userdata):
    if len(word) > 1:
        hexchat.command('whois %s' % word[1])
        hexchat.hook_print('WhoIs Name Line', op_whois, word[1])
    
    return hexchat.EAT_ALL

def op_quiet(word, word_eol, userdata):
    users = hexchat.get_list('users')
    chan = hexchat.get_info('channel')
    if len(word) > 0:
        for user in users:
            if user.nick.lower() == word[1].lower():
                break

        hexchat.command('cs op %s' % chan)
        hexchat.command('timer 1 mode %s +q *!*@%s' % (chan, user.host.split('@')[1]))
        hexchat.command('timer 2 cs deop %s' % chan)
            
    return hexchat.EAT_ALL

def op_unquiet(word, word_eol, userdata):
    users = hexchat.get_list('users')
    chan = hexchat.get_info('channel')
    if len(word) > 0:
        for user in users:
            if user.nick.lower() == word[1].lower():
                break
            
        host = user.host.split('@')[1]
            
        hexchat.command('cs op %s' % chan)
        hexchat.command('timer 1 mode %s -q *!*@%s' % (chan, user.host.split('@')[1]))
        hexchat.command('timer 2 cs deop %s' % chan)
            
    return hexchat.EAT_ALL

hexchat.hook_command('op', op_make)
hexchat.hook_command('deop', op_remove)
hexchat.hook_command('kick', op_kick)
hexchat.hook_command('unkick', op_unkick)
hexchat.hook_command('quiet', op_quiet)
hexchat.hook_command('unquiet', op_unquiet)
