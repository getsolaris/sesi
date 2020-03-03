#-*-coding: utf-8 -*-

# librarys
import os, time, tqdm, requests, threading, webbrowser, configparser

# tkinter
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font
from tkinter import filedialog
from tkinter.ttk import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from ttkthemes import ThemedStyle

# module
import path as skin, common, version_crawler as vc

# constant
CONTAINER_WIDTH = 500
CONTAINER_HEIGHT = 318
VERSION = '0.0.7'
STORAGE_URL = 'https://box.minemy.me/cloud/index.php/s/'
SUDDENATTACK_PROCESS = 'ghsalncr.exe'
BACKGROUND_COLOR = '#F5F6F8'

class Application(tk.Frame):
    def __init__(self, master=None):
        print('======================= Running')
        super().__init__(master)
        style = ThemedStyle(master)
        style.set_theme('arc')
        style.theme_use('arc')
        self.master = master
        self.pack()
        self.create_widgets()

        # 개발PC 인 경우 업데이트를 체크하지 않음
        if os.environ['LOGONSERVER'] != r'\\KEVINCC38':
            self.version_updater()

        if not os.path.exists('saskin.cfg'):
            skin.setup(None)
        else:
            config = configparser.RawConfigParser()
            config.read('saskin.cfg')
            if config['SuddenAttack']['PATH'] == 'None': # None 일 경우
                self.progress_text['text'] = 'saskin.cfg 파일에서 서든어택 경로를 불러오지 못했습니다.'
                time.sleep(1)
                self.progress_text['text'] = '서든어택 경로를 탐색해주세요.'
                self.install['state'] = 'disabled'
            else:
                self.search_path = config['SuddenAttack']['PATH']
                self.path_search['text'] = config['SuddenAttack']['PATH']
                self.install['state'] = 'normal'
                self.progress_text['text'] = 'saskin.cfg 파일에서 서든어택 경로를 불러왔습니다.'

    def version_updater(self):
        recency = vc.release_rss_crawl(VERSION)
        print('version recency: ', recency[0])

        if not recency[0]:
            message_box = tk.messagebox.askquestion('새로운 버전이 나왔습니다.', '파일 다운로드를 진행하시겠습니까 ?',
                                      icon='warning')

            if (message_box == 'yes'):
                webbrowser.open(recency[1][0][1])
                root.destroy()

    def create_frame(self, title, size):
        self.sub_frame = tk.Toplevel()
        self.sub_frame.geometry(size + '+0+50')
        self.sub_frame.title(title)
        self.sub_frame.resizable(False, False)
        self.sub_frame.configure(background=BACKGROUND_COLOR)

    def help_sa_path_search(self):
        tk.messagebox.showinfo('서든어택 경로 탐색', '메인화면의 \'경로 자동검색\' 버튼을 클릭하시면' + "\n" 
                                                     'A~Z 드라이브를 탐색하여 서든어택 경로를 자동 검색합니다.\n')

    def help_update_log(self):
        self.create_frame('업데이트 로그', '500x300')

        releases = vc.version_content()

        version_style = tkinter.font.Font(size=14, weight='bold')
        for release in releases:
            self.version = ttk.Label(self.sub_frame, text='v' + release[0], justify='left', font=version_style)
            self.version.pack(anchor='w')

            self.content = ttk.Label(self.sub_frame, text=release[1] + '\n', justify='left')
            self.content.pack(anchor='w')

    def help_develop(self):
        tk.messagebox.showinfo('제작자', '피시방에서 서든을 주로 하는 개발자가 개발했습니다.\n이메일: saskinio@naver.com')

    def help_opensource(self):
        tk.messagebox.showinfo('오픈소스 안내', 'SuddenAttack Easy Skin Manager는 오픈소스로 공개 되어있는 프로그램입니다.\n'
                                          '언어는 Python 으로 개발 되었고, Pyinstaller 로 패키징(.py to .exe) 합니다.\n'
                                          '개발에 참여 하고 싶으시거나, 궁금하신점이 있으신 사용자분들께서는 아래의 이메일로 연락'
                                          '주시기 바랍니다.\nsaskinio@naver.com')

    def create_widgets(self):
        self.progress_text_label = ttk.Label(root, text='Log >')
        self.progress_text_label.place(x=13, y=292.5)

        self.progress_text = ttk.Label(root, text='')
        self.progress_text.place(x=50, y=294)

        self.menubar = tk.Menu(root)
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label='서든어택 경로 탐색', command=self.help_sa_path_search)
        self.help_menu.add_command(label='업데이트 로그', command=self.help_update_log)
        self.help_menu.add_command(label='제작자', command=self.help_develop)
        self.help_menu.add_command(label='오픈소스', command=self.help_opensource)
        self.account_menu = tk.Menu(self.menubar, tearoff=0)
        self.account_menu.add_command(label='로그인 (개발중)', state='disabled')
        self.account_menu.add_command(label='회원가입 (개발중)', state='disabled')
        self.my_files_menu = tk.Menu(self.menubar, tearoff=0)
        self.my_files_menu.add_command(label='사용방법 (개발중)', state='disabled')
        self.menubar.add_cascade(label='Account', menu=self.account_menu)
        self.menubar.add_cascade(label='My Files', menu=self.my_files_menu)
        self.menubar.add_cascade(label='Help', menu=self.help_menu)
        root.config(menu=self.menubar)

        self.path = ttk.Button(root, text='경로 자동검색', command=self.thread_path_search)
        self.path.place(x=10, y=10)

        self.path_search_label = ttk.Label(root, text='\'경로 자동검색\' 버튼을 클릭하면 서든어택 경로를 자동으로 탐색합니다.')
        self.path_search_label.place(x=10, y=40)
        common.create_tooltip(self.path, text='서든어택 경로를 자동검색합니다.')

        self.path_search = ttk.Label(root, text='')
        self.path_search.place(x=165, y=16.4)

        self.dir_search = ttk.Button(root, text='검색', command=self.self_dir_search, width=4)
        self.dir_search.place(x=111, y=10)
        common.create_tooltip(self.dir_search, text='\'경로 자동검색\' 으로 찾지 못할 경우, 직접 서든어택 경로를 선택해주세요.')

        self.install = ttk.Button(root, text='설치', command=self.thread_install, width=4)
        self.install.place(x=437, y=10)

        self.note = ttk.Notebook(root)
        self.map_tab = ttk.Frame(self.note, width=480, height=200)
        self.weapon_tab = ttk.Frame(self.note, width=480, height=200)
        self.scope_tab = ttk.Frame(self.note, width=480, height=200)
        self.ui_tab = ttk.Frame(self.note, width=480, height=200)
        self.win_lose_tab = ttk.Frame(self.note, width=480, height=200)
        self.my_files = ttk.Frame(self.note, width=480, height=200)
        self.note.add(self.map_tab, text="Maps")
        self.note.add(self.weapon_tab, text="Weapons")
        self.note.add(self.scope_tab, text="Scope")
        # self.note.add(self.ui_tab, text="UI")
        # self.note.add(self.win_lose_tab, text="Win/Lose")
        # self.note.add(self.my_files, text="My Files")
        self.note.place(x=10, y=60)

        # ----------------------- Radio Button Setup tkinter
        self.map_supply_checked = tk.IntVar()
        self.map_dragon_checked = tk.IntVar()
        self.map_duo_checked = tk.IntVar()
        self.map_crosscounter_checked = tk.IntVar()
        self.map_crossport_checked = tk.IntVar()
        self.map_goldeneye_checked = tk.IntVar()
        self.map_clubnight_checked = tk.IntVar()
        self.map_provence_checked = tk.IntVar()
        self.map_trio_checked = tk.IntVar()
        self.weapon_1_checked = tk.IntVar()
        self.scope_checked = tk.IntVar()

        # ----------------------- Map
        self.map_supply_group = ttk.Labelframe(self.map_tab, text='보급창고', width=200, height=4)
        self.map_supply_group.place(x=8, y=5)
        self.map_tab_chkbtn1 = ttk.Radiobutton(self.map_supply_group, text='원본', value=1,
                                              variable=self.map_supply_checked)
        self.map_tab_chkbtn1.pack(side='left', anchor='nw')
        self.map_tab_chkbtn2 = ttk.Radiobutton(self.map_supply_group, text='화이트 스킨', value=2,
                                              variable=self.map_supply_checked)
        self.map_tab_chkbtn2.pack(side='left', anchor='nw')
        self.map_tab_chkbtn3 = ttk.Radiobutton(self.map_supply_group, text='하이터빅터', value=3,
                                              variable=self.map_supply_checked)
        self.map_tab_chkbtn3.pack(side='left', anchor='nw')
        self.map_tab_chkbtn4 = ttk.Radiobutton(self.map_supply_group, text='그림자제거', value=4,
                                              variable=self.map_supply_checked)
        self.map_tab_chkbtn4.pack(side='left', anchor='nw')
        self.map_tab_chkbtn5 = ttk.Radiobutton(self.map_supply_group, text='W스킨', value=5,
                                              variable=self.map_supply_checked)
        self.map_tab_chkbtn5.pack(side='left', anchor='nw')
        
        self.map_dragon_group = ttk.LabelFrame(self.map_tab, text='드래곤로드', width=200, height=4)
        self.map_dragon_group.place(x=8, y=50)
        self.map_tab_chkbtn1 = ttk.Radiobutton(self.map_dragon_group, text='원본', value=1,
                                              variable=self.map_dragon_checked)
        self.map_tab_chkbtn1.pack(side='left', anchor='nw')
        self.map_tab_chkbtn2 = ttk.Radiobutton(self.map_dragon_group, text='그림자제거', value=2,
                                              variable=self.map_dragon_checked)
        self.map_tab_chkbtn2.pack(side='left', anchor='nw')
        self.map_tab_chkbtn3 = ttk.Radiobutton(self.map_dragon_group, text='화이트 스킨', value=3,
                                              variable=self.map_dragon_checked)
        self.map_tab_chkbtn3.pack(side='left', anchor='nw')

        self.map_duo_group = ttk.LabelFrame(self.map_tab, text='듀오', width=200, height=4)
        self.map_duo_group.place(x=250, y=50)
        self.map_tab_chkbtn1 = ttk.Radiobutton(self.map_duo_group, text='원본', value=1,
                                              variable=self.map_duo_checked)
        self.map_tab_chkbtn1.pack(side='left', anchor='nw')
        self.map_tab_chkbtn2 = ttk.Radiobutton(self.map_duo_group, text='화이트 스킨', value=2,
                                              variable=self.map_duo_checked)
        self.map_tab_chkbtn2.pack(side='left', anchor='nw')

        self.map_crosscounter_group = ttk.LabelFrame(self.map_tab, text='크로스카운터', width=200, height=4)
        self.map_crosscounter_group.place(x=8, y=97)
        self.map_tab_chkbtn1 = ttk.Radiobutton(self.map_crosscounter_group, text='원본', value=1,
                                              variable=self.map_crosscounter_checked)
        self.map_tab_chkbtn1.pack(side='left', anchor='nw')
        self.map_tab_chkbtn2 = ttk.Radiobutton(self.map_crosscounter_group, text='화이트 스킨', value=2,
                                              variable=self.map_crosscounter_checked)
        self.map_tab_chkbtn2.pack(side='left', anchor='nw')

        # self.map_crossport_group = ttk.LabelFrame(self.map_tab, text='크로스포트', width=200, height=4)
        # self.map_crossport_group.place(x=8, y=97)
        # self.map_tab_chkbtn1 = ttk.Radiobutton(self.map_crossport_group, text='원본', value=1,
        #                                       variable=self.map_crossport_checked)
        # self.map_tab_chkbtn1.pack(side='left', anchor='nw')
        # self.map_tab_chkbtn2 = ttk.Radiobutton(self.map_crossport_group, text='스킨', value=2,
        #                                       variable=self.map_crossport_checked)
        # self.map_tab_chkbtn2.pack(side='left', anchor='nw')

        self.map_goldeneye_group = ttk.LabelFrame(self.map_tab, text='골든아이', width=200, height=4)
        self.map_goldeneye_group.place(x=160, y=97)
        self.map_tab_chkbtn1 = ttk.Radiobutton(self.map_goldeneye_group, text='원본', value=1,
                                              variable=self.map_goldeneye_checked)
        self.map_tab_chkbtn1.pack(side='left', anchor='nw')
        self.map_tab_chkbtn2 = ttk.Radiobutton(self.map_goldeneye_group, text='화이트 스킨', value=2,
                                              variable=self.map_goldeneye_checked)
        self.map_tab_chkbtn2.pack(side='left', anchor='nw')

        # self.map_clubnight_group = ttk.LabelFrame(self.map_tab, text='클럽나이트', width=200, height=4)
        # self.map_goldeneye_group.place(x=315, y=97)
        # self.map_tab_chkbtn1 = ttk.Radiobutton(self.map_clubnight_group, text='원본', value=1,
        #                                       variable=self.map_clubnight_checked)
        # self.map_tab_chkbtn1.pack(side='left', anchor='nw')
        # self.map_tab_chkbtn2 = ttk.Radiobutton(self.map_clubnight_group, text='스킨', value=2,
        #                                       variable=self.map_clubnight_checked)
        # self.map_tab_chkbtn2.pack(side='left', anchor='nw')

        self.map_provence_group = ttk.LabelFrame(self.map_tab, text='프로방스', width=200, height=4)
        self.map_provence_group.place(x=8, y=143)
        self.map_tab_chkbtn1 = ttk.Radiobutton(self.map_provence_group, text='원본', value=1,
                                              variable=self.map_provence_checked)
        self.map_tab_chkbtn1.pack(side='left', anchor='nw')
        self.map_tab_chkbtn2 = ttk.Radiobutton(self.map_provence_group, text='화이트 스킨', value=2,
                                              variable=self.map_provence_checked)
        self.map_tab_chkbtn2.pack(side='left', anchor='nw')

        self.map_trio_group = ttk.LabelFrame(self.map_tab, text='트리오', width=200, height=4)
        self.map_trio_group.place(x=160, y=143)
        self.map_tab_chkbtn1 = ttk.Radiobutton(self.map_trio_group, text='원본', value=1,
                                              variable=self.map_trio_checked)
        self.map_tab_chkbtn1.pack(side='left', anchor='nw')
        self.map_tab_chkbtn2 = ttk.Radiobutton(self.map_trio_group, text='화이트 스킨', value=2,
                                              variable=self.map_trio_checked)
        self.map_tab_chkbtn2.pack(side='left', anchor='nw')

        # ----------------------- Weapon
        self.weapon_group1 = ttk.LabelFrame(self.weapon_tab, text='Weapon 1', width=200, height=4)
        self.weapon_group1.place(x=8, y=5)
        self.weapon_tab1_chkbtn1 = ttk.Radiobutton(self.weapon_group1, text='형광스킨 (20.02.20)', value=1,
                                              variable=self.weapon_1_checked)
        self.weapon_tab1_chkbtn1.pack(side='left', anchor='nw')

        # ----------------------- Scope
        self.scope_group = ttk.LabelFrame(self.scope_tab, text='Scopes', width=200, height=4)
        self.scope_group.place(x=8, y=5)
        self.scope_tab_chkbtn1 = ttk.Radiobutton(self.scope_group, text='원본', value=1,
                                                  variable=self.scope_checked)
        self.scope_tab_chkbtn1.pack(side='left', anchor='nw')
        self.scope_tab_chkbtn2 = ttk.Radiobutton(self.scope_group, text='무지개', value=2,
                                                  variable=self.scope_checked)
        self.scope_tab_chkbtn2.pack(side='left', anchor='nw')
        self.scope_tab_chkbtn3 = ttk.Radiobutton(self.scope_group, text='흑룡', value=3,
                                                  variable=self.scope_checked)
        self.scope_tab_chkbtn3.pack(side='left', anchor='nw')
        self.scope_tab_chkbtn4 = ttk.Radiobutton(self.scope_group, text='전체화면', value=4,
                                                  variable=self.scope_checked)
        self.scope_tab_chkbtn4.pack(side='left', anchor='nw')

    def thread_path_search(self):
        threading.Thread(target=self.search_path).start()

    def search_path(self):
        search = False
        expect = False
        expect_paths = []

        for i in range(ord('C'), ord('Z') + 1):
            expect_paths.append(chr(i) + ':\\Nexon\\SuddenAttack')
            expect_paths.append(chr(i) + ':\\Game\\SuddenAttack')
            expect_paths.append(chr(i) + ':\\Game\\Nexon\\SuddenAttack')

        for path in expect_paths:
            if os.path.isdir(path):
                expect = True
                search = True
                self.search_path = path
                break

        if not expect:
            paths = []

            # A-Z Drive Search
            for i in range(ord('C'), ord('Z') + 1):
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

                    if SUDDENATTACK_PROCESS in files:
                        self.search_path = root
                        search = True

        if not search:
            self.path_search['text'] = '경로를 찾을 수 없습니다.'
        else:
            self.install['state'] = 'normal'
            self.path_search['text'] = self.search_path
            self.progress_text['text'] = '서든어택 경로를 찾았습니다.'
            skin.setup(self.search_path)

    def thread_install(self):
        threading.Thread(target=self.download).start()

    def download(self):
        self.progress_text['text'] = '스킨정보를 읽어들이고 있습니다..'
        checked = False
        time.sleep(3)

        if self.map_supply_checked.get():
            url = skin.download('map_supply', self.map_supply_checked.get()) + '/download'
            checked = True
            self.download_process('보급창고', url, self.search_path + '\\map_supply.zip', self.search_path + '\\game\\sa_tex')

        if self.map_dragon_checked.get():
            url = skin.download('map_dragon', self.map_dragon_checked.get()) + '/download'
            checked = True
            self.download_process('드래곤로드', url, self.search_path + '\\map_dragon.zip',
                                  self.search_path + '\\game\\sa_tex\\hongkong')

        if self.map_duo_checked.get():
            url = skin.download('map_duo', self.map_duo_checked.get()) + '/download'
            checked = True
            self.download_process('듀오', url, self.search_path + '\\map_duo.zip',
                                  self.search_path + '\\game\\sa_tex2014\\slumdog')

        if self.map_crosscounter_checked.get():
            url = skin.download('map_crosscounter', self.map_crosscounter_checked.get()) + '/download'
            checked = True
            self.download_process('크로스카운터', url, self.search_path + '\\map_crosscounter.zip',
                                  self.search_path + '\\game\\sa_tex\\awp')

        if self.map_crossport_checked.get():
            url = skin.download('map_crossport', self.map_crossport_checked.get()) + '/download'
            checked = True
            self.download_process('크로스포트', url, self.search_path + '\\map_crossport.zip',
                                  self.search_path + '\\game\\sa_tex\\morocco')

        if self.map_goldeneye_checked.get():
            url = skin.download('map_goldeneye', self.map_goldeneye_checked.get()) + '/download'
            checked = True
            self.download_process('골든아이', url, self.search_path + '\\map_goldeneye.zip',
                                  self.search_path + '\\game\\sa_tex\\japen')

        if self.map_clubnight_checked.get():
            url = skin.download('map_clubnight', self.map_clubnight_checked.get()) + '/download'
            checked = True
            self.download_process('클럽나이트', url, self.search_path + '\\map_clubnight.zip',
                                  self.search_path + '\\game\\sa_tex\\nightclub')

        if self.map_provence_checked.get():
            url = skin.download('map_provence', self.map_provence_checked.get()) + '/download'
            checked = True
            self.download_process('프로방스', url, self.search_path + '\\map_provence.zip',
                                  self.search_path + '\\game\\sa_tex\\provence')

        if self.map_trio_checked.get():
            url = skin.download('map_trio', self.map_trio_checked.get()) + '/download'
            checked = True
            self.download_process('트리오', url, self.search_path + '\\map_trio.zip',
                                  self.search_path + '\\game\\sa_tex2013\\damascus')

        if self.weapon_1_checked.get():
            url = skin.download('weapon_flu', self.weapon_1_checked.get()) + '/download'
            checked = True
            self.download_process('형광', url, self.search_path + '\\weapon_flu.zip', self.search_path + '\\game')

        if self.scope_checked.get():
            url = skin.download('scope', self.scope_checked.get()) + '/download'
            checked = True
            self.download_process('스코프', url, self.search_path + '\\scope.zip', self.search_path + '\\game\\sa_interface\\hud\\scope')

        if not checked:
            self.progress_text['text'] = '스킨을 선택해주세요. (선택 안되어있음)'
            return

        self.map_supply_checked.set(0)
        self.map_dragon_checked.set(0)
        self.map_duo_checked.set(0)
        self.map_crosscounter_checked.set(0)
        self.map_crossport_checked.set(0)
        self.map_goldeneye_checked.set(0)
        self.map_clubnight_checked.set(0)
        self.map_provence_checked.set(0)
        self.map_trio_checked.set(0)
        self.weapon_1_checked.set(0)
        self.scope_checked.set(0)

    def download_process(self, section, url, download_path, target):
        url = STORAGE_URL + url
        self.progress_text['text'] = section + ' 스킨 다운로드를 시작합니다.'
        time.sleep(1)

        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        t = tqdm.tqdm(total=total_size, unit='iB', unit_scale=True)
        with open(download_path, 'wb') as f:
            for data in response.iter_content(block_size):
                self.progress_text['text'] = t
                t.update(len(data))
                f.write(data)
        t.close()
        f.close()
        response.close()

        self.progress_text['text'] = '압축 해제중입니다.'
        common.unzip(download_path, target)
        os.remove(download_path)
        self.progress_text['text'] = section + ' 스킨 설치가 완료되었습니다.'

    def self_dir_search(self):
        self.self_dir = filedialog.askdirectory(title='Browse SuddenAttack Folder')

        if self.self_dir:
            self.install['state'] = 'normal'
            self.search_path = self.self_dir
            self.path_search['text'] = self.self_dir
            self.progress_text['text'] = '서든어택 경로를 불러왔습니다.'
            skin.setup(self.self_dir)

if __name__ == "__main__":
    root = tk.Tk()
    root.title('SuddenAttack Easy Skin Manager v' + VERSION)
    root.geometry(str(CONTAINER_WIDTH) + 'x' + str(CONTAINER_HEIGHT) + '+0+50')
    root.resizable(False, False)
    root.maxsize(width=CONTAINER_WIDTH, height=CONTAINER_HEIGHT)
    root.minsize(width=CONTAINER_WIDTH, height=CONTAINER_HEIGHT)
    root.configure(background=BACKGROUND_COLOR)
    # root.iconbitmap(r'C:\Users\kevin\Desktop\sa_skin-master\saskinio.ico')
    app = Application(master=root)
    app.mainloop()
