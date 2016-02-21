Jackbox Party Pack - Drawful Question Editor
=========

Drawful Question Editor is a question editor for the Drawful game in Jackbox Party Pack (Vol. 1). It allows to edit, add and delete questions. 

# Requirements

The program needs python3, python3-tk and Jackbox Party Pack installed. 

# Usage

Start with 
`python3 drawful.py`

A default usage example would be the following
+ **Step 1**: Click `Load` and navigate to the Jackbox Party Pack folder, select the file *assets.bin*. The file is loaded which can take up to one minute. If the file was loaded the last time you opened the program, you can continue working without loading the file again.
+ **Step 2**: The questions can be seen on the left side. Click on any question to edit it. 
  * *Term*: this is the term that is shown to the user and has to be drawn
  * *Alternate spellings*: Alternate spellings of the term that should be accepted. If you want to enter more than one alternate spelling, separate it with `|`, e.g. "color|colour".
  * *Joke Audio File*: You can add a short audio file for jokes. Check the checkbox and enter the path to the audio file to do so.
  * *Save question*: Save the question. It is not yet written back to the game, this is done using `Create assets`.
+ **Step 3 (optional)**: Add new questions using `New Question` or delete one or multiple questions by selecting them and clicking `Delete question`.
+ **Step 4 (without Loader)**: If you are done editing questions, click `Create assets` to create a new *assets.bin*. Replace the original *assets.bin* with the newly generated to use your new questions (it is suggested to do a backup first). 
+ **Step 4 (with Loader)**: Create a patch for the mod loader (and to distribute it to your friends) using `Save as patch`. 
+ Copy the patch and the files `loader.py` and `jbpp.py` to the game directory. If you start the loader (`python3 loader.py`), you can select the patches to apply to the game. If you want to edit a patch, first load the original *assets.bin*, and apply the patch using `Apply patch`.  