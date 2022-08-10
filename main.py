import requests
import os
import threading
import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
import time
from datetime import datetime, timedelta
import customtkinter
import pandas as pd
import numpy as np
from tkinter import StringVar
from osu import apiV1
from tkcalendar import DateEntry

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(color_string="blue")  # Themes: "blue" (standard), "green", "dark-blue"
downloaded = 0
def ReadConfig():
    try:
        SaveDirectory=""
        ApiV1=""
        AutoUpdate=""
        with open('Config.txt',encoding='utf-8',) as f:
            for a in f.readlines():
                if a.__contains__("SaveDirectory"):
                    SaveDirectory= a.split("::")[1]
                elif a.__contains__("ApiV1"):
                    ApiV1 = a.split("::")[1]
                elif a.__contains__("AutoUpdate"):
                    AutoUpdate = a.split("::")[1]
        return SaveDirectory.split('\n')[0],ApiV1,AutoUpdate
    except:
        return '', '', ''

class App(customtkinter.CTk):
    WIDTH = 960
    HEIGHT = 640
    def __init__(self):
        super().__init__()
        self.api = 'https://kitsu.moe/d/'
        self.api2 = 'https://akatsuki.pw/d/'
        self.downloadedMaps = 0
        self.folder_selected,self.ApiV1 ,self.AutoUpdate = ReadConfig()
        #self.OriginalData = pd.read_csv('data/standard.csv', encoding="utf-8")
        #self.df = self.OriginalData
        self.Songs,self.DownloadSongsList,self.Matching = [] , [], []
        self.title("Simple Beatmap Downloader")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        #self.resizable(width=False, height=False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed
        #Modes
        self.ModeType, self.Status = StringVar(), StringVar()
        self.MinDate, self.MaxDate = StringVar(), StringVar()
        # row 1
        self.AutoUpdateCheck=StringVar()
        self.CheckTitle,self.CheckDifficulty = StringVar(),StringVar()
        self.CheckArtist,self.CheckCreator = StringVar(),StringVar()
        self.Title, self.DifficultyName = StringVar(), StringVar()
        self.Artist, self.Creator = StringVar(), StringVar()
        self.BeatmapSetId, self.BeatmapID = StringVar(), StringVar()
        self.Title.trace("w", lambda name, index, mode, var=self.Title: self.test())
        self.DifficultyName.trace("w", lambda name, index, mode, var=self.DifficultyName: self.test())
        self.Artist.trace("w", lambda name, index, mode, var=self.Artist: self.test())
        self.Creator.trace("w", lambda name, index, mode, var=self.Creator: self.test())
        self.BeatmapSetId.trace("w", lambda name, index, mode, var=self.BeatmapSetId: self.test())
        self.BeatmapID.trace("w", lambda name, index, mode, var=self.BeatmapID: self.test())
        # end of row1
        # row 2
        self.MinBPM, self.MaxBPM = StringVar(), StringVar()
        self.MinAR, self.MaxAR = StringVar(), StringVar()
        self.MinOD, self.MaxOD = StringVar(), StringVar()
        self.MinCS, self.MaxCS = StringVar(), StringVar()
        self.MinHP, self.MaxHP = StringVar(), StringVar()
        self.MinSTARS, self.MaxSTARS = StringVar(), StringVar()
        self.MinBPM.trace("w", lambda name, index, mode, var=self.MinBPM: self.test())
        self.MaxBPM.trace("w", lambda name, index, mode, var=self.MaxBPM: self.test())
        self.MinAR.trace("w", lambda name, index, mode, var=self.MinAR: self.test())
        self.MaxAR.trace("w", lambda name, index, mode, var=self.MaxAR: self.test())
        self.MinOD.trace("w", lambda name, index, mode, var=self.MinOD: self.test())
        self.MaxOD.trace("w", lambda name, index, mode, var=self.MaxOD: self.test())
        self.MinCS.trace("w", lambda name, index, mode, var=self.MinCS: self.test())
        self.MaxCS.trace("w", lambda name, index, mode, var=self.MaxCS: self.test())
        self.MinHP.trace("w", lambda name, index, mode, var=self.MinHP: self.test())
        self.MaxHP.trace("w", lambda name, index, mode, var=self.MaxHP: self.test())
        self.MinSTARS.trace("w", lambda name, index, mode, var=self.MinSTARS: self.test())
        self.MaxSTARS.trace("w", lambda name, index, mode, var=self.MaxSTARS: self.test())
        # end of row 2
        # row 3
        self.MD5Hash = StringVar()
        self.MinLength, self.MaxLength = StringVar(), StringVar()
        self.MinPlaycount, self.MaxPlaycount = StringVar(), StringVar()
        self.MinMaxCombo, self.MaxMaxCombo = StringVar(), StringVar()
        self.MinStarsAim, self.MaxStarsAim = StringVar(), StringVar()
        self.MinStarsSpeed, self.MaxStarsSpeed = StringVar(), StringVar()
        self.MD5Hash.trace("w", lambda name, index, mode, var=self.MD5Hash: self.test())
        self.MinLength.trace("w", lambda name, index, mode, var=self.MinLength: self.test())
        self.MaxLength.trace("w", lambda name, index, mode, var=self.MaxLength: self.test())
        self.MinPlaycount.trace("w", lambda name, index, mode, var=self.MinPlaycount: self.test())
        self.MaxPlaycount.trace("w", lambda name, index, mode, var=self.MaxPlaycount: self.test())
        self.MinMaxCombo.trace("w", lambda name, index, mode, var=self.MinMaxCombo: self.test())
        self.MaxMaxCombo.trace("w", lambda name, index, mode, var=self.MaxMaxCombo: self.test())
        self.MinStarsAim.trace("w", lambda name, index, mode, var=self.MinStarsAim: self.test())
        self.MaxStarsAim.trace("w", lambda name, index, mode, var=self.MaxStarsAim: self.test())
        self.MinStarsSpeed.trace("w", lambda name, index, mode, var=self.MinStarsSpeed: self.test())
        self.MaxStarsSpeed.trace("w", lambda name, index, mode, var=self.MaxStarsSpeed: self.test())
        # end of row 3




        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(3,weight=0)
        self.grid_columnconfigure(0,weight=1)
        self.bottom_frame = customtkinter.CTkFrame(master=self)

        self.mid_frame = customtkinter.CTkFrame(master=self)
        self.top_frame = customtkinter.CTkFrame(master=self)
        self.bottom_frame.grid(row=3, column=0,rowspan=1, sticky="n")
        self.mid_frame.grid(row=0, column=0,rowspan=3, sticky="wsne", padx=20, pady=20)
        #self.top_frame.grid(row=0, column=0, sticky="wsne", padx=20, pady=20)

        # ============ bottom_frame ============
        # configure tree lauyout
        self.change_appearance_mode("dark")
        ttk.Style().theme_use("alt")
        ttk.Style().configure("Treeview", background="#2a2d2e",
                              foreground="white", fieldbackground="#cc366d7",font=("Roboto Medium", -13))
        ttk.Style().configure("Treeview.Heading",fieldbackground="#343638" , background="#343638", foreground="white",font=("Roboto Medium", -16))
        self.tree = ttk.Treeview(master=self.bottom_frame, height=8)
        self.scrolly = ttk.Scrollbar(self.bottom_frame, orient="vertical", command=self.tree.yview)
        self.scrolly.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.scrollx = ttk.Scrollbar(self.bottom_frame, orient="horizontal", command=self.tree.xview)
        self.scrollx.pack(side=tk.BOTTOM, fill=tk.BOTH)
        self.tree.pack()
        self.tree.configure(yscrollcommand=self.scrolly.set)
        self.tree.configure(xscrollcommand=self.scrollx.set)

        # start of insertion
        # ============ top_frame ============

        # configure grid layout (3x7)
        # self.top_frame.rowconfigure(index=(0,1,2,3), weight=0)
        # self.top_frame.columnconfigure((0, 1,2,3,4,5,6), weight=1)

        # self.frame_info = customtkinter.CTkFrame(master=self.top_frame)
        # self.frame_info.grid(row=0, column=0,columnspan=7, pady=20, padx=20, sticky="nsew")

        #ModeSelection
        self.ModeF = tk.LabelFrame(self.mid_frame,width=350,height=85)
        # self.ModeF.place(relx=0, rely=0, relheight=0.2, relwidth=0.332)
        self.ModeF.pack(anchor='nw',expand=False)
        self.ModeF.configure(text='''Mode''', font="-family {Segoe UI} -size 16", background="#2a2d2e",
                               foreground="white")
        self.StandardMode = customtkinter.CTkRadioButton(self.ModeF, text_font=("Roboto Medium", -16), text='''Standard'''
                                                    ,variable=self.ModeType,command=self.FilterOriginalData,value=1)
        self.StandardMode.place(anchor="w", relx=0.01, rely=0.1,)
        self.TaikoMode = customtkinter.CTkRadioButton(self.ModeF, text_font=("Roboto Medium", -16),
                                                         text='''Taiko'''
                                                         , variable=self.ModeType, command=self.FilterOriginalData, value=2)
        self.TaikoMode.place(anchor="w", relx=0.3, rely=0.1, )
        self.CtBMode = customtkinter.CTkRadioButton(self.ModeF, text_font=("Roboto Medium", -16),
                                                      text='''CtB'''
                                                      , variable=self.ModeType, command=self.FilterOriginalData, value=3)
        self.CtBMode.place(anchor="w", relx=0.52, rely=0.1, )
        self.ManiaMode = customtkinter.CTkRadioButton(self.ModeF, text_font=("Roboto Medium", -16),
                                                    text='''Mania'''
                                                    , variable=self.ModeType, command=self.FilterOriginalData, value=4)
        self.ManiaMode.place(anchor="w", relx=0.69, rely=0.1,)

        self.AllStatus = customtkinter.CTkRadioButton(self.ModeF, text_font=("Roboto Medium", -16),
                                                      text='''All'''
                                                      , variable=self.Status, command=self.FilterOriginalData, value=1)
        self.AllStatus.place(anchor="w", relx=0.01, rely=0.6, )

        self.RankedStatus = customtkinter.CTkRadioButton(self.ModeF, text_font=("Roboto Medium", -16),
                                                      text='''Ranked'''
                                                      , variable=self.Status, command=self.FilterOriginalData, value=2)
        self.RankedStatus.place(anchor="w", relx=0.175, rely=0.6, )

        self.LovedStatus = customtkinter.CTkRadioButton(self.ModeF, text_font=("Roboto Medium", -16),
                                                         text='''Loved'''
                                                         , variable=self.Status, command=self.FilterOriginalData, value=3)
        self.LovedStatus.place(anchor="w", relx=0.43, rely=0.6,)
        self.ApprovedStatus = customtkinter.CTkRadioButton(self.ModeF, text_font=("Roboto Medium", -16),
                                                        text='''Approved'''
                                                        , variable=self.Status, command=self.FilterOriginalData, value=4)
        self.ApprovedStatus.place(anchor="w", relx=0.66, rely=0.6,)

        #Date Picker
        self.DatePickLF = tk.LabelFrame(self.mid_frame)
        self.DatePickLF.place(relx=0.0, rely=0.8, relheight=0.2, relwidth=0.166)
        self.DatePickLF.configure(text='''Date''', font="-family {Segoe UI} -size 16", background="#2a2d2e", foreground="white")

        self.DateMaxFrame = tk.LabelFrame(self.DatePickLF)
        self.DateMaxFrame.place(relx=0.5, rely=0.31, relheight=0.65, relwidth=0.45, bordermode='ignore')
        self.DateMaxFrame.configure(text='''Max''', font="-family {Segoe UI} -size 13", background="#2a2d2e",
                                  foreground="white")
        self.DateMinFrame = tk.LabelFrame(self.DatePickLF)
        self.DateMinFrame.place(relx=0.05, rely=0.31, relheight=0.65, relwidth=0.45, bordermode='ignore')
        self.DateMinFrame.configure(text='''Min''', font="-family {Segoe UI} -size 13", background="#2a2d2e",
                                  foreground="white")
        self.EntryDateMin =DateEntry(self.DateMinFrame,selectmode='day',textvariable=self.MinDate)
        self.MinDate.set('''1/1/07''')
        self.EntryDateMin.place(relx=0.05, rely=0.45, relheight=0.4, relwidth=0.90, bordermode='ignore')
        self.EntryDateMax = DateEntry(self.DateMaxFrame,selectmode='day',textvariable=self.MaxDate)
        self.EntryDateMax.place(relx=0.05, rely=0.45, relheight=0.4, relwidth=0.90, bordermode='ignore')

        # self.MinDatePicker = DateEntry(self.mid_frame,selectmode='day')
        # self.MinDatePicker.place(relx=0.4, rely = 0.05, relwidth=0.1,relheight=0.05)
        # self.MinDatePicker.configure(font="-family {Segoe UI} -size 13",disabledselectbackground ="black",background='black')
        #title
        self.TitleLF = tk.LabelFrame(self.mid_frame)
        self.TitleLF.place(relx=0, rely = 0.2, relheight=0.2, relwidth=0.166)
        self.TitleLF.configure(text='''Title''',font="-family {Segoe UI} -size 16",background="#2a2d2e",foreground="white")
        self.EntryTitle = customtkinter.CTkEntry(self.TitleLF, textvariable=self.Title,height=25)
        self.EntryTitle.place(relx=0.05, rely=0.35, relheight=0.25, relwidth=0.90, bordermode='ignore')
        self.ExactTitle = customtkinter.CTkCheckBox(self.TitleLF,text_font=("Roboto Medium", -13),text='''Exact'''
                                                    ,variable=self.CheckTitle,onvalue=1,offvalue=0,command=self.test)
        self.ExactTitle.place(anchor="center",relx=0.53,rely=0.70,)
        #difficulty
        self.DifficultyNameLF = tk.LabelFrame(self.mid_frame)
        self.DifficultyNameLF.place(relx=0.166, rely = 0.2, relheight=0.2, relwidth=0.166)
        self.DifficultyNameLF.configure(text='''Difficulty''', font="-family {Segoe UI} -size 16", background="#2a2d2e",foreground="white")
        self.EntryDifficulty = customtkinter.CTkEntry(self.DifficultyNameLF, textvariable=self.DifficultyName, height=25)
        self.EntryDifficulty.place(relx=0.05, rely=0.35, relheight=0.25, relwidth=0.90, bordermode='ignore')
        self.ExactDifficulty = customtkinter.CTkCheckBox(self.DifficultyNameLF, text_font=("Roboto Medium", -13), text='''Exact'''
                                                         ,variable=self.CheckDifficulty,onvalue=1,offvalue=0,command=self.test)
        self.ExactDifficulty.place(anchor="center", relx=0.53, rely=0.70, )
        #Artist
        self.ArtistLF = tk.LabelFrame(self.mid_frame)
        self.ArtistLF.place(relx=0.332, rely = 0.2, relheight=0.2, relwidth=0.166)
        self.ArtistLF.configure(text='''Artist''', font="-family {Segoe UI} -size 16", background="#2a2d2e",foreground="white")
        self.EntryArtist = customtkinter.CTkEntry(self.ArtistLF, textvariable=self.Artist, height=25)
        self.EntryArtist.place(relx=0.05, rely=0.35, relheight=0.25, relwidth=0.90, bordermode='ignore')
        self.ExactArtist = customtkinter.CTkCheckBox(self.ArtistLF, text_font=("Roboto Medium", -13),text='''Exact''',
                                                     variable=self.CheckArtist,onvalue=1,offvalue=0,command=self.test)
        self.ExactArtist.place(anchor="center", relx=0.53, rely=0.70, )
        #Creator
        self.CreatorLF = tk.LabelFrame(self.mid_frame)
        self.CreatorLF.place(relx=0.498, rely = 0.2, relheight=0.2, relwidth=0.166)
        self.CreatorLF.configure(text='''Creator''', font="-family {Segoe UI} -size 16", background="#2a2d2e",foreground="white")
        self.EntryCreator = customtkinter.CTkEntry(self.CreatorLF, textvariable=self.Creator, height=25)
        self.EntryCreator.place(relx=0.05, rely=0.35, relheight=0.25, relwidth=0.90, bordermode='ignore')
        self.ExactCreator = customtkinter.CTkCheckBox(self.CreatorLF, text_font=("Roboto Medium", -13), text='''Exact''',
                                                      variable=self.CheckCreator,onvalue=1,offvalue=0,command=self.test)
        self.ExactCreator.place(anchor="center", relx=0.53, rely=0.70)
        #BeatmapSet id
        self.BeatmapSetIdLF = tk.LabelFrame(self.mid_frame)
        self.BeatmapSetIdLF.place(relx=0.664, rely = 0.2, relheight=0.2, relwidth=0.166)
        self.BeatmapSetIdLF.configure(text='''BeatmapSet ID''', font="-family {Segoe UI} -size 16", background="#2a2d2e", foreground="white")
        self.EntryBeatmapSetId = customtkinter.CTkEntry(self.BeatmapSetIdLF, textvariable=self.BeatmapSetId)
        self.EntryBeatmapSetId.place(relx=0.05, rely=0.35, relheight=0.25, relwidth=0.90, bordermode='ignore')
        #Beatmap id
        self.BeatmapIdLF = tk.LabelFrame(self.mid_frame)
        self.BeatmapIdLF.place(relx=0.83, rely = 0.2, relheight=0.2, relwidth=0.166)
        self.BeatmapIdLF.configure(text='''Beatmap ID''', font="-family {Segoe UI} -size 16", background="#2a2d2e",foreground="white")
        self.EntryBeatmapId = customtkinter.CTkEntry(self.BeatmapIdLF, textvariable=self.BeatmapID, height=25)
        self.EntryBeatmapId.place(relx=0.05, rely=0.35, relheight=0.25, relwidth=0.90, bordermode='ignore')
        #BPM
        self.BPMLF = tk.LabelFrame(self.mid_frame)
        self.BPMLF.place(relx=0.0, rely = 0.4, relheight=0.2, relwidth=0.166)
        self.BPMLF.configure(text='''BPM''', font="-family {Segoe UI} -size 16", background="#2a2d2e",foreground="white")

        self.BPMmaxFrame = tk.LabelFrame(self.BPMLF)
        self.BPMmaxFrame.place(relx=0.5, rely=0.31, relheight=0.65, relwidth=0.45, bordermode='ignore')
        self.BPMmaxFrame.configure(text='''Max''', font="-family {Segoe UI} -size 12", background="#2a2d2e",
                                   foreground="white")
        self.BPMminFrame = tk.LabelFrame(self.BPMLF)
        self.BPMminFrame.place(relx=0.05, rely=0.31, relheight=0.65, relwidth=0.45, bordermode='ignore')
        self.BPMminFrame.configure(text='''Min''', font="-family {Segoe UI} -size 12", background="#2a2d2e",
                                   foreground="white")
        self.EntryBPMmin = customtkinter.CTkEntry(self.BPMminFrame, textvariable=self.MinBPM)
        self.EntryBPMmin.place(relx=0.05, rely=0.45, relheight=0.4, relwidth=0.90, bordermode='ignore')
        self.EntryBPMmax = customtkinter.CTkEntry(self.BPMmaxFrame, textvariable=self.MaxBPM, height=50)
        self.EntryBPMmax.place(relx=0.05, rely=0.45, relheight=0.4, relwidth=0.90, bordermode='ignore')
        #AR
        self.ARLF = tk.LabelFrame(self.mid_frame)
        self.ARLF.place(relx=0.166, rely = 0.4, relheight=0.2, relwidth=0.166)
        self.ARLF.configure(text='''AR''', font="-family {Segoe UI} -size 16", background="#2a2d2e",foreground="white")

        self.ARmaxFrame = tk.LabelFrame(self.ARLF)
        self.ARmaxFrame.place(relx=0.5, rely=0.31, relheight=0.65, relwidth=0.45, bordermode='ignore')
        self.ARmaxFrame.configure(text='''Max''', font="-family {Segoe UI} -size 12", background="#2a2d2e",
                                   foreground="white")
        self.ARminFrame = tk.LabelFrame(self.ARLF)
        self.ARminFrame.place(relx=0.05, rely=0.31, relheight=0.65, relwidth=0.45, bordermode='ignore')
        self.ARminFrame.configure(text='''Min''', font="-family {Segoe UI} -size 12", background="#2a2d2e",
                                   foreground="white")
        self.EntryARmin = customtkinter.CTkEntry(self.ARminFrame, textvariable=self.MinAR)
        self.EntryARmin.place(relx=0.05, rely=0.45, relheight=0.4, relwidth=0.90, bordermode='ignore')
        self.EntryARmax = customtkinter.CTkEntry(self.ARmaxFrame, textvariable=self.MaxAR)
        self.EntryARmax.place(relx=0.05, rely=0.45, relheight=0.4, relwidth=0.90, bordermode='ignore')
        #OD
        self.ODLF = tk.LabelFrame(self.mid_frame)
        self.ODLF.place(relx=0.332, rely = 0.4, relheight=0.2, relwidth=0.166)
        self.ODLF.configure(text='''OD''', font="-family {Segoe UI} -size 16", background="#2a2d2e",foreground="white")

        self.ODmaxFrame = tk.LabelFrame(self.ODLF)
        self.ODmaxFrame.place(relx=0.5, rely=0.31, relheight=0.65, relwidth=0.45, bordermode='ignore')
        self.ODmaxFrame.configure(text='''Max''', font="-family {Segoe UI} -size 12", background="#2a2d2e",
                                  foreground="white")
        self.ODminFrame = tk.LabelFrame(self.ODLF)
        self.ODminFrame.place(relx=0.05, rely=0.31, relheight=0.65, relwidth=0.45, bordermode='ignore')
        self.ODminFrame.configure(text='''Min''', font="-family {Segoe UI} -size 12", background="#2a2d2e",
                                  foreground="white")
        self.EntryODmin = customtkinter.CTkEntry(self.ODminFrame, textvariable=self.MinOD)
        self.EntryODmin.place(relx=0.05, rely=0.45, relheight=0.4, relwidth=0.90, bordermode='ignore')
        self.EntryODmax = customtkinter.CTkEntry(self.ODmaxFrame, textvariable=self.MaxOD)
        self.EntryODmax.place(relx=0.05, rely=0.45, relheight=0.4, relwidth=0.90, bordermode='ignore')
        #CS
        self.CSLF = tk.LabelFrame(self.mid_frame)
        self.CSLF.place(relx=0.498, rely = 0.4, relheight=0.2, relwidth=0.166)
        self.CSLF.configure(text='''CS''', font="-family {Segoe UI} -size 16", background="#2a2d2e",foreground="white")

        self.CSmaxFrame = tk.LabelFrame(self.CSLF)
        self.CSmaxFrame.place(relx=0.5, rely=0.31, relheight=0.65, relwidth=0.45, bordermode='ignore')
        self.CSmaxFrame.configure(text='''Max''', font="-family {Segoe UI} -size 12", background="#2a2d2e",
                                  foreground="white")
        self.CSminFrame = tk.LabelFrame(self.CSLF)
        self.CSminFrame.place(relx=0.05, rely=0.31, relheight=0.65, relwidth=0.45, bordermode='ignore')
        self.CSminFrame.configure(text='''Min''', font="-family {Segoe UI} -size 12", background="#2a2d2e",
                                  foreground="white")
        self.EntryCSmin = customtkinter.CTkEntry(self.CSminFrame, textvariable=self.MinCS)
        self.EntryCSmin.place(relx=0.05, rely=0.45, relheight=0.4, relwidth=0.90, bordermode='ignore')
        self.EntryCSmax = customtkinter.CTkEntry(self.CSmaxFrame, textvariable=self.MaxCS)
        self.EntryCSmax.place(relx=0.05, rely=0.45, relheight=0.4, relwidth=0.90, bordermode='ignore')
        #HP
        self.HPLF = tk.LabelFrame(self.mid_frame)
        self.HPLF.place(relx=0.664, rely = 0.4, relheight=0.2, relwidth=0.166)
        self.HPLF.configure(text='''HP''', font="-family {Segoe UI} -size 16", background="#2a2d2e",foreground="white")

        self.HPmaxFrame = tk.LabelFrame(self.HPLF)
        self.HPmaxFrame.place(relx=0.5, rely=0.31, relheight=0.65, relwidth=0.45, bordermode='ignore')
        self.HPmaxFrame.configure(text='''Max''', font="-family {Segoe UI} -size 12", background="#2a2d2e",
                                  foreground="white")
        self.HPminFrame = tk.LabelFrame(self.HPLF)
        self.HPminFrame.place(relx=0.05, rely=0.31, relheight=0.65, relwidth=0.45, bordermode='ignore')
        self.HPminFrame.configure(text='''Min''', font="-family {Segoe UI} -size 12", background="#2a2d2e",
                                  foreground="white")
        self.EntryHPmin = customtkinter.CTkEntry(self.HPminFrame, textvariable=self.MinHP)
        self.EntryHPmin.place(relx=0.05, rely=0.45, relheight=0.4, relwidth=0.90, bordermode='ignore')
        self.EntryHPmax = customtkinter.CTkEntry(self.HPmaxFrame, textvariable=self.MaxHP)
        self.EntryHPmax.place(relx=0.05, rely=0.45, relheight=0.4, relwidth=0.90, bordermode='ignore')
        #STARS
        self.STARSLF = tk.LabelFrame(self.mid_frame)
        self.STARSLF.place(relx=0.83, rely = 0.4, relheight=0.2, relwidth=0.166)
        self.STARSLF.configure(text='''STARS''', font="-family {Segoe UI} -size 16", background="#2a2d2e",
                             foreground="white")
        self.STARSmaxFrame = tk.LabelFrame(self.STARSLF)
        self.STARSmaxFrame.place(relx=0.5, rely=0.31, relheight=0.65, relwidth=0.45, bordermode='ignore')
        self.STARSmaxFrame.configure(text='''Max''', font="-family {Segoe UI} -size 12", background="#2a2d2e",
                                  foreground="white")
        self.STARSminFrame = tk.LabelFrame(self.STARSLF)
        self.STARSminFrame.place(relx=0.05, rely=0.31, relheight=0.65, relwidth=0.45, bordermode='ignore')
        self.STARSminFrame.configure(text='''Min''', font="-family {Segoe UI} -size 12", background="#2a2d2e",
                                  foreground="white")
        self.EntrySTARSmin = customtkinter.CTkEntry(self.STARSminFrame, textvariable=self.MinSTARS)
        self.EntrySTARSmin.place(relx=0.05, rely=0.45, relheight=0.4, relwidth=0.90, bordermode='ignore')
        self.EntrySTARSmax = customtkinter.CTkEntry(self.STARSmaxFrame, textvariable=self.MaxSTARS)
        self.EntrySTARSmax.place(relx=0.05, rely=0.45, relheight=0.4, relwidth=0.90, bordermode='ignore')
        #MD5 HASH
        self.MD5LF = tk.LabelFrame(self.mid_frame)
        self.MD5LF.place(relx=0.0, rely = 0.6, relheight=0.2, relwidth=0.166)
        self.MD5LF.configure(text='''MD5 Hash''', font="-family {Segoe UI} -size 16", background="#2a2d2e",foreground="white")
        self.MD5Entry = customtkinter.CTkEntry(self.MD5LF,textvariable=self.MD5Hash)
        self.MD5Entry.place(relx=0.05, rely=0.35, relheight=0.25, relwidth=0.90, bordermode='ignore')
        #TOTAL LENGTH
        self.LENGTHLF = tk.LabelFrame(self.mid_frame)
        self.LENGTHLF.place(relx=0.166, rely = 0.6, relheight=0.2, relwidth=0.166)
        self.LENGTHLF.configure(text='''Total Length''', font="-family {Segoe UI} -size 16", background="#2a2d2e",foreground="white")

        self.LENGTHmaxFrame = tk.LabelFrame(self.LENGTHLF)
        self.LENGTHmaxFrame.place(relx=0.5, rely=0.31, relheight=0.65, relwidth=0.45, bordermode='ignore')
        self.LENGTHmaxFrame.configure(text='''Max''', font="-family {Segoe UI} -size 12", background="#2a2d2e",
                                     foreground="white")
        self.LENGTHminFrame = tk.LabelFrame(self.LENGTHLF)
        self.LENGTHminFrame.place(relx=0.05, rely=0.31, relheight=0.65, relwidth=0.45, bordermode='ignore')
        self.LENGTHminFrame.configure(text='''Min''', font="-family {Segoe UI} -size 12", background="#2a2d2e",
                                     foreground="white")
        self.EntryLENGTHmin = customtkinter.CTkEntry(self.LENGTHminFrame, textvariable=self.MinLength)
        self.EntryLENGTHmin.place(relx=0.05, rely=0.45, relheight=0.4, relwidth=0.90, bordermode='ignore')
        self.EntryLENGTHmax = customtkinter.CTkEntry(self.LENGTHmaxFrame, textvariable=self.MaxLength)
        self.EntryLENGTHmax.place(relx=0.05, rely=0.45, relheight=0.4, relwidth=0.90, bordermode='ignore')
        #PLAYCOUNT
        self.PLAYCOUNTLF = tk.LabelFrame(self.mid_frame)
        self.PLAYCOUNTLF.place(relx=0.332, rely = 0.6, relheight=0.2, relwidth=0.166)
        self.PLAYCOUNTLF.configure(text='''Playcount''', font="-family {Segoe UI} -size 16", background="#2a2d2e",foreground="white")

        self.PLAYCOUNTmaxFrame = tk.LabelFrame(self.PLAYCOUNTLF)
        self.PLAYCOUNTmaxFrame.place(relx=0.5, rely=0.31, relheight=0.65, relwidth=0.45, bordermode='ignore')
        self.PLAYCOUNTmaxFrame.configure(text='''Max''', font="-family {Segoe UI} -size 12", background="#2a2d2e",
                                      foreground="white")
        self.PLAYCOUNTminFrame = tk.LabelFrame(self.PLAYCOUNTLF)
        self.PLAYCOUNTminFrame.place(relx=0.05, rely=0.31, relheight=0.65, relwidth=0.45, bordermode='ignore')
        self.PLAYCOUNTminFrame.configure(text='''Min''', font="-family {Segoe UI} -size 12", background="#2a2d2e",
                                      foreground="white")
        self.EntryPLAYCOUNTmin = customtkinter.CTkEntry(self.PLAYCOUNTminFrame, textvariable=self.MinPlaycount)
        self.EntryPLAYCOUNTmin.place(relx=0.05, rely=0.45, relheight=0.4, relwidth=0.90, bordermode='ignore')
        self.EntryPLAYCOUNTmax = customtkinter.CTkEntry(self.PLAYCOUNTmaxFrame, textvariable=self.MaxPlaycount)
        self.EntryPLAYCOUNTmax.place(relx=0.05, rely=0.45, relheight=0.4, relwidth=0.90, bordermode='ignore')
        #MAX COMBO
        self.MaxCOMBOLF = tk.LabelFrame(self.mid_frame)
        self.MaxCOMBOLF.place(relx=0.498, rely = 0.6, relheight=0.2, relwidth=0.166)
        self.MaxCOMBOLF.configure(text='''Max Combo''', font="-family {Segoe UI} -size 16", background="#2a2d2e",foreground="white")

        self.MaxCOMBOmaxFrame = tk.LabelFrame(self.MaxCOMBOLF)
        self.MaxCOMBOmaxFrame.place(relx=0.5, rely=0.31, relheight=0.65, relwidth=0.45, bordermode='ignore')
        self.MaxCOMBOmaxFrame.configure(text='''Max''', font="-family {Segoe UI} -size 12", background="#2a2d2e",
                                         foreground="white")
        self.MaxCOMBOminFrame = tk.LabelFrame(self.MaxCOMBOLF)
        self.MaxCOMBOminFrame.place(relx=0.05, rely=0.31, relheight=0.65, relwidth=0.45, bordermode='ignore')
        self.MaxCOMBOminFrame.configure(text='''Min''', font="-family {Segoe UI} -size 12", background="#2a2d2e",
                                         foreground="white")
        self.EntryMaxCOMBOmin = customtkinter.CTkEntry(self.MaxCOMBOminFrame, textvariable=self.MinMaxCombo)
        self.EntryMaxCOMBOmin.place(relx=0.05, rely=0.45, relheight=0.4, relwidth=0.90, bordermode='ignore')
        self.EntryMaxCOMBOmax = customtkinter.CTkEntry(self.MaxCOMBOmaxFrame, textvariable=self.MaxMaxCombo)
        self.EntryMaxCOMBOmax.place(relx=0.05, rely=0.45, relheight=0.4, relwidth=0.90, bordermode='ignore')
        #STARS AIM
        self.AIMLF = tk.LabelFrame(self.mid_frame)
        self.AIMLF.place(relx=0.664, rely = 0.6, relheight=0.2, relwidth=0.166)
        self.AIMLF.configure(text='''Stars AIM''', font="-family {Segoe UI} -size 16", background="#2a2d2e",foreground="white")

        self.AIMmaxFrame = tk.LabelFrame(self.AIMLF)
        self.AIMmaxFrame.place(relx=0.5, rely=0.31, relheight=0.65, relwidth=0.45, bordermode='ignore')
        self.AIMmaxFrame.configure(text='''Max''', font="-family {Segoe UI} -size 12", background="#2a2d2e",
                                        foreground="white")
        self.AIMminFrame = tk.LabelFrame(self.AIMLF)
        self.AIMminFrame.place(relx=0.05, rely=0.31, relheight=0.65, relwidth=0.45, bordermode='ignore')
        self.AIMminFrame.configure(text='''Min''', font="-family {Segoe UI} -size 12", background="#2a2d2e",
                                        foreground="white")
        self.EntryMaxAIMmin = customtkinter.CTkEntry(self.AIMminFrame, textvariable=self.MinStarsAim)
        self.EntryMaxAIMmin.place(relx=0.05, rely=0.45, relheight=0.4, relwidth=0.90, bordermode='ignore')
        self.EntryMaxAIMmax = customtkinter.CTkEntry(self.AIMmaxFrame, textvariable=self.MaxStarsAim)
        self.EntryMaxAIMmax.place(relx=0.05, rely=0.45, relheight=0.4, relwidth=0.90, bordermode='ignore')
        #STARS SPEED
        self.SPEEDLF = tk.LabelFrame(self.mid_frame)
        self.SPEEDLF.place(relx=0.83, rely = 0.6, relheight=0.2, relwidth=0.166)
        self.SPEEDLF.configure(text='''Stars SPEED''', font="-family {Segoe UI} -size 16", background="#2a2d2e",foreground="white")

        self.SPEEDmaxFrame = tk.LabelFrame(self.SPEEDLF)
        self.SPEEDmaxFrame.place(relx=0.5, rely=0.31, relheight=0.65, relwidth=0.45, bordermode='ignore')
        self.SPEEDmaxFrame.configure(text='''Max''', font="-family {Segoe UI} -size 12", background="#2a2d2e",
                                   foreground="white")
        self.SPEEDminFrame = tk.LabelFrame(self.SPEEDLF)
        self.SPEEDminFrame.place(relx=0.05, rely=0.31, relheight=0.65, relwidth=0.45, bordermode='ignore')
        self.SPEEDminFrame.configure(text='''Min''', font="-family {Segoe UI} -size 12", background="#2a2d2e",
                                   foreground="white")
        self.EntryMaxSPEEDmin = customtkinter.CTkEntry(self.SPEEDminFrame, textvariable=self.MinStarsSpeed)
        self.EntryMaxSPEEDmin.place(relx=0.05, rely=0.45, relheight=0.4, relwidth=0.90, bordermode='ignore')
        self.EntryMaxSPEEDmax = customtkinter.CTkEntry(self.SPEEDmaxFrame, textvariable=self.MaxStarsSpeed)
        self.EntryMaxSPEEDmax.place(relx=0.05, rely=0.45, relheight=0.4, relwidth=0.90, bordermode='ignore')
        # bar !!
        self.ProgressFrame = customtkinter.CTkFrame(self.mid_frame)
        self.ProgressFrame.place(relx=0.175, rely=0.965, relheight=0.035, relwidth=0.822, bordermode='ignore')
        self.ProgressBar= customtkinter.CTkProgressBar(self.ProgressFrame)
        self.ProgressBar.place(relx=0.0, rely=0.0, relheight=1, relwidth=0.95, bordermode='ignore')
        #LABEL INFO FOR USER
        self.LabelDownloadPerc = customtkinter.CTkLabel(self.ProgressFrame, text="%", justify="left", anchor="nw",height=12,width=12)
        self.LabelDownloadPerc.place(rely=0, relx=0.953)
        self.LabelDisplayed = customtkinter.CTkLabel(self.mid_frame,text="Displayed: ",justify="left",anchor="w",height=12)
        self.LabelDisplayed.place(rely=0.895, relx=0.175)
        self.LabelOverall = customtkinter.CTkLabel(self.mid_frame,text="Overall: ",justify="left",anchor="w",height=12)
        self.LabelOverall.place(rely=0.845, relx=0.175)
        self.LabelSearchTime = customtkinter.CTkLabel(self.mid_frame, text="Search in: ", justify="left", anchor="w",height=12)
        self.LabelSearchTime.place(rely=0.8, relx=0.175)
        self.LabelMySongsNum = customtkinter.CTkLabel(self.mid_frame, text=f"My Songs Sets:{len(self.Songs)}",height=12, justify="left", anchor="w")
        self.LabelMySongsNum.place(rely=0.8, relx=0.3)
        self.LabelMissing = customtkinter.CTkLabel(self.mid_frame, text="Missing: ", justify="left", anchor="w",height=12)
        self.LabelMissing.place(rely=0.895, relx=0.3)
        self.LabelMatching = customtkinter.CTkLabel(self.mid_frame, text="Matching: ", justify="left", anchor="w",height=12)
        self.LabelMatching.place(rely=0.845, relx=0.3)

        self.LabelSongFolder = customtkinter.CTkLabel(self.mid_frame, text="Song Folder not selected! ", justify="left", anchor="w")
        self.LabelSongFolder.place(rely=0.076, relx=0.82)
        self.ExportLabel = customtkinter.CTkLabel(self.mid_frame, text="Exported in: ", justify="left",anchor="w")
        self.ExportLabel.place(rely=0.805, relx=0.85)

        self.UpdateLabel = customtkinter.CTkLabel(self.mid_frame, text="update msg", justify="left", anchor="w")
        self.UpdateLabel.place(rely=0.15, relx=0.55)
        self.ApiKeyPresentLabel = customtkinter.CTkLabel(self.mid_frame, text="Api v1: Missing", justify="left", anchor="center")
        self.ApiKeyPresentLabel.place(rely=0.075, relx=0.66)
        self.CheckAutoUpdate = customtkinter.CTkCheckBox(self.mid_frame, text_font=("Roboto Medium", -13), text='''AutoUpdate'''
                                                    , variable=self.AutoUpdateCheck, onvalue=1, offvalue=0,
                                                    command=self.SaveConfig)
        self.CheckAutoUpdate.place(anchor="center", relx=0.57, rely=0.12, )
        #BUTTONS
        self.GetApi = customtkinter.CTkButton(self.mid_frame,text="Update Data",text_font=24,command=self.UpdateData)
        self.GetApi.place(rely=0.015,relx=0.5,relheight=0.06,relwidth=0.15)
        self.UpdateData = customtkinter.CTkButton(self.mid_frame, text="Enter API v1 key", text_font=24,command=self.InputApiKey)
        self.UpdateData.place(rely=0.015, relx=0.66, relheight=0.06, relwidth=0.15)
        self.Search = customtkinter.CTkButton(self.mid_frame, text="Search", text_font=24, command=self.button_event)
        self.Search.place(rely=0.88, relx=0.55, relheight=0.08, relwidth=0.22)
        self.Search = customtkinter.CTkButton(self.mid_frame, text="Download",text_font=24, command=self.DownloadMaps)
        self.Search.place(rely=0.88, relx=0.775, relheight=0.08, relwidth=0.22)
        self.OsuSongFolder = customtkinter.CTkButton(self.mid_frame, text="Songs Folder", command=self.getSongFolder)
        self.OsuSongFolder.place(rely=0.015, relx=0.82, relheight=0.06, relwidth=0.176)
        self.OsuSongsAnalyze = customtkinter.CTkButton(self.mid_frame, text="Check my Beatmaps", command=self.AnalyzeMySongs)
        self.OsuSongsAnalyze.place(rely=0.14, relx=0.82, relheight=0.06, relwidth=0.176)

        self.ExportCSVButton = customtkinter.CTkButton(self.mid_frame, text="Export to CSV",command=self.ExportToCSV)
        self.ExportCSVButton.place(rely=0.805, relx=0.55, relheight=0.06, relwidth=0.12)
        self.ExportExcelButton = customtkinter.CTkButton(self.mid_frame, text="Export to Excel",
                                                         command=lambda: threading.Thread(target=self.ExportToExcel).start())#didnt fix the lag :(
        self.ExportExcelButton.place(rely=0.805, relx=0.68, relheight=0.06, relwidth=0.12)#move later

        #first loading data
        self.ProgressBar.set(0)
        self.StandardMode.invoke()
        self.AllStatus.invoke()
        if self.folder_selected is not None and len(self.folder_selected) > 0:
            self.LabelSongFolder.configure(text=str(self.folder_selected))
            self.AnalyzeMySongs()
        if self.ApiV1 and len(self.ApiV1)>3 :# and the check box
            self.ApiKeyPresentLabel.configure(text="Api v1: Present!")
            if self.AutoUpdate=='1':
                self.CheckAutoUpdate.select()
                updateData = threading.Thread(target=CollectMissingData, args=(self.ApiV1.split('\n')[0],))
                updateData.start()


    #MY FUNCS
    def SetUpdateDataLabelText(self,text:str):
        self.UpdateLabel.configure(text=text)
    def UpdateData(self):
        updateData = threading.Thread(target=CollectMissingData,args=(self.ApiV1.split('\n')[0],))
        updateData.start()
    def InputApiKey(self):
        apiv1Key = tk.simpledialog.askstring(title="Input Api v1", prompt="What's your API V1:")
        if apiv1Key is not None and len(apiv1Key)>2:
            self.ApiV1 = apiv1Key
            self.SaveConfig()
    def cleardata(self):
        self.tree.delete(*self.tree.get_children())
        self.tree['columns'] = []
    def filter_By_Date(self,MinDate,MaxDate):
        mindate = datetime.strptime(MinDate, "%m/%d/%y").strftime('%Y-%m-%d')
        maxdate = datetime.strptime(MaxDate, "%m/%d/%y").strftime('%Y-%m-%d')
        if not mindate<'2007-01-02' :      # approved_date
            self.df = self.df[self.df['approved_date'] >= mindate]
        if not maxdate==datetime.now().strftime('%Y-%m-%d'):
            self.df = self.df[self.df['approved_date'] <= maxdate]
    def filter_By_md5Hash(self, file_md5: str):
        self.df = self.df[self.df['file_md5']==file_md5]
    def filter_By_Title(self,title:str,Exact: bool):
        if Exact:
            self.df = self.df[self.df['title'] == title]
        else:
            self.df = self.df[self.df['title'].str.lower().str.contains(title.lower(),na=False)]
    def filter_By_Version(self,version:str,Exact: bool):
        if Exact:
            self.df = self.df[self.df['version'] == version]
        else:
            self.df = self.df[self.df['version'].str.lower().str.contains(version.lower(), na=False)]
    def filter_By_Artist(self,artist : str,Exact : bool):
        if Exact:
            self.df = self.df[self.df['artist'] == artist]
        else:
            self.df = self.df[self.df['artist'].str.lower().str.contains(artist.lower(), na=False)]
    def filter_By_Creator(self,creator:str,Exact: bool):
        if Exact:
            self.df = self.df[self.df['creator'] == creator]
        else:
            self.df = self.df[self.df['creator'].str.lower().str.contains(creator.lower(), na=False)]
    def filter_By_Beatmapset_Id(self,beatmapset_id:int):
        self.df = self.df[self.df['beatmapset_id'] == beatmapset_id]
    def filter_By_Beatmap_Id(self,beatmap_id:int):
        self.df = self.df[self.df['beatmap_id'] == beatmap_id]
    def filter_By_Length(self,MinLength=0,MaxLength=864000):
        if MinLength > 0:
            self.df = self.df[self.df['total_length'] >= MinLength]
        if MaxLength < 864000:
            self.df = self.df[self.df['total_length'] <= MaxLength]
    def filter_By_BPM(self,MinBPM=0.0,MaxBPM=12000.0):
        if MinBPM > 0.0:
            self.df = self.df[self.df['bpm'] >= MinBPM]
        if MaxBPM < 12000.0:
            self.df = self.df[self.df['bpm'] <= MaxBPM]
    def filter_By_CS(self,MinCS=0.0,MaxCS=11.0):
        if MinCS > 0.0:
            self.df = self.df[self.df['diff_size'] >= MinCS]
        if MaxCS < 11.0:
            self.df = self.df[self.df['diff_size'] <= MaxCS]
    def filter_By_OD(self,MinOD=0.0,MaxOD=12.0):
        if MinOD > 0.0:
            self.df = self.df[self.df['diff_overall'] >= MinOD]
        if MaxOD < 12.0:
            self.df = self.df[self.df['diff_overall'] <= MaxOD]
    def filter_By_AR(self,MimAr=0.0,MaxAr=12.1):
        if MimAr > 0.0:
            self.df = self.df[self.df['diff_approach'] >= MimAr]
        if MaxAr < 12.1:
            self.df = self.df[self.df['diff_approach'] <= MaxAr]
    def filter_By_HP(self,MinHP=0.0,MaxHP=12.1):
        if MinHP > 0.0:
            self.df = self.df[self.df['diff_drain'] >= MinHP]
        if MaxHP < 12.1:
            self.df = self.df[self.df['diff_drain'] <= MaxHP]
    def filter_By_DiffAim(self,MinDiffAim=0.0,MaxDiffAim=12.1):
        if MinDiffAim>0.0:
            self.df = self.df[self.df['diff_aim'] >= MinDiffAim]
        if MaxDiffAim<12.1:
            self.df = self.df[self.df['diff_aim'] <= MaxDiffAim]
    def filter_By_DiffSpeed(self,MinDiffSpeed=0.0,MaxDiffSpeed=12.1):
        if MinDiffSpeed > 0:
            self.df = self.df[self.df['diff_speed'] >= MinDiffSpeed]
        if MaxDiffSpeed < 12.1:
            self.df = self.df[self.df['diff_speed'] <= MaxDiffSpeed]
    def filter_By_Stars(self,MinStars=0.0,MaxStars=25.0):
        if MinStars > 0.0:
            self.df = self.df[self.df['difficultyrating'] >= MinStars]
        if MaxStars < 25.0:
         self.df = self.df[self.df['difficultyrating'] <= MaxStars]
    def filter_By_MaxCombo(self,MinMaxCombo=0,MaxMaxCombo=100000):
        if MinMaxCombo > 0:
            self.df = self.df[self.df['max_combo'] >= MinMaxCombo]
        if MaxMaxCombo < 100000:
            self.df = self.df[self.df['max_combo'] <= MaxMaxCombo]
    def filter_By_PlayCount(self,MinPlayCount=0,MaxPlayCount=2100000000):
        if MinPlayCount > 0:
            self.df = self.df[self.df['playcount'] >= MinPlayCount]
        if MaxPlayCount < 2100000000:
            self.df = self.df[self.df['playcount'] <= MaxPlayCount]
    def filter_By_ApprovedDate(self,MinDate="1970-01-01 01:01:01",MaxDate="2038-01-01 01:01:01"):
        if MinDate > "1970-01-01 01:01:01":
            self.df = self.df[self.df['approved_date']>=MinDate]
        if MaxDate < "2038-01-01 01:01:01":
            self.df = self.df[self.df['approved_date']<=MaxDate]

    def SaveConfig(self):
        if self.AutoUpdateCheck.get()=='1':
            self.AutoUpdate='1'
        else:
            self.AutoUpdate='0'
        Save="SaveDirectory::"+self.folder_selected+"\n"
        Save+="ApiV1::"+self.ApiV1+'\n'
        Save+="AutoUpdate::"+self.AutoUpdate
        with open('Config.txt','w') as file:
            file.truncate()
            file.write(Save)

    def getSongFolder(self):
        self.folder_selected = filedialog.askdirectory()
        self.LabelSongFolder.configure(text=str(self.folder_selected))
        self.AnalyzeMySongs()
        self.SaveConfig()

    def AnalyzeMySongs(self):
        self.Songs=[]
        try:
            try:
                for subdir in os.listdir(self.folder_selected):
                    if subdir.split(" ")[0].isnumeric():
                        self.Songs.append(int(subdir.split(" ")[0]))
            except:
                pass
            try:
                for subdir in os.listdir("Downloads/"):
                    if subdir.split(" ")[0].isnumeric():
                        self.Songs.append(int(subdir.split(" ")[0]))
            except:
                pass
            self.LabelMySongsNum.configure(text=f"My Songs:{len(self.Songs)}")
            self.check_matching()
        except:
            pass
    #SOURCE FUNCS
    def button_event(self):
        self.test(Limited=False)

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()
    def OriginalDataExtract(self):
        try:
            if self.ModeType.get()=='1':
                return pd.read_csv('data/standard.csv',encoding='utf-8')
            if self.ModeType.get()=='2':
                return pd.read_csv('data/Taiko.csv', encoding='utf-8')
            if self.ModeType.get()=='3':
                return pd.read_csv('data/CtB.csv', encoding='utf-8')
            if self.ModeType.get()=='4':
                return pd.read_csv('data/osu!mania.csv', encoding='utf-8')
        except:
            pass
    def FilterdfData(self):
        if self.Status.get() == '2':
            self.OriginalData=self.OriginalData[self.OriginalData['State']==1]
        if self.Status.get() == '3':
            self.OriginalData=self.OriginalData[self.OriginalData['State']==4]
        if self.Status.get() == '4':
            self.OriginalData=self.OriginalData[self.OriginalData['State']==2]
    def FilterOriginalData(self):
        self.OriginalData = self.OriginalDataExtract()
        self.FilterdfData()
        self.test()
    def test(self, Limited = True):
        def IsFloat(NumberSTR: str):
            try:
                float(NumberSTR)
                return True
            except:
                return False

        temptime = time.time()
        try:
            self.df=self.OriginalData.copy()
        except:
            self.df=pd.DataFrame()
        self.cleardata()
        #date
        self.filter_By_Date(self.MinDate.get(),self.MaxDate.get())
        #exacts
        if self.MD5Hash.get() !='':
            self.filter_By_md5Hash(file_md5=self.MD5Hash.get())
        if self.BeatmapSetId.get().isnumeric():
            self.filter_By_Beatmapset_Id(beatmapset_id=int(self.BeatmapSetId.get()))
        if self.BeatmapID.get().isnumeric():
            self.filter_By_Beatmap_Id(beatmap_id=int(self.BeatmapID.get()))
        #end of exacts
        #row 1
        if self.Title.get() !='':
            if self.CheckTitle.get()=='1':
                self.filter_By_Title(title=self.Title.get(), Exact=True)
            else:
                self.filter_By_Title(title=self.Title.get(),Exact=False)
        if self.DifficultyName.get() !='':
            if self.CheckDifficulty.get() == '1':
                self.filter_By_Version(version=self.DifficultyName.get(),Exact=True)
            else:
                self.filter_By_Version(version=self.DifficultyName.get(), Exact=False)
        if self.Artist.get() !='':
            if self.CheckArtist.get() == '1':
                self.filter_By_Artist(artist=self.Artist.get(),Exact=True)
            else:
                self.filter_By_Artist(artist=self.Artist.get(), Exact=False)
        if self.Creator.get() !='':
            if self.CheckCreator.get() == '1':
                self.filter_By_Creator(creator=self.Creator.get(),Exact=True)
            else:
                self.filter_By_Creator(creator=self.Creator.get(), Exact=False)
        #end of row 1
        #row 2
        if IsFloat(self.MinBPM.get()):
            self.filter_By_BPM(MinBPM=float(self.MinBPM.get()))
        if IsFloat(self.MaxBPM.get()):
            self.filter_By_BPM(MaxBPM=float(self.MaxBPM.get()))
        if IsFloat(self.MinAR.get()):
            self.filter_By_AR(MimAr=float(self.MinAR.get()))
        if IsFloat(self.MaxAR.get()):
            self.filter_By_AR(MaxAr=float(self.MaxAR.get()))
        if IsFloat(self.MinOD.get()):
            self.filter_By_OD(MinOD=float(self.MinOD.get()))
        if IsFloat(self.MaxOD.get()):
            self.filter_By_OD(MaxOD=float(self.MaxOD.get()))
        if IsFloat(self.MinCS.get()):
            self.filter_By_CS(MinCS=float(self.MinCS.get()))
        if IsFloat(self.MaxCS.get()):
            self.filter_By_CS(MaxCS=float(self.MaxCS.get()))
        if IsFloat(self.MinHP.get()):
            self.filter_By_HP(MinHP=float(self.MinHP.get()))
        if IsFloat(self.MaxHP.get()):
            self.filter_By_HP(MaxHP=float(self.MaxHP.get()))

        if IsFloat(self.MinSTARS.get()):
            self.filter_By_Stars(MinStars=float(self.MinSTARS.get()))
        if IsFloat(self.MaxSTARS.get()):
            self.filter_By_Stars(MaxStars=float(self.MaxSTARS.get()))
        #end of row 2
        #row 3
        if self.MinLength.get().isnumeric():
            self.filter_By_Length(MinLength=int(self.MinLength.get()))
        if self.MaxLength.get().isnumeric():
            self.filter_By_Length(MaxLength=int(self.MaxLength.get()))
        if self.MinPlaycount.get().isnumeric():
            self.filter_By_PlayCount(MinPlayCount=int(self.MinPlaycount.get()))
        if self.MaxPlaycount.get().isnumeric():
            self.filter_By_PlayCount(MaxPlayCount=int(self.MaxPlaycount.get()))
        if self.MinMaxCombo.get().isnumeric():
            self.filter_By_MaxCombo(MinMaxCombo=int(self.MinMaxCombo.get()))
        if self.MaxMaxCombo.get().isnumeric():
            self.filter_By_MaxCombo(MaxMaxCombo=int(self.MaxMaxCombo.get()))
        if IsFloat(self.MinStarsAim.get()):
            self.filter_By_DiffAim(MinDiffAim=float(self.MinStarsAim.get()))
        if IsFloat(self.MaxStarsAim.get()):
            self.filter_By_DiffAim(MaxDiffAim=float(self.MaxStarsAim.get()))
        if IsFloat(self.MinStarsSpeed.get()):
            self.filter_By_DiffSpeed(MinDiffSpeed=float(self.MinStarsSpeed.get()))
        if IsFloat(self.MaxStarsSpeed.get()):
            self.filter_By_DiffSpeed(MaxDiffSpeed=float(self.MaxStarsSpeed.get()))
        #end of row 3
        # start of insertion
        if self.ModeType.get()=='1':
            self.tree["column"] = ["MD5 Hash","Title","Difficulty Name","Artist","Creator","BeatmapSetId","BeatmapId","Length",
                               "BPM","CS","OD","AR","HP","AIM*","SPEED*","STARS","MaxCombo","Playcount","DateApproved"]
        elif self.ModeType.get()=='2' or self.ModeType.get()=='3':
            self.tree["column"] = ["MD5 Hash","Title","Difficulty Name","Artist","Creator","BeatmapSetId","BeatmapId","Length",
                               "BPM","CS","OD","AR","HP","STARS","MaxCombo","Playcount","DateApproved"]
        elif self.ModeType.get()=='4':
            self.tree["column"] = ["MD5 Hash","Title","Difficulty Name","Artist","Creator","BeatmapSetId","BeatmapId","Length",
                               "BPM","CS","OD","AR","HP","STARS","Playcount","DateApproved"]
        self.tree["show"] = "headings"
        # headers
        for column in self.tree["column"]:
            self.tree.heading(column, text=column)
        # data
        self.df_rows = self.df.to_numpy().tolist()
        if Limited:
            for row in self.df_rows:
                self.tree.insert("", "end", values=row)
                if len(self.tree.get_children())>249:
                    break
        else:
            for row in self.df_rows:
                self.tree.insert("", "end", values=row)
        self.LabelDisplayed.configure(text= "Displayed: "+str(len(self.tree.get_children())))
        self.LabelOverall.configure(text="Overall: "+str(len(self.df)))
        self.LabelSearchTime.configure(text=f"Search in: {round(time.time()-temptime,2)}sec.")
        self.AnalyzeMySongs()
        #self.LabelMatching.configure(text=f"Matching Sets:{len(self.Matching)}")
    def check_matching(self):
        for k,v in self.df.items():
            if k == "beatmapset_id":
                temp = len(set(v))
                self.DownloadSongsList = list(set(v)-set(self.Songs))
                self.LabelMatching.configure(text=f"Matching Sets:{len(set(self.Songs)-(set(self.Songs)-set(v)))}")
        self.LabelMissing.configure(text=f"Missing Sets:{len(self.DownloadSongsList)}")
        self.ProgressBar.set(1 - (len(self.DownloadSongsList) / temp))
        try:
            self.LabelDownloadPerc.configure(text=f'{round((1 - (len(self.DownloadSongsList) / temp))*100, 1)}%')
        except:
            self.LabelDownloadPerc.configure(text=f'100%')
    def GetLabelMatching(self):
        return self.LabelMatching.text
    def GetDownloadList(self):
        return [self.DownloadSongsList[x:x + 5]for x in range(0, len(self.DownloadSongsList), 5)]
    def DownloadMaps(self):
        self.DownloadSongsList.sort()
        DownloadThread= threading.Thread(target=StartDownload,args=(self.api,self.folder_selected))
        DownloadThread.start()
    # def SetDownloaded(self):
    #     self.downloadedMaps+=1
    # def Progress(self):
    #     a= int(self.GetLabelMatching().split(':')[1])
    #     b= len(self.DownloadSongsList)
    #     self.LabelMissing.configure(text=f"Missing Sets:{a-b}")
    #     print(a,b)
    #     self.ProgressBar.set(1-(b/a))
    #     self.LabelDownloadPerc.configure(text=f'{round((b/a)*100,1)}%')
    def ProgressFinish(self):
        self.LabelMissing.configure(text=f"Missing Sets:{0}")
        self.ProgressBar.set(1)
        self.downloadedMaps=0
        self.LabelDownloadPerc.configure(text='100%')
    def UpdateCSVExportTimer(self,temptime):
        self.ExportLabel.configure(text=f"Exported in:{round(time.time() - temptime, 2)}sec")
    def ExportToCSV(self):
        toCSVThread = threading.Thread(target=ToCSV, args=(self.df,))
        toCSVThread.start()
    def ExportToExcel(self):
        toExcelThread = threading.Thread(target=ToExcel,args=(self.df,))
        toExcelThread.start()
