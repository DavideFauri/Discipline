August 2020 edit: I'm archiving this repo since there is no need for this code anymore. I'm using [auto-selfcontrol](https://github.com/andreasgrill/auto-selfcontrol) now.

## Discipline

I created this small program to block my own procrastination attempts. It uses a combination of [`launchd`](http://www.launchd.info/) and Python to automatically launch SelfControl at predetermined times, blocking distracting websites.

## Features

SelfControl cannot be launched automatically on its own, and you have to set manually the length of time during which the block is active. This is fine when you only want to focus for 30 minutes, less so when you need to block distractions every day until 17:00, regardless of the time when you turn on your computer.

Discipline takes care of that, by letting the user select the end time until which to run SelfControl, in a "hh:mm" format.

It also gives a reminder warning and an amount of grace time before letting the block start. The default is 5 seconds, but it can be configured.

Some default templates are included in the `examples` folder:
1. Block websites until 7.00 (go to sleep)
2. Block websites until 13.00 (morning work)
3. Block websites until to 19.00 (afternoon work)


## Requirements
* [SelfControl](selfcontrolapp.com);
* OSX 10.9 or higher.

## Installation and configuration

The `install.sh` script is very minimal, and needs manual intervention before the script can work.

#### Schedule a block

You can look at the premade examples to have a feel of how a block is formatted into a preference list file with a xml structure. These files define an agent (a daemon) that is run by `launchd` and executes an action whenever some condition occurs.

The most important keys in a `.plist` file are:

 * `Label` the name of the agent;
 * `ProgramArguments` the action run by the agent;
 * `StandardErrorPath` the path to the error log for when the agent fails;
 * `StartCalendarInterval` the weekdays and times when to run the agent;

The action in `ProgramArguments` consists always in the same bash command:

```bash
discipline.py --until [hh:mm] --name [yourwifiSSID] --name [yourwifiSSID]
```

where the first argument is the end time of the block in `hh:mm` 24-hour format, and the other arguments are Wi-Fi networks SSIDs. If, when the script is launched, the current Wi-Fi SSID is not included in this list, the script quietly exists.

The times in `StartCalendarInterval` should coincide with the start time of the block.

For more information on how to set up an agent, refer to the Configuration tab at [www.launchd.info/]()

#### 'Install' a block

The `.plist` files should be put into the `/Library/LaunchDaemons` folder (you need admin rights for that), and will be loaded at the next user login. If you want to load them immediately, you can run

```bash
launchctl load /Library/LaunchDaemons/[filename].plist
```

## Known Issues

* I have not managed to make notifications working when launching the script from the root user.

* By design, any block longer than 12 hours will be ignored.

* On Catalina, the daemon cannot read the script if it is in a restricted folder - typically Documents, Downloads or Desktop. For this reason, the daemons refer to a hidden copy in the home folder.
