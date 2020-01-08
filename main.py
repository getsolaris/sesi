#-*-coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.ttk import *
import os
import zipfile
import requests
import configparser
import time
import threading
from tqdm import tqdm

VERSION = '0.1'

def unzip(source_file, dest_path):
    with zipfile.ZipFile(source_file, 'r') as zf:
        zf.extractall(path=dest_path)
        zf.close()

def path_setup(path):
    config = configparser.RawConfigParser()
    if not path:
        config.add_section('SuddenAttack')
        config.set('SuddenAttack', 'PATH', None)
    else:
        config.read('saskin.cfg')
        config['SuddenAttack']['PATH'] = path

    config.write(open('saskin.cfg', 'w'))

def url_path(section, value):
    value -= 1
    if section == 'map_supply':
        # default, white, victor, shadow_remove, W-skin
        supplys = ['Gb86nPaGdkgnMBT', 'YP7WmfzNC4Zb7g8', '3XePbbg8ePbBaqZ', 'cbf6o4PJ24HXTim', 'coKqpJ4GDBDqFdC']
        return supplys[value]
    elif section == 'weapon_flu':
        weapon_flus = ['BEofT6qfotczGEr']
        return weapon_flus[value]
    elif section == 'scope':
        # default, rainbow, black_dragon, full
        scopes = ['iwtdCtg5cLpdAE4', 'YHofryk7NAX6HJf', 'biKoLnBTL9dmfdw', 'itC8tSF92TqSzFX']
        return scopes[value]

