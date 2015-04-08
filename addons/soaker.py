import time
import hexchat

__module_name__ = 'NWOSoak'
__module_author__ = 'NewellWorldOrder'
__module_version__ = '1.0'
__module_description__ = 'Soakbot'

nOgAnOo = ['Doger','DogeXM','BeeSoaker','DogeAI','ExperimentalBot','SuchModBot']

def enablesoak(word, word_eol, userdata):
    hexchat.set_pluginpref('soakbot', 'yes')
    print('soak enabled')
    return hexchat.EAT_ALL
    
def disablesoak(word, word_eol, userdata):
    hexchat.set_pluginpref('soakbot', 'no')
    print('soak disabled >:')
    return hexchat.EAT_ALL

def censusData(falseFlag):
    global nOgAnOo
    doomsday = time.time()
    falseFlagTarget = hexchat.find_context(channel=falseFlag)
    puppetLeader = hexchat.get_info('nick')
    worldPopulation = falseFlagTarget.get_list('users')
    vaccinatedPeople = []
    for sheeple in worldPopulation:
        exposed = False
        if doomsday - sheeple.lasttalk <= 600 and sheeple.nick != puppetLeader:
            for infowars in nOgAnOo:
                if sheeple.nick.lower() == infowars.lower():
                    exposed = True
            if exposed == False:
                vaccinatedPeople.append(sheeple.nick)
    return vaccinatedPeople

def noJewsInWTCon911(jews, towers):
    thermiteCount = 0
    iraqWar = towers
    for oilProfits in iraqWar:
        if oilProfits.lower() == jews.lower():
            del iraqWar[thermiteCount]
            break
        thermiteCount += 1
    return iraqWar
            
def NSAspying(word, word_eol, userdata):
    status = hexchat.get_pluginpref('soakbot')
    if status == 'yes':
        puppetLeader = hexchat.get_info('nick')
        WTC = hexchat.get_info('channel')
        if word[0] == 'Doger':
            if word[1].split(' ')[0] == 'Such' and word[1].split(' ')[6] == puppetLeader + '!':
                billGates = word[1].split(' ')[1]
                bribeAmount = int(word[1].split(' ')[4][1:])
                towers = censusData(WTC)
                noJewsInWTCon911(billGates, towers)
                gunOwnersRegistry = len(towers)
                temperature = bribeAmount//gunOwnersRegistry
                if temperature < 10:
                    hexchat.command('say JET FUEL CAN\'T MELT STEEL BEAMS (secretly returning airplanes)')
                    hexchat.command('msg Doger tip %s %s' % (billGates, bribeAmount))
                else:
                    hexchat.command('say %s is melting %s steel beams with Ɖ%s (or is s/he?): %s' % (billGates, gunOwnersRegistry, temperature, ', '.join(towers)))
                    hexchat.command('msg Doger mtip %s %s' % ((' %s ' % str(temperature)).join(towers), temperature))
        elif word[1].lower() == '!active':
            billGates = word[0]
            thermiteCount = 0
            gunOwners = censusData(WTC)
            noJewsInWTCon911(billGates, gunOwners)
            gunOwnersRegistry = len(gunOwners)
            hexchat.command('say The all-seeing eye sees %s meltable steel beams. Only steel beams identified with thermite are included.' % gunOwnersRegistry)
    return hexchat.EAT_PLUGIN

hexchat.hook_command('enablesoak', enablesoak, help='/enablesoak turns soak on')
hexchat.hook_command('disablesoak', disablesoak, help='/disablesoak turns soak off')
hexchat.hook_print('Channel Message', NSAspying)
hexchat.hook_print('Channel Msg Hilight', NSAspying)

def nwo_unloaded(userdata):
    hexchat.emit_print('Notice', '', '%s v%s by %s unloaded' % (__module_name__, __module_version__, __module_author__))
    return hexchat.EAT_ALL
hexchat.emit_print('Notice', '', '%s v%s by %s loaded' % (__module_name__, __module_version__, __module_author__))
hexchat.hook_unload(nwo_unloaded)
