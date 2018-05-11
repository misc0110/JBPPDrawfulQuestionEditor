#!/usr/bin/python3

import jbpp
import jbppui

class Fibbage2(jbppui.JBPPUI):
    def __init__(self):
        super().__init__()
        
        super().set_path("assets/games/Fibbage")
        super().set_content_file("content/shortie.jet")
        super().set_question_path("content/questions/%s")
        super().set_question_file("data.jet")
        super().set_content_field("questions")
        
        super().set_content_template({"id": 0, "category": "<new>", "x": True, "bumper": ""})
        super().set_question_template({
          "fields":[  
            {  
                "t":"B",
                "v":"false",
                "n":"HasBumperAudio"
            },
            {  
                "t":"B",
                "v":"false",
                "n":"HasBumperType"
            },
            {  
                "t":"B",
                "v":"false",
                "n":"HasCorrectAudio"
            },
            {  
                "t":"B",
                "v":"false",
                "n":"HasQuestionAudio"
            },
            {  
                "t":"S",
                "v":"Suggestions (comma separated)",
                "n":"Suggestions"
            },
            {  
                "t":"S",
                "v":"Category",
                "n":"Category"
            },
            {  
                "t":"S",
                "v":"Correct answer",
                "n":"CorrectText"
            },
            {  
                "t":"S",
                "v":"None",
                "n":"BumperType"
            },
            {  
                "t":"S",
                "v":"Question <BLANK>",
                "n":"QuestionText"
            },
            {  
                "t":"S",
                "v":"Alternative spellings (comma separated)",
                "n":"AlternateSpellings"
            },
            {  
                "t":"A",
                "n":"BumperAudio"
            },
            {  
                "t":"A",
                "v":"372356_0f",
                "n":"CorrectAudio"
            },
            {  
                "t":"A",
                "v":"372353_1",
                "n":"QuestionAudio"
            }
          ]
        })
        
        super().add_ui_field("Category", jbppui.TEXTBOX, "Category", "category")
        super().add_ui_field("Question", jbppui.TEXTBOX, "QuestionText", "What is <BLANK>?")
        super().add_ui_field("Answer", jbppui.TEXTBOX, "CorrectText", "")
        super().add_ui_field("Alternate spellings", jbppui.TEXTBOX, "AlternateSpellings", "spelling1,spelling2,...")
        super().add_ui_field("Suggestions", jbppui.TEXTBOX, "Suggestions", "suggestion1,suggestion2,...")
        
        super().set_display_name("category", jbppui.CONTENT)
        super().add_copy_field("Category", "category")
        
        super().main_screen()

            
            
app = Fibbage2()
app.root.mainloop()  
