import time
import hexchat

__module_name__ = 'NWOSoak'
__module_author__ = 'NewellWorldOrder'
__module_version__ = '1.0'
__module_description__ = 'Soakbot'

nOgAnOo = ['Doger','DogeXM','BeeSoaker','DogeAI','ExperimentalBot','SuchModBot']

def censusData():
    global nOgAnOo
    vaccinatedPeople = []
    for sheeple in hexchat.get_list('users'):
        exposed = False
        if time.time() - sheeple.lasttalk <= 600 and hexchat.nickcmp(sheeple.nick, hexchat.get_info('nick')) != 0:
            for DVDs in nOgAnOo:
                if hexchat.nickcmp(sheeple.nick, DVDs) == 0:
                    exposed = True
            if exposed == False:
                vaccinatedPeople.append(sheeple.nick)
    return vaccinatedPeople

def noJewsInWTCon911(cheney, iraqWar):
    for idx, oilProfits in enumerate(iraqWar):
        if hexchat.nickcmp(cheney, oilProfits) == 0:
            del iraqWar[idx]
            break
    return iraqWar
            
def NSAspying(word, word_eol, userdata):
    status = hexchat.get_pluginpref('soakbot')
    if status == 'yes':
        puppetLeader = hexchat.get_info('nick')
        WTC = hexchat.get_info('channel')
        if word[0] == 'Doger':
            if word[1].split(' ')[0] == 'Such' and word[1].split(' ')[6] == puppetLeader + '!':
                bribeAmount = int(word[1].split(' ')[4][1:])
                towers = noJewsInWTCon911(billGates, censusData())
                temperature = bribeAmount//len(towers)
                if temperature < 10:
                    hexchat.command('say JET FUEL CAN\'T MELT STEEL BEAMS (secretly returning airplanes)')
                    hexchat.command('msg Doger tip %s %s' % (word[1].split(' ')[1], bribeAmount))
                else:
                    hexchat.command('say %s is melting %s steel beams with Ɖ%s (or is s/he?): %s' % (word[1].split(' ')[1], len(towers), temperature, ', '.join(towers)))
                    hexchat.command('msg Doger mtip %s %s' % ((' %s ' % str(temperature)).join(towers), temperature))
        elif word[1].lower() == '!active':
            hexchat.command('say The all-seeing eye sees %s meltable steel beams. Only steel beams identified with thermite are included.' % len(noJewsInWTCon911(word[0], censusData())))
    return hexchat.EAT_PLUGIN

def enablesoak(word, word_eol, userdata):
    hexchat.set_pluginpref('soakbot', 'yes')
    print('soak enabled')
    return hexchat.EAT_ALL
    
def disablesoak(word, word_eol, userdata):
    hexchat.set_pluginpref('soakbot', 'no')
    print('soak disabled >:')
    return hexchat.EAT_ALL

hexchat.hook_command('enablesoak', enablesoak, help='/enablesoak turns soak on')
hexchat.hook_command('disablesoak', disablesoak, help='/disablesoak turns soak off')

hexchat.hook_print('Channel Message', NSAspying)
hexchat.hook_print('Channel Msg Hilight', NSAspying)

def nwo_unloaded(userdata):
    hexchat.set_pluginpref('soakbot', 'no')
    hexchat.emit_print('Notice', '', '%s v%s by %s unloaded' % (__module_name__, __module_version__, __module_author__))
    return hexchat.EAT_ALL
hexchat.emit_print('Notice', '', '%s v%s by %s loaded' % (__module_name__, __module_version__, __module_author__))
hexchat.hook_unload(nwo_unloaded)
