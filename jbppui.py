#!/usr/bin/python3

import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory
from tkinter import simpledialog
from tkinter import messagebox
from shutil import copyfile
import json
import os
import io
import zipfile
import copy

import jbpp

TEXTBOX = 1
CHECKBOX = 2
FILE = 3
OPTIONALFILE = 4

CONTENT = 1
QUESTION = 2

QUESTION_TO_CONTENT = 1
CONTENT_TO_QUESTION = 2

        
class CheckVar(Variable):
    _default = 0
    def __init__(self, master=None, value=None, name=None, on_val = True, off_val = False, field=None, ui = None):
        Variable.__init__(self, master, value, name)
        self._on_val = on_val
        self._off_val = off_val
        self._ui = ui
        self._field = field

    def set(self, val):
        self._tk.globalsetvar(self._name, 1 if val == self._on_val or val == 1 or val is True else 0)
        self.check_dependency()

    def get(self):
        value = self._tk.globalgetvar(self._name)
        return self._on_val if self._tk.getint(value) == 1 else self._off_val
    
    def check_dependency(self):
        if self._ui is not None:
            for u in self._ui:
                if u["depends"] == self._field:
                    u["handle"].configure(state="enabled" if self._tk.getint(self._tk.globalgetvar(self._name)) == 1 else "disabled")
                if u["depends"] == "!" + self._field:
                    u["handle"].configure(state="disabled" if self._tk.getint(self._tk.globalgetvar(self._name)) == 1 else "enabled")
    
    def cb(self):
        self.check_dependency()
        


