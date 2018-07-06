###################################################################
#                   WhiteLight Interferometer Program             #
#                   Created by : Nicolas Perron                   #
#                   For : Ultrafast and Quantum
#!/usr/bin/python3
# -*- coding: utf-8 -*-

#Importing package:
# Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
#Sub_Programs
import Sub_Programs as SP
from Sub_Programs import WL_backend as backend
#Pathlib
from pathlib import Path
#Zurich Instrumente Librairies:
import zhinst.utils as utils
import zhinst.Save_Zi as Save_Zi
#Os python package:
import os
#Font Size
LARGE_FONT = ("Arial", 12)
NORM_FONT = ("Arial", 10)
SMALL_FONT = ("Arial", 8)

class White_Light_Inteferometer(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        Dir = Path.cwd()
        self.PI_Data = None
        self.Zi_Data = None
        Ima = tk.PhotoImage(file = Dir/'FMQ3.gif')
        tk.Tk.wm_title(self, "White Light Interferometer V0.2")
        tk.Tk.wm_iconphoto(self, '-default' ,Ima)
        ##### Frame switching function:
        def Switch_Frame(lst, Box, rw, clm):
            Current = Box.get()
            for element in lst:
                lst[element].grid_forget()

            for element in lst:
                if element == Current:
                    lst[element].configure(labelwidget = Box)
                    lst[element].grid(row = rw, column = clm,
                            padx = 2, pady = 2,sticky = 'nsew')
                else: pass


        #Variable for screen dimension & variables
        txtvar = tk.StringVar()
        global width
        global height

        #Needs to be ajustable(modification to come)
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        #Initialisation of different elements
        Mainframe = ttk.Frame(self, padding = (6,6,6,6))
        GraphBox = backend.Graphic(parent = Mainframe, width = 175,
                height = 150)
        CCBox = ttk.Combobox(Mainframe, textvariable = '',
                state = 'readonly')
        CCBox.grid(row = 0, column = 0,sticky = 'nw')
        CCBox['value'] = ('PI Module Connection','ZI Module connection')
        CCBox.current(0)
        SCBox = ttk.Combobox(Mainframe, textvariable = '',
                state = 'readonly')
        SCBox.grid(row = 0, column = 0,sticky = 'nw')
        SCBox['value'] = ('PI Module Settings','ZI Module Settings')
        SCBox.current(0)
        File_Dialog = backend.File_interaction(Mainframe,
                "File interaction")
        self.ZiFrame = backend.Zi_Connection_Method(Mainframe,CCBox)
        self.frame = backend.PI_Connection_Method(Mainframe,
                CCBox)
        self.PI_Control = backend.PI_control(Mainframe,SCBox)
        self.ZI_Control = backend.Zi_settings(Mainframe, SCBox)
        Flist1 = {'PI Module Connection': self.frame,
                'ZI Module connection' : self.ZiFrame}
        Flist2 = {'PI Module Settings': self.PI_Control,
                'ZI Module Settings': self.ZI_Control}
        CCBox.bind("<<ComboboxSelected>>",
            lambda x : Switch_Frame(Flist1,CCBox,0,0))
        SCBox.bind("<<ComboboxSelected>>",
            lambda x : Switch_Frame(Flist2,SCBox,1,0))
        Switch_Frame(Flist1,CCBox,0,0)
        Switch_Frame(Flist2,SCBox,1,0)
        #Mainframe configuration
        Mainframe.grid(row = 0, column = 0)
        #GraphBox configuration
        GraphBox.create_text(175/2, 75, text = "Awesome Graph",font
            = LARGE_FONT, fill = "black")
        GraphBox.grid(row = 0, column = 1, padx = 5, pady = 5)
        #File location/reading configuration
        File_Dialog.grid(row = 1, column = 1, padx = 2, pady = 2)

        File_Dialog.Start.bind('<Button-1>',
                    lambda : self.Start( self.PI_Data, self.Zi_Data))

        File_Dialog.OpBut.bind('<Button-1>',
                    lambda : self.Load_Setting(
                        File_Dialog.DirVar, self.PI_Data,
                        self.Zi_Data))

        File_Dialog.SvBut.bind('<Button-1>',
                    lambda : self.Save_Setting(
                        File_Dialog.DirVar,
                        File_Dialog.File_InDir, self.PI_Data,
                        self.Zi_Data))

        File_Dialog.Stop.bind('<Button-1>',
                    lambda : self.Stop_Measurement(
                        self.PI_Data,
                        self.Zi_Data))



    def Start(self, File_List, Dir,PI_Data, Zi_Data):
        print('hello')

    def Save_Setting(self, Folder, PI_Data, ZI_Data):

        def Save(Dir, ZI_Data, PI_Data):
            utils.save_settings( ZI_Data['DAQ'],
                    ZI_Data['Device_id'].get(),
                    Dir.get()+os.sep+'_zi_settings.xml')


        if PI_Data or ZI_Data is None:
            messabox.showinfo(icon = 'error', title = 'WARNING',
                    message = 'One of the device is not connected')
        elif Dir.get() == '':
            messabox.showinfo(icon = 'error', title = 'WARNING',
                    message = 'Please Choose a directory')
        else:
            Save( Folder, ZI_Data, PI_Data)
            messabox.showinfo( title = 'Information',
                    message = 'Settings as been saved to the'+
                    'desiered folder.')

    def Load_Setting(self, Folder, PI_Data, ZI_Data):

        def Load(Dir, ZI_Data, PI_Data):
            utils.load_settings( ZI_Data['DAQ'],
                    ZI_Data['Device_id'].get(),
                    Dir.get()+os.sep+'_zi_settings.xml')


        if PI_Data or ZI_Data is None:
            messabox.showinfo(icon = 'error', title = 'WARNING',
                    message = 'One of the device is not connected')
        elif Dir.get() == '':
            messabox.showinfo(icon = 'error', title = 'WARNING',
                    message = 'Please choose a directory')
        else:
            Load( Folder, ZI_Data, PI_Data)
            messabox.showinfo( title = 'Information',
                    message = 'Settings as been saved to the'+
                    'desiered folder.')

    def Stop_Measurement(self, ):
        print('stop')

def Refresh(app, Frame, receiver):
    if app.Frame.connected==False:
        app.after(1000, Refresh, app, Frame, receiver)
    else:
        if app.Frame == app.frame:
            app.PI_Control.Devices = app.frame.Devices_connected
            app.PI_Data = app.PI_Control.Show_device()
        elif app.Frame == app.ZiFrame:
            app.ZI_Control(DAQ = app.ZiFrame.DAQ,
                    Device = app.ZiFrame.device,
                    Prop = app.ZiFrame.proprieties)
            app.Zi_Data = app.ZI_Control.Zi_Setting_List

app = White_Light_Inteferometer()
app.frame.CbmBox.bind("<<ComboboxSelected>>",app.frame.Meth_show)

app.frame.CButton.bind('<Button-1>', lambda x : Refresh(app, frame,
    PI_Control ))
app.ZiFrame.CButton.bind('<Button-1>', lambda x : Refresh(app,
    ZiFrame, ZI_Control))

app.geometry("+{}+{}".format(int(width/5),int(height/5)))
app.mainloop()

