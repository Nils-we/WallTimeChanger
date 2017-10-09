# WallTimeChanger
Python script which changes your desktop wallpaper according the time of the day

All this is based on [WeatherDesk](https://github.com/bharadwaj-raju/WeatherDesk) developed by [bharadwaj-raju](https://github.com/bharadwaj-raju) and [Martin Hansen](http://stackoverflow.com/users/2118300/martin-hansen) who build the original `Desktop.py` module.

# Installation

- Clone the repository to your wanted destination
- Install Python 3 or higher
- Create the `.walls` directory in ~/USER/ and the subdirectories according to your preferences, see [Wallpapers] (#Wallpapers)
- After that just run `WallTimeChanger.py`


**NOTE:** If you use OS X, see [the note for OS X users](#note-for-os-x-users).

## Options

    $ python3 WallTimeChanger.py --help 
    usage: WallTimeChanger.py [-h] [-d directory] [-f format] [-w seconds]
                          [-t [{2,3,4}]] [-n] [-o]
    WallTimeChanger - Change the wallpaper based on the time optional arguments:
    -h, --help            
                        show this help message and exit
    -d directory, --dir directory
                        Specify wallpaper directory. Default: ~/.walls
    -f format, --format format
                        Specify image file format. Default: .jpg
    -w seconds, --wait seconds
                        Specify time (in seconds) to wait before updating. Default: 600
    -t [{2,3,4}], --time [{2,3,4}]
                        Choose the amount of categories.
                        
                        Variations:
                          2 = day/night
                          3 = day/evening/night
                          4 = morning/day/evening/night [Default]
                        See --naming.
     -n, --naming          Show the image file-naming rules and exit.
     -o, --one-time-run    Run once, then exit.


## Wallpapers

**You can choose your own custom set**, conforming to the [naming rules](#naming-of-pictures).
Either put them in the default `~/.walls/` directory or specify a directory with the `--dir` option.

### Naming of Pictures

    $ python3 WallTimeChanger.py --naming
     This is how to name directories in the wallpaper (/.walls) directory:

	   for t -2: day, night
	   for t -3: day, evening, night
	   for t -4: morning, day, evening, night (this is the default setting)
     
     Please be sure it is exactly spelled like above. Otherwise it will not work.



## Supported Platforms 

- Linux

  - AfterStep
  - Awesome WM
  - Blackbox
  - Cinnamon
  - Enlightenment
  - Fluxbox
  - Gnome 2
  - Gnome 3
  - i3
  - IceWM
  - JWM
  - KDE **3**
  - LXDE
  - LXQt
  - Mate
  - Openbox
  - Pantheon
  - Razor-Qt
  - Trinity
  - Unity
  - Windowmaker
  - XFCE

- Windows

- OS X

## In background mode (only for OS X and Linux)

Run

```sh
$ nohup python3 WeatherDesk.py > /dev/null &
```

## Note for OS X users

Please disable the auto-reset/change of wallpaper in the  "Desktop and Screen Saver" preferences.

[![Disable this](http://i.imgur.com/BFi1GHGm.png)](http://i.imgur.com/BFi1GHG.png)

## Note for KDE users

Since KDE 4 and above does not provide an interface to change the desktop background, KDE 4 and above is not supported.

Any contributions on this welcome.
