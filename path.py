import configparser, asyncio, aiohttp, json

SKIN_JSON_PATH = 'https://raw.githubusercontent.com/getsolaris/sesm/master/skin_path.json'

skin_data = None # SKIN PATH JSON DICT

async def skin_path_download():
    async with aiohttp.ClientSession() as session:
        async with session.get(SKIN_JSON_PATH) as res:
            return await res.text()

if not skin_data:
    loop = asyncio.get_event_loop()
    skin_data = json.loads(loop.run_until_complete(skin_path_download()))
    print('======================= Load skin path json')
    print(skin_data)

def download(section, value):
    value -= 1

    return skin_data[section][value]

def setup(path):
    config = configparser.RawConfigParser()
    if not path:
        config.add_section('SuddenAttack')
        config.set('SuddenAttack', 'PATH', None)
    else:
        config.read('saskin.cfg')
        config['SuddenAttack']['PATH'] = path

    config.write(open('saskin.cfg', 'w'))
