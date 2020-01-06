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

class Application(tk.Frame):
    def __init__(self, master=None):
        print('=======================')
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

        if not os.path.exists('saskin.cfg'):
            path_setup(None)
        else:
            config = configparser.RawConfigParser()
            config.read('saskin.cfg')
            self.search_path = config['SuddenAttack']['PATH']
            self.path_search['text'] = config['SuddenAttack']['PATH']
            self.install['state'] = 'normal'
            self.install_test_button['state'] = 'normal'
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

        self.install_test_button = tk.Button(root, text='설치 (테스트용)', command=self.thread_install_test, state='disabled')
        self.install_test_button.place(x=400, y=30)

        self.install = tk.Button(root, text='설치', command=self.install)
        self.install.place(x=400, y=2)

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

        self.map_supply_checked = tk.IntVar()

        self.map_supply_group = LabelFrame(self.map_tab, text='Supply Base', width=200, height=4)
        self.map_supply_group.place(x=8, y=5)
        self.map_tab_chkbtn1 = tk.Radiobutton(self.map_supply_group, text='화이트 스킨', value=1, variable=self.map_supply_checked)
        self.map_tab_chkbtn1.pack(side='left', anchor='nw')
        self.map_tab_chkbtn2 = tk.Radiobutton(self.map_supply_group, text='하이터빅터', value=2, variable=self.map_supply_checked)
        self.map_tab_chkbtn2.pack(side='left', anchor='nw')

    def thread_path_search(self):
        threading.Thread(target=self.path_test).start()

    def path_test(self):
        # test exe
        # endpoint = 'py.exe'
        # endpoint = 'AuthHost.exe'

        # real suddenattack exe
        endpoint = 'ghsalncr.exe'
        cnt = 0
        search = False
        paths = []
        for i in range(ord('A'), ord('Z') + 1):
            paths.append(chr(i) + ':\\')

        for path in paths:
            cnt += 1
            for root, dir, files in os.walk(path):
                dir[:] = [dir for dir in dir if dir != 'Windows']
                dir[:] = [dir for dir in dir if dir != 'Program Files']
                dir[:] = [dir for dir in dir if dir != 'Program Files (x86)']
                dir[:] = [dir for dir in dir if dir != 'ProgramData']
                dir[:] = [dir for dir in dir if dir != 'PerfLogs']
                dir[:] = [dir for dir in dir if dir != '$Recycle.Bin']
                dir[:] = [dir for dir in dir if dir != 'Users']

                print(root)
                self.progress_text['text'] = root

                if endpoint in files:
                    self.search_path = root
                    search = True

        if not search:
            self.path_search['text'] = '경로를 찾을 수 없습니다.'
        else:
            self.install['state'] = 'normal'
            self.install_test_button['state'] = 'normal'
            self.path_search['text'] = self.search_path
            self.progress_text['text'] = '서든어택 경로를 찾았습니다.'
            path_setup(self.search_path)

    def thread_install_test(self):
        threading.Thread(target=self.download).start()

    def download(self):
        a = self.search_path + '\\test.zip'
        b = self.search_path
        self.progress_text['text'] = '다운로드를 시작했습니다.'

        url = 'https://box.team-crescendo.me/cloud/index.php/s/MdKPZpzSWbnHABa/download'
        name = self.search_path + '\\test.zip'

        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        t = tqdm(total=total_size, unit='iB', unit_scale=True)
        with open(name, 'wb') as f:
            for data in response.iter_content(block_size):
                self.progress_text['text'] = t
                t.update(len(data))
                f.write(data)
        t.close()

        self.progress_text['text'] = '압축 해제중입니다.'
        unzip(a, b)
        os.remove(self.search_path + '\\test.zip')
        self.progress_text['text'] = '스킨 설치가 완료되었습니다.'

    def install(self):
        print(self.map_supply_checked.get())

    def self_dir_search(self):
        dir = filedialog.askdirectory(title='Browse SuddenAttack Folder')
        self.install['state'] = 'normal'
        self.install_test_button['state'] = 'normal'
        self.search_path = dir
        self.path_search['text'] = dir
        self.progress_text['text'] = '서든어택 경로를 불러왔습니다.'
        path_setup(dir)

if __name__ == "__main__":
    root = tk.Tk()
    root.title('SuddenAttack Easy Skin Installer v' + VERSION)
    root.geometry('500x300+0+50')
    root.resizable(False, False)
    root.maxsize(width=500, height=320)
    root.minsize(width=500, height=320)
    app = Application(master=root)
    app.mainloop()
