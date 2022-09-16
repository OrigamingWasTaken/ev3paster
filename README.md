# ev3paster
A python script made to combine 2 .lmsp files (ev3 projects) together

Run the script like this:
    `$ python3 paster.py <path to project 1> <path to project 2>`

Exemple:
    `$ python3 paster.py ~/Documents/LEGO Education EV3/FollowLine.lmsp ~/Documents/LEGO Education EV3/TurnGyro.lmsp`

All the blocks from both programms will be merged (+ variables, lists, broadcasts, comments, etc...)

**By doing this, you will loose the 2nd programm informations, by that i mean: User Agent, VM, and some other things. (it shouldn't be harmuflul) + the first file will be overwritten by the combined file (i didn't find a way to prevent this so yeah, just make a backup)**
