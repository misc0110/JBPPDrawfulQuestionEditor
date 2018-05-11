#!/usr/bin/python3

import jbpp
import jbppui

class Drawful(jbppui.JBPPUI):
    def __init__(self):
        super().__init__()
        
        super().set_path("assets/games/Drawful")
        super().set_content_file("content/prompts.jet")
        super().set_question_path("content/prompts/%s")
        super().set_question_file("data.jet")
        super().set_content_field("items")
        
        super().set_content_template({"id": 0, "text": "<new>"})
        super().set_question_template({
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
        })
        
        super().add_ui_field("Term", jbppui.TEXTBOX, "QuestionText", "<new>")
        super().add_ui_field("Alternate spellings", jbppui.TEXTBOX, "AlternateSpellings", "spelling1|spelling2|...")
        
        super().set_display_name("text", jbppui.CONTENT)
        super().add_copy_field("QuestionText", "text")
        
        super().main_screen()

            
            
app = Drawful()
app.root.mainloop()  
