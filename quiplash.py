#!/usr/bin/python3

import jbpp
import jbppui

class Quiplash(jbppui.JBPPUI):
    def __init__(self):
        super().__init__()
        
        super().set_path("assets/games/Quiplash")
        super().set_content_file("content/QuiplashQuestion.jet")
        super().set_question_path("content/QuiplashQuestion/%s")
        super().set_question_file("data.jet")
        super().set_content_field("content")
        
        super().set_content_template({"x":"false","id":0,"prompt":"<new>"}) 
        super().set_question_template({
                    "fields":[  
                {  
                    "t":"B",
                    "v":"false",
                    "n":"HasJokeAudio"
                },
                {  
                    "t":"S",
                    "v":"",
                    "n":"Keywords"
                },
                {  
                    "t":"S",
                    "v":"",
                    "n":"Author"
                },
                {  
                    "t":"S",
                    "v":"",
                    "n":"KeywordResponseText"
                },
                {  
                    "t":"S",
                    "v":"prompt",
                    "n":"PromptText"
                },
                {  
                    "t":"S",
                    "v":"",
                    "n":"Location"
                },
                {  
                    "t":"A",
                    "v":"374019_0",
                    "n":"KeywordResponseAudio"
                },
                {  
                    "t":"A",
                    "v":"374017_0",
                    "n":"PromptAudio"
                }
            ]
        })
        
        super().add_ui_field("Prompt", jbppui.TEXTBOX, "PromptText", "prompt")
        super().add_ui_field("Response", jbppui.TEXTBOX, "KeywordResponseText", "")
        super().add_ui_field("Keywords", jbppui.TEXTBOX, "Keywords", "")
        
        super().set_display_name("prompt", jbppui.CONTENT)
        super().add_copy_field("PromptText", "prompt")
        
        super().main_screen()

            
            
app = Quiplash()
app.root.mainloop()  
