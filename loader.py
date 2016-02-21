#!/usr/bin/python3

import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import shutil
import json
import os
from os import listdir
from os.path import isfile, join

import jbpp 

VERSION = 1

class App(object):
    def __init__(self):
        """ init application """
        self.root = tkinter.Tk()
        self.root.title("JBPP Mod Loader")
        
        ttk.Style().theme_use('clam')
        
        #self.root.minsize(width=400, height=300)
        self.conf = None
        self.applied_patches = {}
        
        self.get_patches()
        self.load_config()
        self.main_screen()


    def main_screen(self):
        frmPatches = ttk.Frame(self.root)
        frmPatches.pack(expand=YES, fill='both')
        
        for game in self.patches.keys():
            frmGame = ttk.Frame(frmPatches)
            frmGame.pack(expand=NO, fill='x')
            
            ttk.Label(frmGame, text=game).pack()
            ttk.Radiobutton(frmGame, text='None', variable=self.applied_patches[game], value="").pack(pady=8, padx=8, side=LEFT)
            for p in self.patches[game]:
                ttk.Radiobutton(frmGame, text=p["info"]["name"], variable=self.applied_patches[game], value=p["file"]).pack(pady=8, padx=8, side=LEFT)
                
        
        frm = ttk.Frame(self.root)
        frm.pack(expand=NO, fill='both')

        btnLoad = ttk.Button(frm, text = 'Start')
        btnLoad['command'] = self.load_game
        btnLoad.pack(pady=8, padx=8, side=RIGHT)
        
        
    def get_patches(self):
        patchfiles = [f for f in listdir(".") if isfile(join(".", f)) and f.endswith(".jbp")]
        self.patches = {}
        for p in patchfiles:
            try:
                info = jbpp.patch_info(p)
                self.patches.setdefault(info["game"], []).append({"file": p, "info": info})
            except:
                # invalid patch
                pass
            
               
        for game in self.patches.keys():
            self.applied_patches[game] = tkinter.StringVar()
            self.applied_patches[game].set("")
        print(self.patches)
        
        
    def find_patch_by_file(self, name):
        for p in self.patches:
            for patch in self.patches[p]:
                if patch["file"] == name:
                    return (p, patch)
        return (None, None)
        
        
    def load_config(self):
        if not os.path.isfile("loader.conf"):
            return
        
        try:
            with open("loader.conf") as f:
                self.conf = json.load(f)
                if self.conf["v"] < VERSION:
                    return
        except:
            return
        
        for a in self.conf["patches"]:
            game, _ = self.find_patch_by_file(a)
            if game: self.applied_patches[game].set(a)
        

    def save_config(self, active):
        with open("loader.conf", "w") as f:
            json.dump({"v": VERSION, "patches": active}, f)
    
    
    def config_changed(self, active):
        if not self.conf: return True
        return set(active) != set(self.conf["patches"])
    
    
    def load_game(self):
        active = []
        for p in self.applied_patches:
            val = self.applied_patches[p].get()
            if val != '': active.append(val)
        
        if self.config_changed(active):
            toplevel = Toplevel()
            label1 = Label(toplevel, text="Please wait, applying patches...")
            label1.pack(padx=16, pady=16)
            self.root.update()        
            
            self.save_config(active)
            # check for original assets
            if not os.path.isfile("assets.bin.orig"):
                shutil.move("assets.bin", "assets.bin.orig")
            # extract
            jbpp.uncompress("assets.bin.orig")
            # apply all patches
            for p in active:
                jbpp.apply_patch(p)
            # assemble again
            jbpp.compress("assets.bin")
            # start
            toplevel.destroy()
            self.root.update()
            
            os.system("./tjpp.exe")
            self.root.destroy()
            
        else:
            # just start the game
            os.system("./tjpp.exe")
            self.root.destroy()
            
app = App()
app.root.mainloop()
