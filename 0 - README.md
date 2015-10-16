#Discipline

Using `launchd`, Applescript and SelfControl, three agents will force me to keep a productive schedule.

1. Block sites from 1.00 to 7.00 (go to sleep)
2. Block sites from 9.00 to 13.00 (morning work)
3. Block sites from 14.00 to 18.00 (afternoon work)

Also:
* a notification is sent 5 minutes before starting
* if the computer wakes up from sleep during disciplined hours, `launchd` will still give a grace time of 5 minutes and then start the block for the remaining time

## Requirements
* the [SelfControl](selfcontrolapp.com) application;
* OSX 10.9 or higher;
* administrator rights.
The last two requirements are there because I use a script library; some modifications to the `Discipline.scpt` file could make it an executable and extend support to older versions of Applescript.

## TODO
* Fix the midnight bug (see known issues)
* As soon as I find an Applescript-compatible Pomodoro application, it should be integrated with the morning and afternoon work periods.
* I probably should create an installing script: but it’s just a matter of copying files (and loading them with `launchctl`).

## Installation notes:
There are two steps, installing the script library and installing the agents.

### Installing the library
#### (optional) Alias the library
If you need to modify the script library or its location in the directory tree, it might be convenient to create an alias to it. I couldn’t find a bash-only way to do it, so I had to call Applescript (keep in mind that first you should `cd` to the `discipline` main folder):
```
osascript -e 'set this_dir to do shell script "pwd"
set fromfile to this_dir & "/Script Libraries/Discipline.scpt"
tell application "Finder" to make alias file to POSIX file fromfile at POSIX file this_dir'
```

#### Move .scpt file to the Script Libraries folder
The `Discipline.scpt` library should go in the /Library/Script Libraries folder. I didn’t have it on my machine, so before moving the file I created the destination folder:
```
sudo mkdir “/Library/Script Libraries”
sudo mv Discipline.scpt “/Library/Script Libraries/Discipline.scpt”
```

### Installing the agents
The agents’ job consist of a single `osascript` call to the main script library; therefore there should be no need to create an alias. Of course, the simple and recommended way to install, view and modify the agents is to use [LaunchControl](http://www.soma-zone.com/LaunchControl/). 

#### Move the .plist files to the ~/Library/LaunchAgents folder
```
mv LaunchAgents/local.gotosleep.plist ~/Library/local.gotosleep.plist
mv LaunchAgents/local.morningwork.plist ~/Library/local.morningwork.plist
mv LaunchAgents/local.afternoonwork.plist ~/Library/local.afternoonwork.plist
```

#### Load the .plist files
You could just reboot (or logout and login), and the agents should be loaded automatically. Or, you could use `launchctl` to load them manually:
```
launchctl load ~/Library/LaunchAgents/local.gotosleep.plist
launchctl load ~/Library/LaunchAgents/local.morningwork.plist
launchctl load ~/Library/LaunchAgents/local.afternoonwork.plist
```

## Customization
The general template for calling a block is:
```
osascript -e “tell script \”Discipline\” to block_me(\”06:00\”, \”14:00\”, 60)
```
where the first two arguments are the start and end time of the block, and the third is the grace period (in seconds) between the warning notification and the block’s actual start.
These parameters are parsed by Applescript, so it’s entirely possible that other variable types are allowed (i.e. integers instead of strings).

## Known Issues
I think (but I didn't test) that the program won't work if a block is set across midnight: for example, from 23:00 to 7:00 of the next day.

A hacky solution is to create two agents, one that ends at 23:59 and the other that starts at 00:00.