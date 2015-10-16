#Discipline

Using the dark powers of `launchd`, Applescript and SelfControl, I will summon daemons (more precisely, agents) to force me to keep a productive schedule.

The example templates are as such:
1. Block sites from 1.00 to 7.00 (go to sleep)
2. Block sites from 9.00 to 13.00 (morning work)
3. Block sites from 14.00 to 19.00 (afternoon work)
4. Block sites from 21:00 to 24:00 (evening work)
5. Block sites all day long except Sunday (always block)

Also:
* a notification is sent 60 seconds before starting
* if the computer wakes up from sleep during disciplined hours, `launchd` will still give a grace time and then start the block for the remaining time

## Requirements
* the [SelfControl](selfcontrolapp.com) application;
* OSX 10.9 or higher;
* administrator rights.
The last two requirements are there because I use a script library; some modifications to the `Discipline.scpt` file could make it an executable and extend support to older versions of Applescript.

### Optional requirements
* the [LaunchControl](www.soma-zone.com/LaunchControl/) application.
This is used to easily view and edit the agents. It’s fun!

## TODO
* Fix the midnight bug (not sure if it still exists, see known issues)
* As soon as I find an Applescript-compatible Pomodoro application, it could be integrated with the morning and afternoon work periods.

## Installation notes:
Everything is pretty much self-explanatory, you have to remember that both the Script Libraries folder and the LaunchAgents folder can be either in the shared `/Library/` which is common to all accounts, or in your user-specific `~/Library/` folder. It’s up to you to decide where to install the contents.

#### (optional) Alias the library
If you need to modify the script library or its location in the directory tree, it might be convenient to create an alias to it. I couldn’t find a bash-only way to do it, so I had to call Applescript. First, you should `cd` to the folder containing `Discipline.scpt`, and then you should run:
``` bash
mkdir -p ~/Library/Script\ Libraries
osascript -e 'set this_dir to do shell script "pwd"
set to_alias to this_dir & "/Discipline.scpt"
set that_dir to POSIX path of (path to library folder from user domain) & “Script Libraries”
tell application "Finder" to make alias file to POSIX file to_alias at POSIX file that_dir'
```

### Load the .plist files without LaunchControl
You could just reboot (or logout and login), and the agents should be loaded automatically. Or, you could use `launchctl` to load them manually:
``` bash
launchctl load ~/Library/LaunchAgents/local.gotosleep.plist
```

## Customization
The general template for calling a block is:
``` bash
osascript -e “tell script \”Discipline\” to block_me(\”06:00\”, \”14:00\”, 60)
```
where the first two arguments are the start and end time of the block, and the third is the grace period (in seconds) between the warning notification and the block’s actual start.
These parameters are parsed by Applescript, so it’s entirely possible that other variable types are allowed (i.e. integers instead of strings).

## Known Issues
I think (but I didn't test) that the program won't work if a block is set across midnight: for example, from 23:00 to 7:00 of the next day.

A hacky solution is to create two agents, one that ends at 23:59 and the other that starts at 00:00.