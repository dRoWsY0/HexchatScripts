import hexchat

__module_name__ = 'NWOutils'
__module_author__ = 'NewellWorldOrder'
__module_version__ = '1'
__module_description__ = 'Stealth op commands'

def op_op(word, word_eol, userdata):
    chan = hexchat.get_info('channel')
    if len(word) == 1:
        hexchat.command('cs op %s' % chan)
    else:
        i = len(word) - 1
        while i > 0:
            hexchat.command('cs op %s %s' % (chan, word[i]))
            i -= 1
            
    return hexchat.EAT_ALL

def op_deop(word, word_eol, userdata):
    chan = hexchat.get_info('channel')
    if len(word) == 1:
        hexchat.command('cs deop %s' % chan)
    else:
        i = len(word) - 1
        while i > 0:
            hexchat.command('cs deop %s %s' % (chan, word[i]))
            i -= 1
    return hexchat.EAT_ALL

def op_kick(word, word_eol, userdata):
    users = hexchat.get_list('users')
    chan = hexchat.get_info('channel')
    if len(word) > 0:
        hexchat.command('cs op %s' % chan)
        hexchat.command('timer 1 kickban %s' % word_eol[1])
        hexchat.command('timer 1 cs deop %s' % chan)
    return hexchat.EAT_ALL

def op_unban(word, word_eol, userdata):
    chan = hexchat.get_info('channel')
    if len(word) == 2:
        cnc = hexchat.find_context(channel='freenode')
        cnc.set()
        cnc.command('whois %s' % word[1])
        hexchat.hook_print('WhoIs Name Line', op_unban)
    elif len(word) > 2:
        hexchat.command('cs op %s' % chan)
        hexchat.command('timer 1 MODE %s -b *!*@%s' % (chan, word[2]))
        hexchat.command('timer 1.7 cs deop %s' % chan)
    return hexchat.EAT_PLUGIN

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
        hexchat.command('cs op %s' % chan)
        hexchat.command('timer 1 mode %s -q *!*@%s' % (chan, user.host.split('@')[1]))
        hexchat.command('timer 2 cs deop %s' % chan)
    return hexchat.EAT_ALL

def op_recover(word, word_eol, userdata):
    if len(word) > 0:
        hexchat.command('cs unban %s' % word[1])
        hexchat.command('join %s' % word[1])
    return hexchat.EAT_ALL

def nwo_greentext(word, word_eol, userdata):
    if len(word) > 0:
        hexchat.command('say \00303>%s' % word_eol[1])
    return hexchat.EAT_ALL

hexchat.hook_command('op', op_op)
hexchat.hook_command('deop', op_deop)
hexchat.hook_command('kick', op_kick)
hexchat.hook_command('unban', op_unban)
hexchat.hook_command('quiet', op_quiet)
hexchat.hook_command('unquiet', op_unquiet)
hexchat.hook_command('recover', op_recover)
hexchat.hook_command('>', nwo_greentext)
