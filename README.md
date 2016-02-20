Jackbox Party Box - Drawful Question Editor
=========

Drawful Question Editor is a question editor for the Drawful game in Jackbox Party Box (Vol. 1). It allows to edit, add and delete questions. 

# Requirements

The program needs python3, python3-tk and Jackbox Party Box installed. 

# Usage

Start with 
`python3 drawful.py`

A default usage example would be the following
+ **Step 1**: Click `Load` and navigate to the Jackbox Party Box folder, select the file *assets.bin*. The file is loaded which can take up to one minute. If the file was loaded the last time you opened the program, you can continue working without loading the file again.
+ **Step 2**: The questions can be seen on the left side. Click on any question to edit it. 
  * *Term*: this is the term that is shown to the user and has to be drawn
  * *Alternate spellings*: Alternate spellings of the term that should be accepted. If you want to enter more than one alternate spelling, separate it with `|`, e.g. "color|colour".
  * *Joke Audio File*: You can add a short audio file for jokes. Check the checkbox and enter the path to the audio file to do so.
  * *Save question*: Save the question. It is not yet written back to the game, this is done using `Create assets`.
+ **Step 3 (optional)**: Add new questions using `New Question` or delete one or multiple questions by selecting them and clicking `Delete question`.
+ **Step 4**: If you are done editing questions, either click `Create assets` to create a new *assets.bin*. Replace the original *assets.bin* with the newly generated to use your new questions (it is suggested to do a backup first). Or create a patch to distribute it to your friends using `Save as patch`. You can then load the original *assets.bin*, and apply the patch using `Apply patch`. This has the advantage that you do not need to share the 350MB *assets.bin* file. 