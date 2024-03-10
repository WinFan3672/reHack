0.4 is a massive release (in fact, the diff is 9000 lines long), so I've decided to read through all the changes to make a proper changelog.

# Engine Changes
* Added the concept of date and time. An in-game day lasts 10 real-life minutes, and is tracked courtesy of `time.time()`.
* Completely overhauled how files and folders are stored and handled.
* Programs have versions and descriptions.
* Each node has a `tick()` method, which is called after a command is run.
    - This is a minor change, but is actually massive. It allows to simulate multi-threaded operations while keeping the game single-threaded (see below note).
* Nodes now have a `check_health()` method which returns a boolean to determine whether or not that host is alive. The default behaviour is to check if `core.sys` exists in the `sys` folder.
* Nodes have a `motd` member, which displays a 'message of the day' to users that connect directly. The default is a generic Debian message.
## Why Is The Game Single-Threaded?
* I have very little experience making multi-threaded applications, which would massively increase the chance of technical debt occuring later in development.
* The game's code is quite large (6800 lines of Python, and 8,000 lines of text (if you ignore the 230,000-line password dictionary, which I will)), so making it multi-threaded would be a significant undertaking.
* It's not necessary. The game runs in the terminal. It's single-threaded by design. The current engine changes allow for simulating a multi-threaded experience anyway, so what's the point?

# Gameplay Changes
* Added a `history` command, which lists all nodes you've run the `connect` command on.
    - In future, I plan to make more commands mark the node as 'visited'.
* Signup services for email addresses now send emails.
    - The services that do this include JMail.
* You can now save and load the game. 
    - This is managed through a custom (and fully editable) file format located in the 'savegames' directory. 
    - NOTE: This is experimental and a LOT of data is not saved. This will be updated in future.
* A LOT of `debug` subcommands have been added, including `debug ide`, which opens a Python shell in the current game state.
* Added an `ftp` command, which opens an interactive file browser.
* Moved the `connect` shell to the new `ssh` program.
* Wikis have been overhauled, using a page and category system (note: they stills rely on the files in `wikis`).
* The MasterVPS service node (`mastervps.service`) has been overhauled with a proper interactive UI.

# Nodes
* New node types
    - Tor mail server
        - Can send/receive mail over Tor
    - Forum
        - Forums can have boards, boards can have topics, topics can have replies.
        - Forums can be private, meaning you need to log into a Forum account to access the forum's contents.
    - IRC Server
        - IRC servers can have channels, channels can have messages.
        - No IRC servers set up currently.
    - Search Engine
        - Is given a list of nodes
        - Allows you to search through them by name or IP address.
        - Currently two of them:
            - search.com
                - Contains a load of common websites
            - search.rehack.org
                - An extension of search.com with nodes that may help a hacker
    - Link tree
        - Displays the MOTD and then a list of links.
        - A public variant of a Node Tracker.
* New nodes
    - Debian
        - debian.org: Web server
        - ftp.debain.org: FTP server
        - git.debian.org: Version control server
    - MHT FTP Server
        - ftp.mht.com
    - Federal Government Databases
        - db.medic.gov: Medical DB
        - cb.crim.gov: Criminal DB

# Missions
* The Project Autocrat mission series has been condensed into a single mission that needs you to upload a file called autocrat.docx to the reHack Drop Server (drop.rehack.org)
* The tutorial mission series has been modified and extended to reflect current and future gameplay.

# End of Changelog
This isn't every change made (if you really want to know, clone the git repo and run `git diff v0.3.0 v0.4.0` and see all the changes to the source code), but it's the most important ones.
