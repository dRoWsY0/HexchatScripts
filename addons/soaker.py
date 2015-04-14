import time
import hexchat

__module_name__ = 'NWOSoak'
__module_author__ = 'NewellWorldOrder'
__module_version__ = '1.0'
__module_description__ = 'Soakbot'

def enablesoak(word, word_eol, userdata):
    hexchat.set_pluginpref('soakbot', 'yes')
    print('Soaker enabled')
    return hexchat.EAT_ALL
    
def disablesoak(word, word_eol, userdata):
    hexchat.set_pluginpref('soakbot', 'no')
    print('Soaker disabled >:')
    return hexchat.EAT_ALL

def soakerlistadd(word, word_eol, userdata):
    ignoreList = hexchat.get_pluginpref('soakbotignorelist')
    if ignoreList != 'None':
        hexchat.set_pluginpref('soakbotignorelist', '%s %s' % (ignoreList, word_eol[1].lower()))
    else:
        hexchat.set_pluginpref('soakbotignorelist', '%s' % word_eol[1].lower())
    print('%s added to the ignore list' % ', '.join(word_eol[1].split(' ')))
    return hexchat.EAT_ALL

def soakerlistlist(word, word_eol, userdata):
    ignoreList = hexchat.get_pluginpref('soakbotignorelist')
    print(ignoreList)
    return hexchat.EAT_ALL
    
def soakerlistremove(word, word_eol, userdata):
    ignoreList = hexchat.get_pluginpref('soakbotignorelist').split(' ')
    for user in ignoreList:
        for removal in word:
            if removal != word[1] and ignoreList.count(removal) >= 1:
                ignoreList.remove(removal)
    return hexchat.EAT_ALL

def soakerlistclear(word, word_eol, userdata):
    hexchat.del_pluginpref('soakbotignorelist')
    print('Ignore list cleared')
    return hexchat.EAT_ALL
    
def soakerActivityCheck(actionNick):
    activeList = []
    ignoreList = hexchat.get_pluginpref('soakbotignorelist').split(' ')
    for active in hexchat.get_list('users'):
        appendList = False
        if time.time() - active.lasttalk <= 600 and hexchat.nickcmp(active.nick, hexchat.get_info('nick')) != 0 and hexchat.nickcmp(active.nick, actionNick) != 0:
            for ignored in ignoreList:
                if hexchat.nickcmp(active.nick, ignored) == 0:
                    appendList = True
            if appendList == False:
                activeList.append(active.nick)
    return activeList
            
def soakerMessageHandler(word, word_eol, userdata):
    soakbotNick = hexchat.get_info('nick')
    status = hexchat.get_pluginpref('soakbot')
    if status == 'yes':
        if word[1].lower() == '!active':
            hexchat.command('say I spy with my little NSA, %s meltable shibe beams. Only users identified with NickServ are included.' % len(soakerActivityCheck(word[0])))
        #elif word[0] == 'Doger':
        else:
            #if word[1].split(' ')[0] == 'Such' and word[1].split(' ')[6] == soakbotNick + '!':
            if word[1].split(' ')[0] == '!tip' and word[1].split(' ')[1] == soakbotNick:
                #initUser = word[1].split(' ')[1]
                initUser = word[0]
                #soakAmount = int(word[1].split(' ')[4][1:])
                soakAmount = int(word[1].split(' ')[2])
                listActive = soakerActivityCheck(initUser)
                averageTip = soakAmount//len(listActive)
                if averageTip < 10:
                    hexchat.command('say Sorry %s, jet fuel can\'t melt steel beams. Returning soak.' % initUser)
                    #hexchat.command('msg Doger tip %s %s' % (initUser, soakAmount))
                else:
                    hexchat.command('say %s is melting %s shibe beams with Ɖ%s: %s' % (initUser, len(listActive), averageTip, ', '.join(listActive)))
                    #hexchat.command('msg Doger mtip %s %s' % ((' %s ' % str(averageTip)).join(listActive), averageTip))
    return hexchat.EAT_PLUGIN

hexchat.hook_command('enablesoak', enablesoak, help='/enablesoak turns soak on')
hexchat.hook_command('disablesoak', disablesoak, help='/disablesoak turns soak off')
hexchat.hook_command('soakerignoreadd', soakerlistadd, help='/soakerlistadd adds users to ignore list')
hexchat.hook_command('soakerignorelist', soakerlistlist, help='/soakerlistignore lists users on the ignore list')
hexchat.hook_command('soakerignoreremove', soakerlistremove, help='/soakerlistremove removes users from the ignore list')
hexchat.hook_command('soakerignoreclear', soakerlistclear, help='/soakerignoreclear clears the ignore list')

hexchat.hook_print('Channel Message', soakerMessageHandler)
hexchat.hook_print('Channel Msg Hilight', soakerMessageHandler)

def nwo_unloaded(userdata):
    hexchat.set_pluginpref('soakbot', 'no')
    hexchat.emit_print('Notice', '', '%s v%s by %s unloaded' % (__module_name__, __module_version__, __module_author__))
    return hexchat.EAT_ALL
hexchat.emit_print('Notice', '', '%s v%s by %s loaded' % (__module_name__, __module_version__, __module_author__))
hexchat.hook_unload(nwo_unloaded)