def ToExcel(df):
    temptime = time.time()
    os.makedirs('Exports', exist_ok=True)
    dt_string = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    df.to_excel(f"Exports\\{dt_string}.xlsx", encoding="utf-8")
    app.UpdateCSVExportTimer(temptime)
def ToCSV(df):
    temptime = time.time()
    os.makedirs('Exports', exist_ok=True)
    dt_string = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    df.to_csv(f"Exports\\{dt_string}.csv", encoding="utf-8")
    app.UpdateCSVExportTimer(temptime)
def StartDownload(api,folder):
    app.AnalyzeMySongs()
    DownloadList = app.GetDownloadList()
    if folder and len(folder)>2:
        folder+="/"
    else:
        folder = "Downloads/"
    i=0
    for Col in DownloadList:
        i += len(Col)
        for mapset in Col:
            download_thread = threading.Thread(target=download,
                                               args=(api + str(mapset), folder + str(mapset)+' SBD' + '.osz'))
            download_thread.start()
        download_thread.join()
        app.AnalyzeMySongs()
    app.ProgressFinish()

def download(link, filelocation):
    r = requests.get(link, stream=True)
    with open(filelocation, 'wb') as f:
        for chunk in r.iter_content(1024):
            if chunk:
                f.write(chunk)
def createNewDownloadThread(link, filelocation):
     download_thread = threading.Thread(target=download, args=(link,filelocation))
     download_thread.start()
