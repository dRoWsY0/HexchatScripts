import hexchat as hexchat

__module_name__ = 'Hidden Op'
__module_author__ = 'NewellWorldOrder'
__module_version__ = '1'
__module_description__ = 'Stealth op commands'

bannedUser = ''

def op_make(word, word_eol, userdata):
    chan = hexchat.get_info('channel')
    if len(word) < 2:
        hexchat.command('cs op ' + chan)
    else:
        hexchat.command('cs op ' + chan + ' ' + word_eol[1])
    return hexchat.EAT_ALL

def op_remove(word, word_eol, userdata):
    chan = hexchat.get_info('channel')
    if len(word) < 2:
        hexchat.command('cs deop ' + chan)
    else:
        hexchat.command('cs deop ' + chan + ' ' + word_eol[1])
    return hexchat.EAT_ALL

def op_kick(word, word_eol, userdata):
    users = hexchat.get_list('users')
    chan = hexchat.get_info('channel')
    if len(word) > 0:
        for user in users:
            if user.nick.lower() == word[1].lower():
                break
        bannedUser = '*!*@%s' % user.host.split('@')[1]
        hexchat.command('cs op ' + chan)
        hexchat.command('timer 1 kickban ' + word_eol[1])
        hexchat.command('timer 1 cs deop ' + chan)

    return hexchat.EAT_ALL

def op_whois(word, word_eol, userdata):
    if len (word) <2:
        print(word[2])
        
    return hexchat.EAT_ALL

def op_unban(word, word_eol, userdata):
    chan = hexchat.get_info('channel')
    hexchat.command('whois %s' % word[1])
    hexchat.command('cs op ' + chan)
    hexchat.command('cs deop ' + chan)
            
    return hexchat.EAT_ALL

def op_quiet(word, word_eol, userdata):
    users = hexchat.get_list('users')
    chan = hexchat.get_info('channel')
    if len(word) > 0:
        for user in users:
            if user.nick.lower() == word[1].lower():
                break
        
        hexchat.command('cs op ' + chan)
        hexchat.command('mode %s +q *!*@%s' % (chan, user.host.split('@')[1]))
        hexchat.command('cs deop ' + chan)
            
    return hexchat.EAT_ALL

def op_unquiet(word, word_eol, userdata):
    users = hexchat.get_list('users')
    chan = hexchat.get_info('channel')
    if len(word) > 0:
        for user in users:
            if user.nick.lower() == word[1].lower():
                break
        
        hexchat.command('cs op ' + chan)
        hexchat.command('mode %s -q *!*@%s' % (chan, user.host.split('@')[1]))
        hexchat.command('cs deop ' + chan)
            
    return hexchat.EAT_ALL

hexchat.hook_command('op', op_make)
hexchat.hook_command('deop', op_remove)
hexchat.hook_command('kick', op_kick)
hexchat.hook_print('Whois Real Host', op_whois)
hexchat.hook_command('unban', op_unban)
hexchat.hook_command('quiet', op_quiet)
hexchat.hook_command('unquiet', op_unquiet)
