import hexchat

__module_name__ = 'NWOutils'
__module_author__ = 'NewellWorldOrder'
__module_version__ = '2.0'
__module_description__ = 'Stealth op commands'

def nwo_op(word, word_eol, userdata):
    chan = hexchat.get_info('channel')
    nick = hexchat.get_info('nick')
    if len(word) == 1:
        hexchat.command('RAW PRIVMSG ChanServ :op %s' % chan)
    else:
        i = len(word) - 1
        while i > 0:
            hexchat.command('RAW PRIVMSG ChanServ :op %s %s' % (chan, word[i]))
            i -= 1
    return hexchat.EAT_ALL

def nwo_deop(word, word_eol, userdata):
    chan = hexchat.get_info('channel')
    nick = hexchat.get_info('nick')
    if len(word) == 1:
        hexchat.command('RAW PRIVMSG ChanServ :deop %s' % chan)
    else:
        i = len(word) - 1
        while i > 0:
            hexchat.command('RAW PRIVMSG ChanServ :deop %s %s' % (chan, word[i]))
            i -= 1
    return hexchat.EAT_ALL

def nwo_kick(word, word_eol, userdata):
    users = hexchat.get_list('users')
    chan = hexchat.get_info('channel')
    nick = hexchat.get_info('nick')
    if len(word) >= 2:
        for user in users:
            if hexchat.nickcmp(user.nick, word[1]) == 0:
                host = user.host.split('@')[1]
                hexchat.command('RAW PRIVMSG ChanServ :op %s' % chan)
                hexchat.command('timer 1 RAW MODE %s -e+b *!*@%s *!*@%s' % (chan, host, host))
                if len(word) > 2:
                    hexchat.command('timer 1 RAW KICK %s %s %s' % (chan, word[1], word_eol[2]))
                else:
                    hexchat.command('timer 1 RAW KICK %s %s' % (chan, word[1]))
                hexchat.command('timer 2 RAW MODE %s -o %s' % (chan, nick))
                break
    return hexchat.EAT_ALL

def nwo_unquiet(word, word_eol, userdata):
    users = hexchat.get_list('users')
    chan = hexchat.get_info('channel')
    nick = hexchat.get_info('nick')
    if len(word) >= 2:
        for user in users:
            if hexchat.nickcmp(user.nick, word[1]) == 0:
                host = user.host.split('@')[1]
                hexchat.command('RAW PRIVMSG ChanServ :op %s' % chan)
                hexchat.command('timer 1 RAW MODE %s -q *!*@%s *!*@%s' % (chan, host, host))
                hexchat.command('timer 2 RAW MODE %s -o %s' % (chan, nick))
                break
    return hexchat.EAT_ALL

def nwo_judo(word, word_eol, userdata):
    chan = hexchat.get_info('channel')
    nick = hexchat.get_info('nick')
    try:
        hexchat.command('RAW PRIVMSG ChanServ :op %s' % chan)
        hexchat.command('timer 1 %s' % word_eol[1])
        hexchat.command('timer 2 RAW MODE %s -o %s' % (chan, nick))
    except:
        print('Failed')
    return hexchat.EAT_ALL

def nwo_dankyamyams(word, word_eol, userdata):
    if len(word) > 0:
        hexchat.command('say \00303>%s' % word_eol[1])
    return hexchat.EAT_ALL

hexchat.hook_command('op', nwo_op, help='/op will op you if +o flags are set on you. /op <nickname> [<nickname>] will op others')
hexchat.hook_command('deop', nwo_deop, help='/deop will deop you if +o flags are set for you. /deop <nickname> [<nickname>] will deop others')
hexchat.hook_command('kb', nwo_kick, help='/kb <nickname> will temporarily op you, kickban <nickname> and deop you')
hexchat.hook_command('uq', nwo_unquiet)
hexchat.hook_command('judo', nwo_judo, help='/judo <op command> temporarily gives you operator status to execute a command.')
hexchat.hook_command('>', nwo_dankyamyams)

def nwo_unloaded(userdata):
    hexchat.emit_print('Notice', '', '%s v%s by %s unloaded' % (__module_name__, __module_version__, __module_author__))
    return hexchat.EAT_ALL
hexchat.emit_print('Notice', '', '%s v%s by %s loaded' % (__module_name__, __module_version__, __module_author__))
hexchat.hook_unload(nwo_unloaded)