def ExtractForStandardCSV(data:list):
    SaveData=[]
    for k in data:
        SaveData.append(
                [k['file_md5'], k['title'], k['version'], k['artist'], k['creator'], str(k['beatmapset_id']),
                 str(k['beatmap_id']), str(k['total_length']), str(round(float(k['bpm']))), str(k['diff_size']),
                 str(k['diff_overall']),
                 str(k['diff_approach']), str(k['diff_drain']), str(round(float(k['diff_aim']), 2)),
                 str(round(float(k['diff_speed']), 2)), str(round(float(k['difficultyrating']), 2)),
                 str(k['max_combo']), str(k['playcount']), str(k['approved_date']),int(k['approved'])])
    return SaveData

def ExtractForTaikoAndCTB_CSV(data:list):
    SaveData = []
    for k in data:
        SaveData.append(
                [k['file_md5'], k['title'], k['version'], k['artist'], k['creator'], str(k['beatmapset_id']),
                 str(k['beatmap_id']), str(k['total_length']), str(round(float(k['bpm']))), str(k['diff_size']),
                 str(k['diff_overall']),str(k['diff_approach']), str(k['diff_drain']),
                 str(round(float(k['difficultyrating']), 2)),str(k['max_combo']), str(k['playcount']),
                 str(k['approved_date']),int(k['approved'])])
    return SaveData
