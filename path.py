import configparser

# MAP_SUPPLYS: default, white, victor, shadow_remove, W-skin
SUPPLYS = ['oFSA4KKC9oSn9wH', 'ke2eTQSjmXWrq8t', 'sGbDLSWboM9aLGF', '7dKpcLTsgpyGTQ8', 'oFSA4KKC9oSn9wH']

# WEAPON_FLU
FLU = ['idS4mZN2HefApxE']

# SCOPE: default, rainbow, black_dragon, full
SCOPES = ['QYDCAn2BxwNEWrH', 'itg8MoPnxyWDy5Z', '5zmEGCfjXRM3Fg4', 'xdyMDc6dxNCQSgL']

def download(section, value):
    value -= 1

    if section == 'map_supply':
        return SUPPLYS[value]
    elif section == 'weapon_flu':
        return FLU[value]
    elif section == 'scope':
        return SCOPES[value]

def setup(path):
    config = configparser.RawConfigParser()
    if not path:
        config.add_section('SuddenAttack')
        config.set('SuddenAttack', 'PATH', None)
    else:
        config.read('saskin.cfg')
        config['SuddenAttack']['PATH'] = path

    config.write(open('saskin.cfg', 'w'))