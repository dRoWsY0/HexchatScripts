import time
import hexchat
import re

__module_name__ = 'NWOSoak'
__module_author__ = 'NewellWorldOrder'
__module_version__ = '1.0'
__module_description__ = 'Soakbot'

hexchat.set_pluginpref('soakbot', 'no')
soakAllList = []
noSoakList = []
activeTimer = 10

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
    global soakAllList
    global noSoakList
    global activeTimer
    soakAll = False
    if actionNick in soakAllList:
        soakAll = True
    activeList = []
    ignoreListNickserv = []
    ignoreList = hexchat.get_pluginpref('soakbotignorelist').split(' ')
    ignoreList.extend([actionNick.lower(), hexchat.get_info('nick').lower()])
    ignoreList.extend(noSoakList)
    for active in hexchat.get_list('users'):
        if active.nick.lower() == actionNick:
            ignoreListNickserv.append(active.account)
    for active in hexchat.get_list('users'):
        if time.time() - active.lasttalk <= (60 * activeTimer) or soakAll:
            if active.host.split('@')[1] != 'services.' and active.nick.lower() not in ignoreList and active.account not in ignoreListNickserv:
                activeList.append(active.nick)
                ignoreListNickserv.append(active.account)
    noSoakList = []
    activeTimer = 10
    return activeList
            
def soakerMessageHandler(word, word_eol, userdata):
    global soakAllList
    global noSoakList
    global activeTimer
    soakbotNick = hexchat.get_info('nick')
    status = hexchat.get_pluginpref('soakbot')
    message = word[1].lower().split(' ')
    if status == 'yes':
        if message[0] == '!active':
            hexchat.command('say I spy with my little NSA, %s meltable shibe beams. Only users identified with NickServ are included.' % len(soakerActivityCheck(word[0])))
        elif len(message) >= 4 and message[0] + ' ' + message[1] == '!tip ' + soakbotNick.lower():
            subUser = re.compile('-.*')
            newTime = re.compile('--timer=\d*')
            if 'all' in message[3:]:
                soakAllList.append(word[0].lower())
            for words in message[3:]:
                m = re.match(newTime, words)
            if m.string:
                activeTimer = int(m.string.split('=')[1])
            noSoakList = [match[1:] for match in message[3:] if re.match(subUser, match)]
        elif word[0] == 'Doger':
            if message[0] == 'such' and message[6] == soakbotNick.lower() + '!':
                initUser = word[1].split(' ')[1]
                soakAmount = int(message[4][1:])
                listActive = soakerActivityCheck(initUser.lower())
                if len(listActive) >= 1:
                    averageTip = soakAmount//len(listActive)
                    if averageTip < 10:
                        hexchat.command('say Sorry %s, jet fuel can\'t melt steel beams. Returning soak.' % initUser)
                        #hexchat.command('say %s YOU\'LL GO BLIND! Returning soak.' % initUser)
                        hexchat.command('msg Doger tip %s %s' % (initUser, soakAmount))
                    else:
                        hexchat.command('say %s is melting %s shibe beams with Ɖ%s: %s' % (initUser, len(listActive), averageTip, ', '.join(listActive)))
                        #hexchat.command('say %s is bukkaking %s horny shibes with %sL of cum: %s' % (initUser, len(listActive), averageTip, ', '.join(listActive)))
                        hexchat.command('msg Doger mtip %s %s' % ((' %s ' % str(averageTip)).join(listActive), averageTip))
                try:
                    soakAllList.remove(initUser)
                    
                except:
                    print('')
        return hexchat.EAT_ALL
    return hexchat.EAT_NONE

def ignoreDoger(word, word_eol, userdata):
    status = hexchat.get_pluginpref('soakbot')
    if status == 'yes':
        return hexchat.EAT_ALL
    return hexchat.EAT_NONE

hexchat.hook_command('enablesoak', enablesoak, help='/enablesoak turns soak on')
hexchat.hook_command('disablesoak', disablesoak, help='/disablesoak turns soak off')
hexchat.hook_command('soakerignoreadd', soakerlistadd, help='/soakerlistadd adds users to ignore list')
hexchat.hook_command('soakerignorelist', soakerlistlist, help='/soakerlistignore lists users on the ignore list')
hexchat.hook_command('soakerignoreremove', soakerlistremove, help='/soakerlistremove removes users from the ignore list')
hexchat.hook_command('soakerignoreclear', soakerlistclear, help='/soakerignoreclear clears the ignore list')

hexchat.hook_print('Private Message', ignoreDoger)
hexchat.hook_print('Private Message to Dialog', ignoreDoger)
hexchat.hook_print('Channel Message', soakerMessageHandler)
hexchat.hook_print('Channel Msg Hilight', soakerMessageHandler)

hexchat.set_pluginpref('soakbot', 'no')

def nwo_unloaded(userdata):
    hexchat.set_pluginpref('soakbot', 'yes')
    print('Soaker enabled')
    hexchat.emit_print('Notice', '', '%s v%s by %s unloaded' % (__module_name__, __module_version__, __module_author__))
    return hexchat.EAT_ALL
hexchat.emit_print('Notice', '', '%s v%s by %s loaded' % (__module_name__, __module_version__, __module_author__))
hexchat.hook_unload(nwo_unloaded)