class Application(tk.Frame):
    def __init__(self, master=None):
        print('======================= Running')
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

        if not os.path.exists('saskin.cfg'):
            path_setup(None)
        else:
            config = configparser.RawConfigParser()
            config.read('saskin.cfg')
            if config['SuddenAttack']['PATH'] == 'None': # None 일 경우
                self.progress_text['text'] = 'saskin.cfg 파일에서 서든어택 경로를 불러오지 못했습니다.'
                time.sleep(1)
                self.progress_text['text'] = '서든어택 경로를 탐색해주세요.'
            else:
                self.search_path = config['SuddenAttack']['PATH']
                self.path_search['text'] = config['SuddenAttack']['PATH']
                self.install['state'] = 'normal'
                self.progress_text['text'] = 'saskin.cfg 파일에서 서든어택 경로를 불러왔습니다.'

    def create_widgets(self):
        self.progress_text_label = tk.Label(root, text='Log >')
        self.progress_text_label.place(x=13, y=290)

        self.progress_text = tk.Label(root, text='')
        self.progress_text.place(x=50, y=290)

        self.menubar = tk.Menu(root)
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label='서든어택 경로 탐색')
        self.help_menu.add_command(label='업데이트 로그')
        self.account_menu = tk.Menu(self.menubar, tearoff=0)
        self.account_menu.add_command(label='로그인')
        self.account_menu.add_command(label='회원가입')
        self.my_files_menu = tk.Menu(self.menubar, tearoff=0)
        self.my_files_menu.add_command(label='사용방법')
        self.menubar.add_cascade(label='Account', menu=self.account_menu)
        self.menubar.add_cascade(label='My Files', menu=self.my_files_menu)
        self.menubar.add_cascade(label='Help', menu=self.help_menu)
        root.config(menu=self.menubar)

        self.path = tk.Button(root, text='경로 자동검색', command=self.thread_path_search)
        self.path.place(x=10, y=10)

        self.path_search_label = tk.Label(root, text='\'경로 자동검색\' 버튼을 클릭하면 서든어택 경로를 자동으로 탐색합니다.')
        self.path_search_label.place(x=10, y=36)

        self.path_search = tk.Label(root, text='경로')
        self.path_search.place(x=140, y=13)

        self.dir_search = tk.Button(root, text='검색', command=self.self_dir_search)
        self.dir_search.place(x=100, y=10)

        self.install = tk.Button(root, text='설치', command=self.thread_install)
        self.install.place(x=455, y=10)

        self.note = Notebook(root)
        self.map_tab = Frame(self.note, width=480, height=200)
        self.weapon_tab = Frame(self.note, width=480, height=200)
        self.scope_tab = Frame(self.note, width=480, height=200)
        self.ui_tab = Frame(self.note, width=480, height=200)
        self.win_lose_tab = Frame(self.note, width=480, height=200)
        self.my_files = Frame(self.note, width=480, height=200)
        self.note.add(self.map_tab, text="Maps")
        self.note.add(self.weapon_tab, text="Weapons")
        self.note.add(self.scope_tab, text="Scope")
        self.note.add(self.ui_tab, text="UI")
        self.note.add(self.win_lose_tab, text="Win/Lose")
        self.note.add(self.my_files, text="My Files")
        self.note.place(x=10, y=60)

        # ----------------------- Radio Button Setup tkinter
        self.map_supply_checked = tk.IntVar()
        self.weapon_1_checked = tk.IntVar()
        self.scope_checked = tk.IntVar()

        # ----------------------- Map
        self.map_supply_group = LabelFrame(self.map_tab, text='Supply Base', width=200, height=4)
        self.map_supply_group.place(x=8, y=5)
        self.map_tab_chkbtn1 = tk.Radiobutton(self.map_supply_group, text='원본', value=1,
                                              variable=self.map_supply_checked)
        self.map_tab_chkbtn1.pack(side='left', anchor='nw')
        self.map_tab_chkbtn2 = tk.Radiobutton(self.map_supply_group, text='화이트 스킨', value=2,
                                              variable=self.map_supply_checked)
        self.map_tab_chkbtn2.pack(side='left', anchor='nw')
        self.map_tab_chkbtn3 = tk.Radiobutton(self.map_supply_group, text='하이터빅터', value=3,
                                              variable=self.map_supply_checked)
        self.map_tab_chkbtn3.pack(side='left', anchor='nw')
        self.map_tab_chkbtn4 = tk.Radiobutton(self.map_supply_group, text='그림자제거', value=4,
                                              variable=self.map_supply_checked)
        self.map_tab_chkbtn4.pack(side='left', anchor='nw')
        self.map_tab_chkbtn5 = tk.Radiobutton(self.map_supply_group, text='W스킨', value=5,
                                              variable=self.map_supply_checked)
        self.map_tab_chkbtn5.pack(side='left', anchor='nw')

        # ----------------------- Weapon
        self.weapon_group1 = LabelFrame(self.weapon_tab, text='Weapon 1', width=200, height=4)
        self.weapon_group1.place(x=8, y=5)
        self.weapon_tab1_chkbtn1 = tk.Radiobutton(self.weapon_group1, text='형광스킨 (20.01.02)', value=1,
                                              variable=self.weapon_1_checked)
        self.weapon_tab1_chkbtn1.pack(side='left', anchor='nw')

        # ----------------------- Scope
        self.scope_group = LabelFrame(self.scope_tab, text='Scopes', width=200, height=4)
        self.scope_group.place(x=8, y=5)
        self.scope_tab_chkbtn1 = tk.Radiobutton(self.scope_group, text='원본', value=1,
                                                  variable=self.scope_checked)
        self.scope_tab_chkbtn1.pack(side='left', anchor='nw')
        self.scope_tab_chkbtn2 = tk.Radiobutton(self.scope_group, text='무지개', value=2,
                                                  variable=self.scope_checked)
        self.scope_tab_chkbtn2.pack(side='left', anchor='nw')
        self.scope_tab_chkbtn3 = tk.Radiobutton(self.scope_group, text='흑룡', value=3,
                                                  variable=self.scope_checked)
        self.scope_tab_chkbtn3.pack(side='left', anchor='nw')
        self.scope_tab_chkbtn4 = tk.Radiobutton(self.scope_group, text='전체화면', value=4,
                                                  variable=self.scope_checked)
        self.scope_tab_chkbtn4.pack(side='left', anchor='nw')

    def thread_path_search(self):
        threading.Thread(target=self.path_test).start()

    def path_test(self):
        # suddenattack process name
        endpoint = 'ghsalncr.exe'
        search = False
        paths = []

        # A-Z Drive Search
        for i in range(ord('A'), ord('Z') + 1):
            paths.append(chr(i) + ':\\')

        for path in paths:
            for root, dir, files in os.walk(path):
                dir[:] = [dir for dir in dir if dir != 'Windows']
                dir[:] = [dir for dir in dir if dir != 'Program Files']
                dir[:] = [dir for dir in dir if dir != 'Program Files (x86)']
                dir[:] = [dir for dir in dir if dir != 'ProgramData']
                dir[:] = [dir for dir in dir if dir != 'PerfLogs']
                dir[:] = [dir for dir in dir if dir != '$Recycle.Bin']
                dir[:] = [dir for dir in dir if dir != 'Users']

                self.progress_text['text'] = root

                if endpoint in files:
                    self.search_path = root
                    search = True

        if not search:
            self.path_search['text'] = '경로를 찾을 수 없습니다.'
        else:
            self.install['state'] = 'normal'
            self.path_search['text'] = self.search_path
            self.progress_text['text'] = '서든어택 경로를 찾았습니다.'
            path_setup(self.search_path)

    def thread_install(self):
        threading.Thread(target=self.download).start()

    def download(self):
        self.progress_text['text'] = '스킨정보를 읽어들이고 있습니다..'
        checked = False

        if self.map_supply_checked.get() > 0:
            time.sleep(3)
            url = url_path('map_supply', self.map_supply_checked.get()) + '/download'
            checked = True
            self.download_process('보급창고', url, self.search_path + '\\map_supply.zip', self.search_path + '\\game\\sa_tex')

        if self.weapon_1_checked.get() > 0:
            time.sleep(3)
            url = url_path('weapon_flu', self.weapon_1_checked.get()) + '/download'
            checked = True
            self.download_process('형광', url, self.search_path + '\\weapon_flu.zip', self.search_path + '\\game')

        if self.scope_checked.get() > 0:
            time.sleep(3)
            url = url_path('scope', self.scope_checked.get()) + '/download'
            checked = True
            self.download_process('스코프', url, self.search_path + '\\scope.zip', self.search_path + '\\game\\sa_interface\\hud\\scope')

        if not checked:
            self.progress_text['text'] = '스킨을 선택해주세요. (선택 안되어있음)'
            return

        self.map_supply_checked.set(None)
        self.weapon_1_checked.set(None)
        self.scope_checked.set(None)


    def download_process(self, section, url, download_path, target):
        url = 'https://box.team-crescendo.me/cloud/index.php/s/' + url
        self.progress_text['text'] = section + ' 스킨 다운로드를 시작합니다.'

        time.sleep(1)

        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        t = tqdm(total=total_size, unit='iB', unit_scale=True)
        with open(download_path, 'wb') as f:
            for data in response.iter_content(block_size):
                self.progress_text['text'] = t
                t.update(len(data))
                f.write(data)
        t.close()
        f.close()
        response.close()

        self.progress_text['text'] = '압축 해제중입니다.'
        unzip(download_path, target)
        os.remove(download_path)
        self.progress_text['text'] = section + ' 스킨 설치가 완료되었습니다.'

    def self_dir_search(self):
        self.dir = filedialog.askdirectory(title='Browse SuddenAttack Folder')
        self.install['state'] = 'normal'
        self.search_path = self.dir
        self.path_search['text'] = self.dir
        self.progress_text['text'] = '서든어택 경로를 불러왔습니다.'
        path_setup(self.dir)

if __name__ == "__main__":
    root = tk.Tk()
    root.title('SuddenAttack Easy Skin Installer v' + VERSION)
    root.geometry('500x300+0+50')
    root.resizable(False, False)
    root.maxsize(width=500, height=320)
    root.minsize(width=500, height=320)
    app = Application(master=root)
    app.mainloop()
