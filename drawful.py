import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import json
import os

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
        
        self.question_detail = {}
        self.prompts = {}
        
        ttk.Style().theme_use('clam')
        
        self.main_screen()

    def main_screen(self):
        self.usrVal = tkinter.StringVar()
        self.pwdVal = tkinter.StringVar()
        
        frm = ttk.Frame(self.root)
        frm.pack(expand=NO, fill='both')

        btnLoad = ttk.Button(frm, text = 'Load')
        btnLoad['command'] = self.load_assets
        btnLoad.pack(pady=8, padx=8, side=LEFT)
        
        btnSave = ttk.Button(frm, text = 'Save')
        btnSave['command'] = self.save_assets
        btnSave.pack(pady=8, padx=8, side=LEFT)
        
        frmQuestions = ttk.Frame(self.root)
        frmQuestions.pack(expand=True, fill='both')
        
        self.questions = ttk.Treeview(frmQuestions)
        self.questions.pack(expand=YES, fill='both', side = LEFT)
        self.questions.bind('<ButtonRelease-1>', self.question_clicked)
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
        
        btnUpdate = ttk.Button(frmQuestDetails, text = 'Update')
        btnUpdate['command'] = self.update_question
        btnUpdate.pack(pady=8, padx=8, side=BOTTOM)
        
        frmQuestActions = ttk.Frame(self.root)
        frmQuestActions.pack(expand=NO, fill='both')
        
        btnNewQuest = ttk.Button(frmQuestActions, text = 'New question')
        btnNewQuest.pack(pady=8, padx=8, side=LEFT)
        
        btnDelQuest = ttk.Button(frmQuestActions, text = 'Delete question')
        btnDelQuest['command'] = self.delete_question
        btnDelQuest.pack(pady=8, padx=8, side=LEFT)
        
        
    def load_assets(self):
        filename = askopenfilename(defaultextension=".bin", filetypes=[("assets.bin", ".bin")], initialfile="assets.bin", parent=self.root, title="Choose Jackbox Party Box assets.bin")
        print(filename)
        toplevel = Toplevel()
        label1 = Label(toplevel, text="Please wait, parsing assets...")
        label1.pack()
        self.root.update()        
        if(filename): jbpb.uncompress(filename)
        self.parse_questions()
        toplevel.destroy()
    
    def save_assets(self):
        filename = asksaveasfilename(defaultextension=".bin", filetypes=[("assets.bin", ".bin")], initialfile="assets.bin", parent=self.root, title="Choose Jackbox Party Box assets.bin")
        toplevel = Toplevel()
        label1 = Label(toplevel, text="Please wait, saving assets...")
        label1.pack()
        self.root.update()        

        print(self.prompts)
        print(self.question_detail)

        self.save_questions()
        jbpb.compress(filename)
        
        toplevel.destroy()

    
    def update_question(self):
        self.prompts["items"][self.qindex]["text"] = self.termVal.get()
        self.set_field(self.question_detail[self.qid], "QuestionText", self.termVal.get())
        self.set_field(self.question_detail[self.qid], "AlternateSpellings", self.alternateSpellingsVal.get())
        
        self.questions.item(self.questions.get_children()[self.qindex], text=self.termVal.get())
    
    def question_clicked(self, qid):
        curItem = self.questions.focus()
        self.qindex = self.questions.index(curItem)
        self.qid = self.questions.item(curItem)["tags"][0]
        self.termVal.set(self.get_field(self.question_detail[self.qid], "QuestionText"))
        self.alternateSpellingsVal.set(self.get_field(self.question_detail[self.qid], "AlternateSpellings"))
        
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
    
    
    def get_field(self, val, name):
        for f in val["fields"]:
            if f["n"] == name:
                return f["v"]
        return None
    
    def set_field(self, val, name, new_val):
        for f in val["fields"]:
            if f["n"] == name:
                f["v"] = new_val
                return
        return None
    
    def parse_questions(self):
        with open("assets/games/Drawful/content/prompts.jet", "r") as f:
            self.prompts = json.load(f)
            self.questions.delete(*self.questions.get_children())
            for q in self.prompts["items"]:
                self.questions.insert("", "end", tags=(q["id"]), text=q["text"])
                # get details
                with open("assets/games/Drawful/content/prompts/" + str(q["id"]) + "/data.jet") as det:
                    self.question_detail[q["id"]] = json.load(det)
                    
    def save_questions(self):
        with open("assets/games/Drawful/content/prompts.jet", "w") as f:
            json.dump(self.prompts, f)
        for q in self.prompts["items"]:
            path = "assets/games/Drawful/content/prompts/" + str(q["id"])
            if not os.path.isdir(path):
                os.mkdir(path)
            with open(path + "/data.jet", "w") as det:
                json.dump(self.question_detail[q["id"]], det)
                # TODO: joke audio
            
            
app = App()
app.root.mainloop()  