def ExtractForManiaCSV(data:list):
    SaveData = []
    for k in data:
        SaveData.append(
                [k['file_md5'], k['title'], k['version'], k['artist'], k['creator'], str(k['beatmapset_id']),
                 str(k['beatmap_id']), str(k['total_length']), str(round(float(k['bpm']))), str(k['diff_size']),
                 str(k['diff_overall']), str(k['diff_approach']), str(k['diff_drain']),
                 str(round(float(k['difficultyrating']), 2)), str(k['playcount']), str(k['approved_date']),int(k['approved'])])
    return SaveData

def CheckFile(Name):
    try:
        tempData = pd.read_csv('data/'+Name+'.csv',encoding='utf-8')
        if len(tempData) > 0:
            if len(tempData['approved_date'].max()) > 0:
                return True
        return False
    except:
        return False
def CollectMissingData(ApiV1:str):
    today = datetime.today().strftime('%Y-%m-%d')
    GameModes = ["standard", "Taiko", "CtB", "osu!mania"]
    mode = 0
    for GameMode in GameModes:
        date = "2007-10-06 00:00:00"
        if GameMode == "standard":
            last=''
            if CheckFile(GameMode):
                df = pd.read_csv("data/"+GameMode+'.csv',encoding='utf-8')
                date = df['approved_date'].max()
            else:
                df = pd.DataFrame(columns=(
                "file_md5", "title", "version", "artist", "creator", "beatmapset_id", "beatmap_id",
                "total_length", "bpm", "diff_size", "diff_overall", "diff_approach", "diff_drain",
                "diff_aim", "diff_speed", "difficultyrating", "max_combo", "playcount", "approved_date", "State"))
            while datetime.strptime(date, "%Y-%m-%d %H:%M:%S") <= datetime.strptime(today, "%Y-%m-%d"):
                date = str(datetime.strptime(date, "%Y-%m-%d %H:%M:%S")-timedelta(minutes=1))
                test = apiV1.get_beatmaps(key=ApiV1, since=date, mode=mode)
                temp = pd.DataFrame(ExtractForStandardCSV(test),columns=(
                        "file_md5", "title", "version", "artist", "creator", "beatmapset_id", "beatmap_id",
                        "total_length", "bpm", "diff_size", "diff_overall", "diff_approach", "diff_drain",
                        "diff_aim", "diff_speed", "difficultyrating", "max_combo", "playcount", "approved_date", "State"))
                #df = df.append(temp,ignore_index=True)
                df = pd.concat([df,temp],ignore_index=True)
                date = df['approved_date'].max()
                app.SetUpdateDataLabelText(GameMode + ": " + df['approved_date'].max() + " " + str(len(test)) + " maps")


                if last!= date:
                    last=date
                else:
                    break
            df.drop_duplicates(inplace=True)
            df.to_csv("data/"+GameMode+'.csv',encoding='utf-8',index=False)
        elif GameMode == "Taiko" or GameMode == "CtB":
            last = ''
            if CheckFile(GameMode):
                df = pd.read_csv("data/"+GameMode + '.csv', encoding='utf-8')
                date = df['approved_date'].max()
            else:
                df = pd.DataFrame(columns=(
                    "file_md5", "title", "version", "artist", "creator", "beatmapset_id", "beatmap_id",
                    "total_length", "bpm", "diff_size", "diff_overall", "diff_approach", "diff_drain",
                    "difficultyrating", "max_combo", "playcount", "approved_date", "State"))
            while datetime.strptime(date, "%Y-%m-%d %H:%M:%S") <= datetime.strptime(today, "%Y-%m-%d"):
                date = str(datetime.strptime(date, "%Y-%m-%d %H:%M:%S") - timedelta(minutes=1))
                test = apiV1.get_beatmaps(key=ApiV1, since=date, mode=mode)
                temp = pd.DataFrame(ExtractForTaikoAndCTB_CSV(test), columns=(
                    "file_md5", "title", "version", "artist", "creator", "beatmapset_id", "beatmap_id",
                    "total_length", "bpm", "diff_size", "diff_overall", "diff_approach", "diff_drain",
                    "difficultyrating", "max_combo", "playcount", "approved_date", "State"))
                df = pd.concat([df, temp], ignore_index=True)
                date = df['approved_date'].max()
                app.SetUpdateDataLabelText(GameMode + ": " + df['approved_date'].max()+ " " + str(len(test)) + " maps")
                if last!= date:
                    last=date
                else:
                    break
            df.drop_duplicates(inplace=True)
            df.to_csv("data/"+GameMode + '.csv', encoding='utf-8', index=False)
        elif GameMode == "osu!mania":
            last = ''
            if CheckFile(GameMode):
                df = pd.read_csv("data/"+GameMode + '.csv', encoding='utf-8')
                date = df['approved_date'].max()
            else:
                df = pd.DataFrame(columns=(
                    "file_md5", "title", "version", "artist", "creator", "beatmapset_id", "beatmap_id",
                    "total_length", "bpm", "diff_size", "diff_overall", "diff_approach", "diff_drain",
                    "difficultyrating", "playcount", "approved_date", "State"))
            while datetime.strptime(date, "%Y-%m-%d %H:%M:%S") <= datetime.strptime(today, "%Y-%m-%d"):
                date = str(datetime.strptime(date, "%Y-%m-%d %H:%M:%S") - timedelta(minutes=1))
                test = apiV1.get_beatmaps(key=ApiV1, since=date, mode=mode)
                temp = pd.DataFrame(ExtractForManiaCSV(test),  columns=(
                    "file_md5", "title", "version", "artist", "creator", "beatmapset_id", "beatmap_id",
                    "total_length", "bpm", "diff_size", "diff_overall", "diff_approach", "diff_drain",
                    "difficultyrating", "playcount", "approved_date", "State"))
                df = pd.concat([df, temp], ignore_index=True)
                date = df['approved_date'].max()
                app.SetUpdateDataLabelText(GameMode + ": " + df['approved_date'].max()+ " " + str(len(test)) + " maps")
                if last!= date:
                    last=date
                else:
                    break
            df.drop_duplicates(inplace=True)
            df.to_csv("data/"+GameMode + '.csv', encoding='utf-8', index=False)
        mode+=1
    app.SetUpdateDataLabelText("UPDATED!")
if __name__ == "__main__":
    app = App()
    app.mainloop()