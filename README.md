#Discipline

Using `launchd`, Applescript and SelfControl, three daemons will force me to keep a productive schedule.

1) Block sites from 1.00 to 7.00 (go to sleep)
2) Block sites from 9.00 to 13.00 (morning work)
3) Block sites from 14.00 to 18.00 (afternoon work)

Also:

* start even if in sleep
* notify 5 minutes before starting
* on 2) and 3), launch Pomodoro

## Installation notes:

Get current working directory, alias the library to the proper global folder

```
osascript -e 'set this_dir to do shell script "pwd"
set fromfile to this_dir & "/Script Libraries/Discipline.scpt"
tell application "Finder" to make alias file to POSIX file fromfile at POSIX file this_dir'
```

```
sudo mkdir "/Library/Script Libraries"
sudo mv Discipline.scpt "/Library/Script Libraries/Discipline.scpt"
```