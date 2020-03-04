import configparser

# MAP_SUPPLYS: default, white, victor, shadow_remove, W-skin
SUPPLYS = ['AjswetwKdj44zye', 'ke2eTQSjmXWrq8t', 'sGbDLSWboM9aLGF', '7dKpcLTsgpyGTQ8', '9CL2CqsHP2tMr99']

# WEAPON_FLU: default, flu
FLU = ['tkqz8tE9q97b93o', 'KNx5sfYfzfFfXmQ']

# SKYS: default, 3 supply high bomb, gray, night
SKYS = ['TSrT8W2nFpfs2TH', 'aMzbxLw2Fsi3CM4', '6fwBP9XKqKf7353', 'zr9M98anSTnzTrG']

# WIRES: default, white, trans
WIRES = ['QN5nNEdEwGidzyo', 'aYfecKG5NrgfYQL', 'CmmBKaqG5EWT7Jt']

# SCOPE: default, rainbow, black_dragon, full
SCOPES = ['QYDCAn2BxwNEWrH', 'itg8MoPnxyWDy5Z', '5zmEGCfjXRM3Fg4', 'xdyMDc6dxNCQSgL']

# DRAGON: default, shadow_remove, white
DRAGONS = ['83TbHkXSL3jY2wp', 'oQp8TYp7FAdfjkj', '8p34GSjAHmDa5Ca']

# DUOS: default, white
DUOS = ['7qSn5PSJzE76iR9', 'N4c8cKgcRQDXTmL']

# CROSS COUNTERS: default, renew
CROSS_COUNTERS = ['dfAeqRdJwH2rHPa', 'EBxgzDMEHPE4PbB']

# CROSS PORTS: default, renew
CROSS_PORTS = ['X2skLzg6EJoPGKo']

# GOLDEN EYES: default, white
GOLDEN_EYES = ['JCbYWig46GPy85N', 'HYXDGCKjtmScdJs']

# CLUB NIGHT: default, renew
CLUB_NIGHTS = ['i5WHkiaQe83RMm9']

# PROVENCE: default, renew
PROVENCES = ['RetX4K4L6ZPbwzG', 'F877tqD4G5yngR3']

# TRIO: default, renew
TRIOS = ['EtFnjxmR3HgrsrC', 'DGnJFeJw9SXDRWF']

def download(section, value):
    value -= 1

    if section == 'map_supply':
        return SUPPLYS[value]
    elif section == 'weapon_flu':
        return FLU[value]
    elif section == 'map_dragon':
        return DRAGONS[value]
    elif section == 'map_duo':
        return DUOS[value]
    elif section == 'etc_scope':
        return SCOPES[value]
    elif section == 'map_crosscounter':
        return CROSS_COUNTERS[value]
    elif section == 'map_crossport':
        return CROSS_PORTS[value]
    elif section == 'map_goldeneye':
        return GOLDEN_EYES[value]
    elif section == 'map_clubnight':
        return CLUB_NIGHTS[value]
    elif section == 'map_provence':
        return PROVENCES[value]
    elif section == 'map_trio':
        return TRIOS[value]
    elif section == 'etc_sky':
        return SKYS[value]
    elif section == 'etc_wire':
        return WIRES[value]

def setup(path):
    config = configparser.RawConfigParser()
    if not path:
        config.add_section('SuddenAttack')
        config.set('SuddenAttack', 'PATH', None)
    else:
        config.read('saskin.cfg')
        config['SuddenAttack']['PATH'] = path

    config.write(open('saskin.cfg', 'w'))