class JBPPUI(object):
    def __init__(self):
        """ init application """
        self.root = tkinter.Tk()
        self.question = None
        self.root.title("JBPP Question Editor")
        
        self.path = ""
        self.gamename = ""
        
        self.qid = None
        self.qindex = None
        self.question_detail = {}
        self.prompts = {}
        self.gui_elements = []
        self.quest_elements = []
        
        self.list_category = None
        self.list_category_val = None
        
        self.ui_template = []
        self.ui_tampered = False
        
        self.content_template = {}
        self.question_template = {}
        
        self.question_path = ""
        self.question_file = ""
        
        self.content_field = ""
        
        self.copy_list = []
        
        self.content_file = ""
        
        self.btnLoad = None
        
        ttk.Style().theme_use('clam')
        
        self.root.minsize(width=700, height=400)
        

    def set_path(self, path):
        self.path = path
        
        
    def set_content_template(self, t):
        self.content_template = t
        
    
    def set_question_template(self, t):
        self.question_template = t
        
    
    def set_content_file(self, f):
        self.content_file = f
        
    
    def set_question_path(self, p):
        self.question_path = p
        
        
    def set_question_file(self, f):
        self.question_file = f
        
        
    def set_display_name(self, field, where):
        self.display_name = field
        self.display_name_from = where
        
        
    def set_content_field(self, cf):
        self.content_field = cf
        
    
    def set_game_name(self, name):
        self.gamename = name
        
        
    def add_copy_field(self, from_field, to_field, direction = QUESTION_TO_CONTENT):
        self.copy_list.append({"from": from_field, "to": to_field, "direction": direction})
        

    def main_screen(self):
        frm = ttk.Frame(self.root)
        frm.pack(expand=NO, fill='both')

        self.btnLoad = ttk.Button(frm, text = 'Load')
        self.btnLoad['command'] = self.load_assets
        self.btnLoad.pack(pady=8, padx=8, side=LEFT)
        
        btnApplyPatch = ttk.Button(frm, text = 'Apply patch')
        btnApplyPatch['command'] = self.load_patch
        btnApplyPatch.pack(pady=8, padx=8, side=LEFT)
        
        
        btnPatch = ttk.Button(frm, text = 'Save as patch')
        btnPatch['command'] = self.save_patch
        btnPatch.pack(pady=8, padx=8, side=LEFT)
        
        btnSave = ttk.Button(frm, text = 'Create assets')
        btnSave['command'] = self.save_assets
        btnSave.pack(pady=8, padx=8, side=LEFT)
        
        frmQuestions = ttk.Frame(self.root)
        frmQuestions.pack(expand=True, fill='both')

        
        self.questions = ttk.Treeview(frmQuestions)
        self.questions.pack(expand=YES, fill='both', side = LEFT)
        self.questions.bind('<<TreeviewSelect>>', self.question_clicked)
        ysb = ttk.Scrollbar(frmQuestions, orient='vertical', command=self.questions.yview)
        self.questions.configure(yscroll=ysb.set)
        ysb.pack(side=LEFT, expand=NO, fill='y')
        
        frmQuestDetails = ttk.Frame(frmQuestions)
        frmQuestDetails.pack(expand=YES, fill='both', side=LEFT)
        
                
        for u in self.ui_template:
            if u["type"] == TEXTBOX:
                ttk.Label(frmQuestDetails, text=u["name"]).pack()
                element = ttk.Entry(frmQuestDetails, textvariable=u["variable"])
            elif u["type"] == CHECKBOX:
                element = ttk.Checkbutton(frmQuestDetails, text=u["name"], variable=u["variable"], command=u["variable"].cb)
            element.pack(padx=32, pady=8, expand=NO, fill='x')
            u["handle"] = element
            self.quest_elements.append(element)
            
        
        btnUpdate = ttk.Button(frmQuestDetails, text = 'Save question')
        btnUpdate['command'] = self.update_question
        btnUpdate.pack(pady=8, padx=8, side=BOTTOM)
        
        frmQuestActions = ttk.Frame(self.root)
        frmQuestActions.pack(expand=NO, fill='both')
        
        btnNewQuest = ttk.Button(frmQuestActions, text = 'New question')
        btnNewQuest['command'] = self.add_question
        btnNewQuest.pack(pady=8, padx=8, side=LEFT)
        
        btnDelQuest = ttk.Button(frmQuestActions, text = 'Delete question')
        btnDelQuest['command'] = self.delete_question
        btnDelQuest.pack(pady=8, padx=8, side=LEFT)
        
        self.init_questions()


    def add_ui_field(self, name, typ, field, default="", is_list_text = False, depends = "", on_value = "true", off_value = "false", provider = QUESTION):
        self.ui_template.append({
            "name": name, 
            "type": typ, 
            "variable": tkinter.StringVar() if typ != CHECKBOX else CheckVar(on_val=on_value, off_val=off_value, field=field, ui=self.ui_template), 
            "default": default, 
            "field": field,
            "handle": None,
            "lasttext": default,
            "on_value": on_value,
            "off_value": off_value,
            "depends": depends,
            "provider": provider
        })
        if is_list_text: 
            self.list_category = field
            self.list_category_val = self.ui_template[len(self.ui_template) - 1]["variable"]


    def init_questions(self):
        if os.path.isdir(self.path):
            self.parse_questions()
            for g in self.quest_elements:
                g.configure(state='disabled')
        else:        
            for g in self.gui_elements:
                g.configure(state='disabled')
            self.btnLoad.configure(state='normal')

       
    def load_assets(self):
