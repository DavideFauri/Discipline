## Discipline

I created this small program to block my own procrastination attempts. It uses a combination of [`launchd`](http://www.launchd.info/) and Applescripts to automatically launch SelfControl at predetermined times, blocking distracting websites.

## Features

SelfControl cannot be launched automatically on its own, and you have to set manually the length of time during which the block is active. This is fine when you only want to focus for 30 minutes, less so when you need to block distractions every day until 17:00, regardless of the time when you turn on your computer.

Discipline takes care of that, by letting the user select multiple time periods during which to run SelfControl, in a "start time : end time" format.

It also gives a reminder warning and an amount of grace time before letting the block start. The default is 60 seconds, but it can be configured.

Some default templates are included in the `examples` folder:
1. Block websites from 1.00 to 7.00 (go to sleep)
2. Block websites from 9.00 to 13.00 (morning work)
3. Block websites from 14.00 to 19.00 (afternoon work)
4. Block websites from 21:00 to 24:00 (evening work)
5. Block websites all day long except Sunday (always block)


## Requirements
* [SelfControl](selfcontrolapp.com);
* OSX 10.9 or higher;
* administrator rights;
* (optional) [LaunchControl](www.soma-zone.com/LaunchControl/).

OSX version and admin rights are needed because I use a script library; with some modifications of `Discipline.scpt` one could turn the scripts into a self-contained app and extend support to older versions of Applescript.

I use LaunchControl to easily view and manage the launch agents.

## Installation and configuration

#### Install the script library

Either run the `install.sh` script, or copy the `Discipline.scpt` library file to your Script Libraries folder.

#### Schedule a block

You can look at the premade examples to have a feel of how a block is formatted into a preference list file with a xml structure. These files define an agent (a daemon) that is run by `launchd` and executes an action whenever some condition occurs.

The most important keys in a `.plist` file are:

 * `Label` the name of the agent;
 * `ProgramArguments` the action run by the agent;
 * `StandardErrorPath` the path to the error log for when the agent fails;
 * `StartCalendarInterval` the weekdays and times when to run the agent;

The action in `ProgramArguments` consists always in the same bash command:

```bash
osascript -e tell script \"Discipline\" to block_me(\”[start time]\”, \"[end time]\", [grace period])
```

where the first two arguments are the start and end time of the block in `hh:mm` 24-hour format, and the third is the grace period (in seconds) between the warning notification and the block’s actual start.

The times in `StartCalendarInterval` should coincide with the start time of the block.

For more information on how to set up an agent, refer to the Configuration tab at [www.launchd.info/]()

#### 'Install' a block

The `.plist` files should be put into the `~/Library/LaunchAgents` folder, and will be loaded at the next user login. If you want to load them immediately, you can run

```bash
launchctl load ~/Library/LaunchAgents/[filename].plist
```

#### Notes on installation

You can choose to install library and schedules on your user-specific `$HOME/Library/` folder (the default), or on the shared `/Library/` common to all accounts. In the former case, Discipline will only run when that user logs in.

## Known Issues

* If the scheduled period includes midnight (ex. it goes from 10pm to 2am), it *might* not work properly. If this is the case for you, just create two agents, one until 11.59pm and one starting at 0.00am.

* Applescript always expects the script library to be located in the same `Library/Script Libraries` folder. If you want to put `Discipline.scpt` somewhere else in your filesystem, you should create a Finder alias by running this command on the console:

```bash
osascript -e 'tell application "Finder" to make alias file to POSIX file "[/folder/that/contains]/Discipline.scpt" at POSIX file "/Users/[Username]/Library/Script Libraries" '
```

