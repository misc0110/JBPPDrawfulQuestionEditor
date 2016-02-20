import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import simpledialog
from tkinter import messagebox
from shutil import copyfile
import json
import os
import io
import zipfile

import jbpb

class App(object):
    def __init__(self):
        """ init application """
        self.root = tkinter.Tk()
        self.question = None
        # self.root.iconbitmap("time.ico")
        self.root.title("JBPB Drawful Question Editor")
        
        self.termVal = tkinter.StringVar()
        self.alternateSpellingsVal = tkinter.StringVar()
        self.jokeAudio = tkinter.IntVar()
        self.audioFile = tkinter.StringVar()
        self.termValBefore = None
        self.alternateSpellingsValBefore = None
        self.jokeAudioBefore = None
        self.audioFileBefore = None
        
        self.qid = None
        self.qindex = None
        self.question_detail = {}
        self.prompts = {}
        self.gui_elements = []
        self.quest_elements = []
        
        ttk.Style().theme_use('clam')
        
        self.root.minsize(width=700, height=400)
        
        self.main_screen()


    def main_screen(self):
        self.usrVal = tkinter.StringVar()
        self.pwdVal = tkinter.StringVar()
        
        frm = ttk.Frame(self.root)
        frm.pack(expand=NO, fill='both')

        btnLoad = ttk.Button(frm, text = 'Load')
        btnLoad['command'] = self.load_assets
        btnLoad.pack(pady=8, padx=8, side=LEFT)
        
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
        
        ttk.Label(frmQuestDetails, text='Term').pack()
        self.entryTerm = ttk.Entry(frmQuestDetails, textvariable=self.termVal)
        self.entryTerm.pack(padx=32, pady=8, expand=NO, fill='x')

        ttk.Label(frmQuestDetails, text='Alternate spellings').pack()
        self.entrySpell = ttk.Entry(frmQuestDetails, textvariable=self.alternateSpellingsVal)
        self.entrySpell.pack(padx=32, pady=8, expand=NO, fill='x')
        
        frmAudio = ttk.Frame(frmQuestDetails)
        frmAudio.pack(expand=NO, fill='both')
        
        ttk.Label(frmAudio, text='Joke Audio File').pack()
        self.checkAudio = ttk.Checkbutton(frmAudio, text='Has Joke Audio', variable=self.jokeAudio)
        self.checkAudio.pack(padx=32, pady=8, expand=NO, fill='x')
        
        #ttk.Label(frmAudio, text='Joke Audio File').pack()
        self.entryAudio = ttk.Entry(frmAudio, textvariable=self.audioFile)
        self.entryAudio.pack(padx=32, pady=8, expand=YES, fill='x', side=LEFT)
        
        btnSearchAudio = ttk.Button(frmAudio, text='...')
        btnSearchAudio['command'] = self.search_audio
        btnSearchAudio.pack(side=LEFT, padx=32, pady=8, expand=NO, fill='none')
        
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
        
        self.gui_elements = [btnPatch, btnApplyPatch, btnSave, btnDelQuest, btnNewQuest, btnSearchAudio, btnUpdate, self.entryTerm, self.entrySpell, self.entryAudio, self.checkAudio]
        self.quest_elements = [btnUpdate, btnSearchAudio, self.entryTerm, self.entrySpell, self.checkAudio, self.entryAudio]
        
        if os.path.isdir("assets"):
            self.parse_questions()
            for g in self.quest_elements:
                g.configure(state='disabled')
        else:        
            for g in self.gui_elements:
                g.configure(state='disabled')
            btnLoad.configure(state='normal')

        self.entryTerm.bind("<Return>", lambda qid: [self.update_question(), self.entrySpell.focus_set()])
        self.entrySpell.bind("<Return>", lambda qid: self.update_question())
        self.entryAudio.bind("<Return>", lambda qid: self.update_question())
        
        
    def load_assets(self):
        filename = askopenfilename(defaultextension=".bin", filetypes=[("assets.bin", ".bin")], initialfile="assets.bin", parent=self.root, title="Choose Jackbox Party Box assets.bin")
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
            if(filename): jbpb.uncompress(filename)
            self.parse_questions()
        except:
            messagebox.showwarning("Parse file", "Could not parse assets file!")
        toplevel.destroy()
        for g in self.gui_elements:
            g.configure(state='normal')
        for g in self.quest_elements:
            g.configure(state='disabled')
    
    
    def save_assets(self):
        filename = asksaveasfilename(defaultextension=".bin", filetypes=[("assets.bin", ".bin")], initialfile="assets.bin", parent=self.root, title="Choose Jackbox Party Box assets.bin")
        toplevel = Toplevel()
        label1 = Label(toplevel, text="Please wait, saving assets...")
        label1.pack(padx=16, pady=16)
        self.root.update()        

        print(self.prompts)
        print(self.question_detail)

        self.save_questions()
        
        if filename: jbpb.compress(filename)
        
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
        
        jbpb.create_patch(filename, "assets/games/Drawful/content", {"game": "Drawful", "name": pname})
        
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
            jbpb.apply_patch(filename)
            self.parse_questions()
        except:
            messagebox.showwarning("Parse file", "Could not parse assets file!")
        toplevel.destroy()
        

    def search_audio(self):
        filename = askopenfilename(defaultextension=".mp3", filetypes=[("MP3", ".mp3")], initialdir=os.path.dirname(self.audioFile.get()), initialfile=os.path.basename(self.audioFile.get()), parent=self.root, title="Choose an audio file")
        if filename:
            self.audioFile.set(filename)

    
    def update_question(self):
        print(self.question_detail[self.qid])
        self.prompts["items"][self.qindex]["text"] = self.termVal.get()
        self.set_field(self.question_detail[self.qid], "QuestionText", self.termVal.get())
        self.set_field(self.question_detail[self.qid], "AlternateSpellings", self.alternateSpellingsVal.get())
        self.set_field(self.question_detail[self.qid], "HasJokeAudio", "true" if self.jokeAudio.get() != 0 else "false")
        
        if os.path.isfile(self.audioFile.get()):
            try:
                copyfile(self.audioFile.get(), os.path.join("assets/games/Drawful/content/prompts/" + str(self.qid), os.path.basename(self.audioFile.get())))
            except:
                pass
            self.set_field(self.question_detail[self.qid], "JokeAudio", os.path.basename(self.audioFile.get()).replace(".mp3", ""))
        
        self.questions.item(self.questions.get_children()[self.qindex], text=self.termVal.get())
        
        self.termValBefore = self.termVal.get()
        self.alternateSpellingsValBefore = self.alternateSpellingsVal.get()
        self.jokeAudioBefore = self.jokeAudio.get()
        self.audioFileBefore = self.audioFile.get()
        self.save_questions(self.qid)
    
    
    def question_clicked(self, qid):
        if self.termValBefore:
            if (self.termValBefore != self.termVal.get() or 
                self.alternateSpellingsValBefore != self.alternateSpellingsVal.get() or 
                self.jokeAudioBefore != self.jokeAudio.get() or 
                self.audioFileBefore != self.audioFile.get()):
                if messagebox.askyesno(0.0, "Question changed! Do you want to save?"):
                    self.update_question()
            
        for g in self.quest_elements:
            g.configure(state='normal')
            
        curItem = self.questions.focus()
        self.qindex = self.questions.index(curItem)
        self.qid = self.questions.item(curItem)["tags"][0]
        self.termVal.set(self.get_field(self.question_detail[self.qid], "QuestionText"))
        self.alternateSpellingsVal.set(self.get_field(self.question_detail[self.qid], "AlternateSpellings"))
        self.jokeAudio.set(self.get_field(self.question_detail[self.qid], "HasJokeAudio") == "true")
        if self.jokeAudio.get() != 0: self.audioFile.set(os.path.join("assets/games/Drawful/content/prompts/" + str(self.qid), self.get_field(self.question_detail[self.qid], "JokeAudio") + ".mp3"))
        else: self.audioFile.set("")
        self.termValBefore = self.termVal.get()
        self.alternateSpellingsValBefore = self.alternateSpellingsVal.get()
        self.jokeAudioBefore = self.jokeAudio.get()
        self.audioFileBefore = self.audioFile.get()
        self.entryTerm.focus_set()
        
        
    def delete_question(self):
        if self.questions.selection():
            items = self.questions.selection()
        else:
            items = [ self.questions.focus() ]
            
        for curItem in items:
            self.qindex = self.questions.index(curItem)
            self.qid = self.questions.item(curItem)["tags"][0]
            
            self.questions.delete(curItem)
            
            del self.prompts["items"][self.qindex]
            del self.question_detail[self.qid]
            
        self.save_questions(-1)
            
    
    def add_question(self):
        self.max_id += 1
        qid = self.max_id
        
        self.prompts["items"].append({"id": qid, "text": "<new>"})
        self.question_detail[qid] = {
          "length": 4,
          "fields": [
            {
                "n": "QuestionText",
                "t": "S",
                "v": "<new>"
            },
            {
                "n": "AlternateSpellings",
                "t": "S",
                "v": ""
            },
            {
                "n": "HasJokeAudio",
                "t": "B",
                "v": "false"
            },
            {
                "n": "JokeAudio",
                "t": "A",
                "v": ""
            }
          ]    
        }
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
        with open("assets/games/Drawful/content/prompts.jet", "r") as f:
            self.prompts = json.load(f)
            self.questions.delete(*self.questions.get_children())
            for q in self.prompts["items"]:
                self.questions.insert("", "end", tags=(q["id"]), text=q["text"])
                if int(q["id"]) > self.max_id: self.max_id = int(q["id"])
                # get details
                with open("assets/games/Drawful/content/prompts/" + str(q["id"]) + "/data.jet") as det:
                    self.question_detail[q["id"]] = json.load(det)
    
    
    def save_questions(self, qid=None):
        with open("assets/games/Drawful/content/prompts.jet", "w") as f:
            json.dump(self.prompts, f)
            
        for q in self.prompts["items"]:
            if not qid and q["id"] != qid: continue
            path = "assets/games/Drawful/content/prompts/" + str(q["id"])
            if not os.path.isdir(path):
                os.mkdir(path)
            with open(path + "/data.jet", "w") as det:
                json.dump(self.question_detail[q["id"]], det)
            
            
app = App()
app.root.mainloop()  