#        filename = askopenfilename(defaultextension=".bin", filetypes=[("assets.bin", ".bin")], initialfile="assets.bin", parent=self.root, title="Choose Jackbox Party Pack assets.bin")
#        if not filename:
#            return
#        
#        if not os.path.isfile(filename):
#            messagebox.showwarning("Open file", "Could not open file!")
#            return
        game_dir = askdirectory()
        if os.path.isfile(os.path.join(game_dir, "assets.bin")): # non-steam version
            filename = os.path.join(game_dir, "assets.bin")
        else: # steam version
            self.set_path(os.path.join(game_dir, self.path.replace("assets/", "")))
            filename = None
        
        toplevel = Toplevel()
        label1 = Label(toplevel, text="Please wait, parsing assets...")
        label1.pack(padx=16, pady=16)
        self.root.update()
        try:
            if(filename): jbpp.uncompress(filename)
            self.parse_questions()
        except:
            messagebox.showwarning("Parse file", "Could not parse assets file!")
        toplevel.destroy()
        for g in self.gui_elements:
            g.configure(state='normal')
        for g in self.quest_elements:
            g.configure(state='disabled')
    
    
    def save_assets(self):
        filename = asksaveasfilename(defaultextension=".bin", filetypes=[("assets.bin", ".bin")], initialfile="assets.bin", parent=self.root, title="Choose Jackbox Party Pack assets.bin")
        toplevel = Toplevel()
        label1 = Label(toplevel, text="Please wait, saving assets...")
        label1.pack(padx=16, pady=16)
        self.root.update()        

        #print(self.prompts)
        #print(self.question_detail)

        self.save_questions()
        
        if filename: jbpp.compress(filename)
        
        toplevel.destroy()
        
        
    def save_patch(self):
        filename = asksaveasfilename(defaultextension=".jbp", filetypes=[("Jackbox Party Patch", ".jbp")], initialfile="drawful.jbp", parent=self.root, title="Save as patch")
        if not filename: return
    
        pname = simpledialog.askstring("Patch Name", "Name of patch (e.g. 'German translation')", parent=self.root)
    
        toplevel = Toplevel()
        label1 = Label(toplevel, text="Please wait, saving patch...")
        label1.pack(padx=16, pady=16)
        self.root.update()        
        self.save_questions()
        
        jbpp.create_patch(filename, self.path, {"game": self.gamename, "name": pname})
        
        toplevel.destroy()
        
        
    def load_patch(self):
        filename = askopenfilename(defaultextension=".jbp", filetypes=[("Jackbox Party Patch", ".jbp")], parent=self.root, title="Choose Jackbox Party Patch file")
        if not filename:
            return
        
        if not os.path.isfile(filename):
            messagebox.showwarning("Open file", "Could not open file!")
            return
        
        toplevel = Toplevel()
        label1 = Label(toplevel, text="Please wait, parsing assets...")
        label1.pack(padx=16, pady=16)
        self.root.update()
        
        try:
            jbpp.apply_patch(filename)
            self.parse_questions()
        except:
            messagebox.showwarning("Parse file", "Could not parse assets file!")
        toplevel.destroy()
        

    def search_audio(self):
        filename = askopenfilename(defaultextension=".mp3", filetypes=[("MP3", ".mp3")], initialdir=os.path.dirname(self.audioFile.get()), initialfile=os.path.basename(self.audioFile.get()), parent=self.root, title="Choose an audio file")
        if filename:
            return filename
        else:
            return None

    
    def update_question(self):
        #print(self.question_detail[self.qid])
        #self.prompts[self.content_field][self.qindex][self.list_category] = self.list_category_val.get() 
        for c in self.copy_list:
            if c["direction"] == QUESTION_TO_CONTENT:
                val = None
                for u in self.ui_template:
                    if u["field"] == c["from"]:
                        val = u["variable"].get()
                        break
                self.prompts[self.content_field][self.qindex][c["to"]] = val
        
        
        for u in self.ui_template:
            if u["provider"] == QUESTION:
                self.set_field(self.question_detail[self.qid], u["field"], u["variable"].get())
            elif u["provider"] == CONTENT:
                self.prompts[self.content_field][self.qindex][u["field"]] = u["variable"].get()
            
        #if os.path.isfile(self.audioFile.get()):
            #try:
                #copyfile(self.audioFile.get(), os.path.join("assets/games/Fibbage2/content/fibbageshortie/" + str(self.qid), os.path.basename(self.audioFile.get())))
            #except:
                #pass
            #self.set_field(self.question_detail[self.qid], "JokeAudio", os.path.basename(self.audioFile.get()).replace(".mp3", ""))
        
        t = "<new>"
        if self.display_name_from == CONTENT:
            t = self.prompts[self.content_field][self.qindex][self.display_name]
        elif self.display_name_from == QUESTION:
            t = self.question_detail[self.qid][self.display_name]
        self.questions.item(self.questions.get_children()[self.qindex], text=t)
        
        self.ui_mark_saved()
        self.save_questions(self.qid)
    
    
    def ui_has_changed(self):
        if not self.ui_tampered:
            return False
        
        for u in self.ui_template:
            if u["variable"].get() != u["lasttext"]:
                #print("%s != %s" % (u["variable"].get(), u["lasttext"]))
                return True
        return False
    
    
    def ui_mark_saved(self):
        for u in self.ui_template:
            u["lasttext"] = u["variable"].get()
    
    
    def question_clicked(self, qid):
        if self.ui_has_changed() and messagebox.askyesno(0.0, "Question changed! Do you want to save?"):
            self.update_question()
        if not self.ui_tampered:
            self.ui_tampered = True
            
        for g in self.quest_elements:
            g.configure(state='normal')
            
        curItem = self.questions.focus()
        self.qindex = self.questions.index(curItem)
        self.qid = self.questions.item(curItem)["tags"][0]
        
        for u in self.ui_template:
            if u["provider"] == QUESTION:
                u["variable"].set(self.get_field(self.question_detail[self.qid], u["field"]))
            elif u["provider"] == CONTENT:
                u["variable"].set(self.prompts[self.content_field][self.qindex][u["field"]])

            u["lasttext"] = u["variable"].get()
        
        self.ui_template[0]["handle"].focus_set()
        
        
    def delete_question(self):
        if self.questions.selection():
            items = self.questions.selection()
        else:
            items = [ self.questions.focus() ]
            
        for curItem in items:
            self.qindex = self.questions.index(curItem)
            self.qid = self.questions.item(curItem)["tags"][0]
            
            self.questions.delete(curItem)
            
            del self.prompts[self.content_field][self.qindex]
            del self.question_detail[self.qid]
            
        self.save_questions(-1)
            
            
    
    
    def add_question(self):
        self.max_id += 1
        qid = self.max_id
        
        tc = copy.deepcopy(self.content_template)
        tc["id"] = qid
        self.prompts[self.content_field].append(tc)
        
        
        self.question_detail[qid] = copy.deepcopy(self.question_template) 
        
        it = self.questions.insert("", "end", tags=(qid), text="<new>")
        self.questions.focus(it)
        self.root.update()
        self.questions.selection_set(it)
        self.save_questions(qid)
    
    
    def get_field(self, val, name):
        for f in val["fields"]:
            if f["n"] == name:
                if "v" not in f:
                    return ""
                return f["v"]
        return None
    
    
    def set_field(self, val, name, new_val):
        for f in val["fields"]:
            if f["n"] == name:
                f["v"] = new_val
                return
        return None
    
    
    def parse_questions(self):
        self.max_id = 0
        with open(os.path.join(self.path, self.content_file), "r") as f:
            self.prompts = json.load(f)
            self.questions.delete(*self.questions.get_children())
            for q in self.prompts[self.content_field]:
                if int(q["id"]) > self.max_id: self.max_id = int(q["id"])
                # get details
                with open(os.path.join(os.path.join(self.path, self.question_path), self.question_file) % str(q["id"])) as det:
                    self.question_detail[q["id"]] = json.load(det)

                t = "<new>"
                if self.display_name_from == CONTENT:
                    t = q[self.display_name]
                elif self.display_name_from == QUESTION:
                    t = self.question_detail[q[id]][self.display_name]
                    
                self.questions.insert("", "end", tags=(q["id"]), text=t)

    
    
    def save_questions(self, qid=None):
        with open(os.path.join(self.path, self.content_file), "w") as f:
            json.dump(self.prompts, f)
        
        #print("---------------------------")
        #print(self.prompts)
        #print("---------------------------")
        
        
        for q in self.prompts[self.content_field]:
            #if not qid and q["id"] != qid: continue
            path = os.path.join(self.path, self.question_path) % str(q["id"])
            if not os.path.isdir(path):
                os.mkdir(path)
            with open(os.path.join(path, self.question_file), "w") as det:
                json.dump(self.question_detail[q["id"]], det)
            
            #print(q["id"])
            #print("---------------------------")
            #print(self.question_detail[q["id"]])
            #print("---------------------------")
            #print("---------------------------")

            

