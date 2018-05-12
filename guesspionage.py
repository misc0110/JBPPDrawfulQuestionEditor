#!/usr/bin/python3

import jbpp
import jbppui

class Guesspionage(jbppui.JBPPUI):
    def __init__(self):
        super().__init__()
        
        super().set_game_name("Guesspionage")
        
        super().set_path("assets/games/PollPosition")
        super().set_content_file("content/PollPositionQuestions.jet")
        super().set_question_path("content/PollPositionQuestions/%s")
        super().set_question_file("data.jet")
        super().set_content_field("content")
        
        super().set_content_template({"x":"false","id":0,"category":"<new>","type":"yn"}) 
        super().set_question_template({  
            "fields":[  
                {  
                    "t":"B",
                    "v":"false",
                    "n":"HasIntro"
                },
                {  
                    "t":"B",
                    "v":"false",
                    "n":"HasResponse"
                },
                {  
                    "t":"N",
                    "v":"23",
                    "n":"A"
                },
                {  
                    "t":"N",
                    "v":"0",
                    "n":"PollAns"
                },
                {  
                    "t":"S",
                    "v":"",
                    "n":"Target"
                },
                {  
                    "t":"S",
                    "v":"mc",
                    "n":"Type"
                },
                {  
                    "t":"S",
                    "v":"What percentage of people wipe their butts while standing up?",
                    "n":"QText"
                },
                {  
                    "t":"S",
                    "v":"Sitting down",
                    "n":"Choice1"
                },
                {  
                    "t":"S",
                    "v":"Toilet Cam",
                    "n":"DataMode"
                },
                {  
                    "t":"S",
                    "v":"A little of both",
                    "n":"Choice2"
                },
                {  
                    "t":"S",
                    "v":"After you poop, do you wipe your butt standing up or sitting down?",
                    "n":"PollQ"
                },
                {  
                    "t":"S",
                    "v":"Standing up",
                    "n":"Choice0"
                },
                {  
                    "t":"S",
                    "v":"Post-defecation procedures. Standing vs. sitting.",
                    "n":"ExpResults"
                },
                {  
                    "t":"A",
                    "n":"Response"
                },
                {  
                    "t":"A",
                    "v":"480122_4",
                    "n":"Q"
                },
                {  
                    "t":"A",
                    "v":"480125_2",
                    "n":"Intro"
                }
            ]
            })
        
        super().add_ui_field("Name", jbppui.TEXTBOX, "category", "", provider=jbppui.CONTENT)
        super().add_ui_field("Category", jbppui.TEXTBOX, "ExpResults", "")
        super().add_ui_field("Question", jbppui.TEXTBOX, "QText", "?")
        super().add_ui_field("Answer", jbppui.TEXTBOX, "A", "")
        super().add_ui_field("Data mode", jbppui.TEXTBOX, "DataMode", "")
        
        super().add_ui_field("Poll", jbppui.TEXTBOX, "PollQ", "")
        super().add_ui_field("Multiple Choice", jbppui.CHECKBOX, "type", False, provider=jbppui.CONTENT, on_value = "mc", off_value = "yn")
        super().add_ui_field("Choice 1", jbppui.TEXTBOX, "Choice0", "", depends="type")
        super().add_ui_field("Choice 2", jbppui.TEXTBOX, "Choice1", "", depends="type")
        super().add_ui_field("Choice 3", jbppui.TEXTBOX, "Choice2", "", depends="type")
        
        
        super().set_display_name("category", jbppui.CONTENT)
        
        super().main_screen()

            
            
app = Guesspionage()
app.root.mainloop()  
