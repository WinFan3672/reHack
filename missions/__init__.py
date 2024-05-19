from resource.classes import *
import resource.information as resourceInfo
from resource.libs import *
from game.player import *
import data
from game.programs import (
    Mission,
    BlankMission,
    LANMission,
    NestedLANMission,
    ConnectMission,
    NMapMission,
    BuyMission,
    pickSelection,
    MailAccount,
    FileCheck,
    FileCopiedCheck,
    ZippedFileCopiedCheck,
    FileDeletedCheck,
    FileCheckMission,
    HostKillMission,
    NodeCheckMission,
    NodeCheck,
    UserNodeCheck,
    FunctionMission,
)
import nodes
import nodes.forum
import nodes.lan
import nodes.test



def pentest2_end():
    node = data.getNode("cinnamon.mail.com")
    data.addFirewall("cinnamon.mail.com", Firewall("cinnamon"))
    node.accounts = [MailAccount("admin")]
    node.minPorts = 65536


def chan_missions(self):
    """
    Missions located in the "Jobs" board in 5chan.
    """
    bodies = [
        [
            "Right. You might have heard of the game World of Legends. It's fairly popular, and I've recently found out that it's peer-to-peer.",
            "This means that I can quite easily find the IP's of any player I play with.",
            "Earlier today, I played against someone who was really, really good. So good, in fact, that I'm quite sure they were cheating.",
            "(I say 'quite sure', but they were casting spells from across the map with a level three character.)",
            "",
            "Because I hate cheaters, I want them to get what they deserve.",
            "Their system can't be that secure, so could you connect to their PC and delete some system files?",
            "That should put them out of action for a couple days, since they'll need to reinstall their system and find their cheats again.",
            "Oh, yeah the address: {}".format(data.getNode("5chan_mission1").address)
        ],
        [
            "I imagine you've heard of the new DCSE online platform.",
            "Well, I have a great idea on how to cause some chaos. Think of it as hacktivism.",
            "The DCSE trading platform is built off standard software that is known to have an off-switch. Hack in and shut down the exchange.",
            "Oh, and most importantly, don't delete anything, we don't want to cause lasting damage, just confusion.",
            "The DCSE website can be found here: dcse.com",
        ],
        [
            "Blue Medical are a big technology company who manufacture medical devices, like pacemakers and such.",
            "Their devices operate using a proprietary communications protocol. Attempts to reverse-engineer such a protocl have failed thus far.",
            "If the hacking community got ahold of the source code to some firmware, this would be a big deal. It would allow for people to tinker",
            "with their devices, doing things like reading the data off the device out of curiosity, and potentially find security vulnerabilities"
            "to report to BM. It sounds like a good idea, doesn't it?",
            "",
            "Well, their LAN is like Fort Knox. I imagine it'd be a good challenge for you to get in.",
            "Hack into it for now and we'll see where to go from here.",
            "Their website is here: bluemedical.com",
        ],
        [
            "You may have heard of NTP, the protocol that syncs up your computer with the atomic clocks measuring time to insane degrees of accuracy.",
            "Well, NanoSoft Workspaces has a minor flaw: it relies on a single time server (time.workspaces.com). As such, if it goes down, a lot of systems will",
            "end up with out of sync clocks. Over time, this causes more and more issues.",
            "If you do this properly, NanoSoft might not notice for some time, leading to chaos.",
            "What are you waiting for?",
        ],
    ]
    end_email = Email(
        "null@null.null", 
        "{}@jmail.com".format(self.name),
        "Mission Complete",
        "Congratulations on the successful mission. Payment should be credited within the next 2 business days.",
    )
    bodies = ["\n".join(x) for x in bodies]
    emails = [
        Email(
            "null@null.null",
            "{}@jmail.com".format(self.name),
            "Die, Cheater",
            bodies[0],
        ),
        Email(
            "null@null.null",
            "{}@jmail.com".format(self.name),
            "Sharing Is Caring",
            bodies[1],
        ),
        Email(
            "null@null.null",
            "{}@jmail.com".format(self.name),
            "Blue Blood Spilled",
            bodies[2],
        ),
        Email(
            "null@null.null",
            "{}@jmail.com".format(self.name),
            "I Can't Tell The Time",
            bodies[3],
        ),
    ]
    return [
        HostKillMission(
            self,
            "5chan_mission1",
            "Die, Cheater",
            "5chan_mission1",
            emails[0],
            end_email,
            reward=650,
        ),
        FunctionMission(
            self,
            "5chan_mission2",
            "Sharing Is Caring",
            data.getNode("dcse").check_locked,
            emails[1],
            end_email,
            reward=4500,
        ),
        BlankMission(
            self,
            "5chan_mission3",
            "Blue Blood Spilled",
            "bluemedical_ftp",
            emails[2],
            end_email,
            reward=1500,
        ),
        HostKillMission(
            self,
            "5chan_mission4",
            "I Can't Tell The Time",
            "workspaces_time",
            emails[3],
            end_email,
            reward=500,
        ),
    ]


def base_missions(self):
    bodies = [
        [
            "We see you have helped a client secure their network.",
            "In every mission in our Pentest Series, we like to include a secret CTF-style challenge at the end.",
            "We'd like you to hack into the same network the client just secured, and if you hack it, we'll pay you nicely.",
            "If you can't hack in, just cancel the mission. We get it. Not all sysadmins suck at their job."
            "Good luck!",
        ],
        [
            "Well done. Your generous payment has been provided.",
            "The client has not been informed about this.",
            "Please keep this a secret, in order to keep the spirit of the CTF challenges going."
        ],
    ]
    bodies = ["\n".join(x) for x in bodies]
    emails = [
        Email(
            "contracts@rehack.org",
            "{}@jmail.com".format(self.name),
            "CTF: JMail (7500 Cr. Reward)",
            bodies[0],
        ),
        Email(
            "contracts@rehack.org",
            "{}@jmail.com".format(self.name),
            "Mission Complete",
            bodies[1],
        ),
    ]
    return [
        Mission(
            self,
            "pentest1_ctf",
            "CTF: JMail",
            "jmail",
            emails[0],
            emails[1],
            reward=7500,
        ),
        Mission(
            self,
            "pentest2_ctf",
            "CTF: Mail.com",
            "cinnamon.mail.com",
            emails[0],
            emails[1],
            reward=5500,
        ),
    ]


def main_story_missions(self):
    def mission1_end():
        def action1():
            player = data.getNode("localhost")
            mht = data.getNode("mht")
            with open("msgboard/mht.com/mountain2") as f:
                story = mht.add_story("Mountain View Leaker Arrested", "Admin", player.date.clone(), f.read())
                story.reply("bit", "did not expect so much to happen so quickly")
                story.reply("admin", "I had a hunch something like this would happen; just think how many billions of $'s IsDedCo makes from soft drink sales.")
                story.reply("mindman", "IDCO is down 76%, whereas COCA is up 366% on the DCSE (DC Stock Exchange), isn't it crazy?")
        player = data.getNode("localhost")
        mht = data.getNode("mht")
        chan = data.getTorNode("5chan").get_board("News")
        dcsebets = data.getNode("nerdnet").get_board("n/dcsebets")
        ftp = data.getNode("mhtftp")
        with open("msgboard/mht.com/mountain") as f:
            story = mht.add_story("Mountain View Recipe Leaked", "Admin", player.date.clone() + 1, f.read())
            story.reply("bit", "This is WILD, must be a reHack agent at work")
            story.reply("admin", "bit: wouldn't surprise me, reHack's been in the (non-mainstream) news all year (e.g ColonSlash's garbage 'exposé')")
            story.reply("bit", "that article really WAS garbage")
            story.reply("rehack", "admin: funnily enough, i tried to send a cease-and-desist but it appears as if the owner ran off without a trace")
            story.reply("rehack", "old articles gone, no response to ANY emails, nobody knows what happened")
            story.reply("admin", "rehack: sounds like a story in the making")
            story.reply("newt", "who do you think it is?")
            story.reply("rehack", "i have my suspicions, must be an ex-agent of mine, which narrows it down a LOT (not many agents leave on bad terms)")
            story.reply("bit", "rehack: can you even cease-and-desist for that?")
            story.reply("rehack", "100%, it's defamation of the highest order")

            post = chan.add_topic("mht", "Mountain View Recipe Leaked", f.read())
            post.reply("admin", "NOTE: This was Syndicated from mht.com")
            post.reply("byte", "what. the. hell.")
            post.reply("isdedman", "isded really is dead :(")
            post.reply("byte", "good one, but yeah you're right")
            post.reply("stocknerd", "guys, COCA's gonna be on the up-and-up because of this, better buy, buy, buy")
            post.reply("stocknerd", "and IDCO is gonna be down like crazy, so better short, short, short")
            post.reply("byte", "isn't time in the market > timing the market?")
            post.reply("stocknerd", "not if it's a short squeeze, and this is gonna be one hell of a short squeeze")

        short = dcsebets.add_topic("u/stocknerd", "SHORT SQUEEZE: COCA UP, IDCO DOWN", "I anticipate that IDCO will go down a LOT, and COCA will go up: mht.com")
        short.reply("u/admin", "The hedge funds are already doing it, breaks the point of n/dcsebets")
        short.reply("u/stocknerd", "Shorting IDCO? Don't think so.")
        short.reply("u/spill", "i've spent 10k on COCA stock, it's been down for a while, so I expect it to peak at its previous peak in ~6 months' time")
        with open("data/mview_recipe.txt") as f:
            ftp.pub.create_file("MountainViewRecipe.docx", f.read(), "mhtftp")
        player.actions.append(Action(player.date.clone() + 1, action1))

    def pentest1_end():
        jmail = data.getNode("jmail")
        jmail.hacked = False
        jmail.minPorts = 255
        for user in jmail.users:
            if user.name == "admin":
                user.password = data.genString(16)
                adminPass = user.password
        for account in jmail.accounts:
            if account.name == "admin":
                account.password = "firefly"
        data.addFirewall(jmail, Firewall("jmail", 5))

        ## Send ransom email
        body = "\n".join([
            "HELLO.",
            "WE RECENTLY NOTICED THAT YOU HAVE SECURED YOUR NETWORK, WITH HELP FROM REHACK.",
            "WE HAVE 2TB OF CLASSIFIED DOCUMENTS WE INTEND TO RELEASE. THE DOCUMENTS INCLUDE YOUR FINANCIAL DATA AS WELL AS",
            "EVIDENCE OF FRAUD AND CORPORATE ESPIONAGE THAT YOU, JOHN MALLEY, HAVE COMMITTED.",
            "",
            "HOWEVER, WE ARE NOT ENTIRELY EVIL. WE WOULD BE WILLING TO DELETE THIS DATA, IF YOU SEND THE PASSWORD",
            "TO YOUR ADMIN PANEL TO THE FOLLOWING EMAIL ADDRESS:",
            "",
            "darkgroup1337@jmail.com",
            "",
            "WE ARE WAITING.",
        ])
        email = Email("darkgroup1337@jmail.com", "admin@jmail.com", "YOU HAVE BEEN WARNED", body)
        sendEmail(email)

        jmail.accounts.append(MailAccount("darkgroup1337", "letmein"))

        sendEmail(Email("admin@jmail.com", "darkgroup1337@jmail.com", "Re: YOU HAVE BEEN WARNED", adminPass))
    bodies = [
        [
            "Welcome, fellow hacker.",
            "This tutorial covers the 'scan' command.",
            "If you have root access to a node and it has ssh installed, you can run several commands."
            "One of them is 'scan'. It lists all nodes linked to a node.",
            "This is extremely useful as it allows you to search through more of a network that is normally hidden.",
            "",
            "To demonstrate, connect to coca.com and hack in.",
            "Once you've done that, connect to it and run the scan command and find the mainframe password.",
            "Using the mainframe password, log in using the login command.",
            "",
            "You may encounter the following nodes:",
            "* A mail server",
            "   * This is really easy to break into and should have a lot of useful info.",
            "* A mainframe",
            "   * This needs a password.",
            "* A few employee nodes.",
            "   * Hack in and run 'ls'. You never know if they left some text notes.",
            "",
            "A few tips:",
            "* You can use 'bruter' to brute-force admin passwords instead of searching.",
            "* Similarly, 'emailbruter' brute-forces emails."
            "* You can use 'mailman' to log into email accounts if you find them.",
            "   * If you find the admin password, don't bother with looking at individual accounts. Use 'login' and connect, because it lets you see everything.",
            "* Refer to the wiki (wiki.rehack.org) if you're stuck.",
        ],
        [
            "Hello again.",
            "Welcome back to another advanced tutorial.",
            "",
            "Sometimes, the admin password is easy to guess.",
            "So easy in fact, that your own computer can crack it.",
            "Allow me to introduce bruter.",
            "Bruter is built into reHackOS and allows you to brute-force an admin password.",
            "As a demonstration, hack into: bruter.rehack.test and guess the admin password.",
            "",
            "See you on the other side.",
        ],
        [
            "Hello again.",
            "Welcome back. Some nodes have firewalls.",
            "Firewalls are another hoop you must jump over.",
            "As a demonstration, break into firewall.rehack.test.",
            "You'll need to purchase 'firewall' from the store.",
            "Once you've broken in, finish the mission.",
        ],
        [
            "Hello. I am the sysadmin for the Mountain View Intranet.",
            "I have become increasingly disenchanted with my work here, as I feel that I will be replaced any second now.",
            "As such, I'd like to acquire a small payday for myself, with your help of course.",
            "A fellow employee of mine keeps uploading encrypted copies of the Mountain View Recipe File password on our FTP server.",
            "I have to keep deleting them for security purposes, but this time, I haven't noticed that he's done it again, wink wink.",
            "I need you to do the following:",
            "",
            "1. Hack into our intranet (intranet.mountain.view). I won't give you the password because that's too obvious.",
            "2. Connect to the Intranet. You can use `lanconnect` or similar software.",
            "3. Hack into our ftp server (located at ftp.local).",
            "4. Using the header data from that Password file, find my colleague's computer and hack into that. I think it's in his home folder.",
            "5. Find the password for the archive.",
            "6. Jump back into our FTP server and decrypt the archive with the password in the password file.",
            "7. Upload the decrypted file to the reHack drop server (drop.rehack.org)."
            "",
            "Once this happens, who knows. Maybe I'll sell the recipe on the black market, or to the Coca Corporation, although they have a history of not accepting those offers.",
        ],
        [
            "No way, you did it! Was it too hard? I hope not.",
            "I'm gonna stash the recipe for later, and encrypt it with my *own* DEC archive. The password for that one is 'mountainous', in case you're curious.",
            "Feel free to read the recipe for yourself, although from what I've just read, it might be worse for your health than ACTUAL mountain dirt.",
        ],
        [
            "Hello, fellow hacker.",
            "I need you to do the following:",
            "* Hack into the CIA's website: cia.gov",
            "* Find and hack into the CIA's LAN (I believe there's an Advanced Tutorial for that).",
            "* Find the server relating to Project Autocrat",
            "* Break into that and connect to it over FTP",
            "* There's a file in the `home` folder. Upload it to the drop server: drop.rehack.org",
            "",
            "Get back to me once you're done and I'll be sure to pay you VERY well.",
        ],
        [
            "Welcome to the Advanced Tutorial for LAN's.",
            "Most respected companies have a LAN set up in their building.",
            "These contain devices that can only be accessed from within the LAN.",
            "To actually hack into a LAN, you need 2 tools:",
            "",
            "* lanconnect",
            "This is built into your OS.",
            "* lancrack",
            "This costs 2500 credits.",
            "",
            "If you have the IP of a LAN's router, you can use lancrack to open port 1, and lanconnect to connect to it.",
            "Once you're in, you can connect to different devices on the network.",
            "However, you need a list of local IP's. Thankfully, the router you just connected to is located at `192.168.0.0`, and you can connect to it and see a list of devices.",
            "From there, you can hack whatever you need to hack.",
            "",
            "Using this knowledge, connect to `lan.rehack.test` and hack the machine with the hostname 'Hack me'.",
        ],
        [
            "Hello. I am the administrator of JMail, a popular email service. You might've heard of it.",
            "I am sick and tired of all the negative press our service gets due to its constant attacks.",
            "As such, I've configured JMail's servers to log extra information for the duration of this mission.",
            "I'd like you to hack JMail and get back to me, so that I can work out what I need to fix.",
            "Basic pentesting. Deal?",
        ],
        [
            "That was massively insightful.",
            "I have increased the security of the server:",
            "* A firewall was added.",
            "* I've installed port blockers to prevent port breaking.",
            "* I've set new passwords for both my user and the admin panel.",
            "",
            "Thanks for working with me.",
        ],
        [
            "It's no secret that Mail.com is known for its security, and not in a good way.",
            "With denunciations from many high-ranking cybersecurity firms, our future isn't very bright.",
            "We have a mail server called Cinnamon, which is used as a default config for our mail servers.",
            "It's located here: cinnamon.mail.com",
            "We'd like you to break into it. That's it. We WILL pay you highly, and WILL NOT report you anywere, least of all your employer.",
            "Go."
        ],
        [
            "Thanks for the quick work. As promised, we have wire 10,000 big ones over to your account.",
            "The Cinnamon server has been reset and security updates have been released.",
        ],
        [
            "Hack into ftp.debian.org and delete core.sys from the sys folder.",
            "The disruption caused by this will be significant.",
        ],
    ]
    bodies = ["\n".join(x) for x in bodies]
    end_email = Email(
        "contracts@rehack.mail",
        "{}@jmail.com".format(self.name),
        "Contract Complete",
        "Congratulations on completing the contract.\nIf you want to complete more contracts, visit contracts.rehack.org",
    )
    emails = [
        Email(
            "contracts@rehack.mail",
            "{}@jmail.com".format(self.name),
            "Advanced Tutorial #1: SSH",
            bodies[0],
        ),
        Email(
            "contracts@rehack.mail",
            "{}@jmail.com".format(self.name),
            "Advanced Tutorial #2: Brute-Force Attacks",
            bodies[1],
        ),
        Email(
            "contracts@rehack.mail",
            "{}@jmail.com".format(self.name),
            "Advanced Tutorial #3: Firewalls",
            bodies[2],
        ),
        Email(
            "contracts@rehack.mail",
            "{}@jmail.com".format(self.name),
            "Top of the Mountain",
            bodies[3],
        ),
        Email(
            "contracts@rehack.mail",
            "{}@jmail.com".format(self.name),
            "RE: Top of the Mountain",
            bodies[4],
        ),
        Email(
            "contracts@rehack.mail",
            "{}@jmail.com".format(self.name),
            "Project Autocrat",
            bodies[5],
        ),
        Email(
            "contracts@rehack.mail",
            "{}@jmail.com".format(self.name),
            "Advanced Tutorial #4: LANs",
            bodies[6],
        ),
        Email(
            "admin@jmail.com",
            "{}@jmail.com".format(self.name),
            "Pentesting Series: JMail",
            bodies[7],
        ),
        Email(
            "admin@jmail.com",
            "{}@jmail.com".format(self.name),
            "Thanks for your help",
            bodies[8],
        ),
        Email(
            "admin@root.mail.com",
            "{}@jmail.com".format(self.name),
            "Pentesting Series: Mail.com",
            bodies[9],
        ),
        Email(
            "admin@root.mail.com",
            "{}@jmail.com".format(self.name),
            "Thanks",
            bodies[10],
        ),
    ]
    test1_fc = FileCheck("debianftp")
    test1_fc.add(FileDeletedCheck("core.sys", "sys"))
    test2_fc = FileCheck("rhdrop")
    test2_fc.add(FileCopiedCheck("core.sys", origin="debianftp"))
    autocrat_fc = FileCheck("rhdrop")
    autocrat_fc.add(FileCopiedCheck("autocrat.docx", data.AUTOCRAT, origin="cialan"))
    mountain_fc = FileCheck("rhdrop")
    with open("data/mview_recipe.txt") as f:
        mountain_fc.add(FileCopiedCheck("Recipe.docx", f.read(), "mountainremote"))
    return [
        Mission(
            self,
            "advanced1",
            "Advanced Tutorial #1: SSH",
            "cocamain",
            emails[0],
            end_email,
            reward=750,
        ),
        Mission(
            self,
            "advanced2",
            "Advanced Tutorial #2: Brute-Force Attacks",
            "brutertest",
            emails[1],
            end_email,
            reward=750,
        ),
        Mission(
            self,
            "advanced3",
            "Advanced Tutorial #3: Firewalls",
            "firewalltest",
            emails[2],
            end_email,
            reward=1450,
        ),
        LANMission(
            self,
            "advanced4",
            "Advanced Tutorial #4: LANs",
            "hackme",
            "testlan",
            emails[6],
            end_email,
            reward=3500,
        ),
        FileCheckMission(
            self,
            "mission1",
            "Top of the Mountain",
            mountain_fc,
            emails[3],
            emails[4],
            reward=500,
            end_function=mission1_end,
        ),
        FileCheckMission(
            self,
            "autocrat",
            "Project Autocrat",
            autocrat_fc,
            emails[5],
            end_email,
            reward=10000,
            end_function = data.getNode("shodan").autocrat,
        ),
        Mission(
            self,
            "pentest1",
            "Pentesting Series: JMail",
            "jmail",
            emails[7],
            emails[8],
            reward=1500,
            end_function=pentest1_end,
            next_id="pentest1_ctf",
        ),
        Mission(
            self,
            "pentest2",
            "Pentesting Series: Mail.Com",
            "cinnamon.mail.com",
            emails[9],
            end_email,
            reward=2750,
            end_function=pentest2_end,
            next_id="pentest2_ctf",
        ),
    ]


def start_missions(self):
    bodies = [
        [
            "Welcome to reHack!",
            "",
            "As you're new here, you'll want to check out our intranet (intranet.rehack.org).",
            "You can do this using the 'connect' command.",
            "Our intranet contains some useful resources as well as some info for beginners such as yourself.",
            "We look forward to seeing you succeed.",
        ],
        [
            "Hello.",
            "",
            "I work for AnonMail, a reHack sponsor.",
            "AnonMail provides unlimited untraceable email addresses.",
            "A rehack.org email address is a huge red flag, and a jmail.com email is easy to trace.",
            "AnonMail is neither. We have over a million accounts, 99% of which are privacy-savvy users.",
            "As such, your email blends right in.",
            "You get a randomly generated username and get to receive up to 100,000 emails before your mailbox shuts down.",
            "",
            "To register, visit www.anon.mail and follow the instructions.",
        ],
        [
            "You have been personally invited to become a member of 5chan.",
            "5chan is a hacking forum consisting entirely of anonymous members, or anons.",
            "As a warning, 5chan is not for the faint of heart.",
            "",
            "Get 1337 hacking advice, share cybersecurity news, and shitpost until the end of the world.",
            "",
            "The Tor IP address for our signup service is here: {}".format(data.getTorNode("5chan-signup").address),
            "",
            "Signed:",
            "",
            "Anonymous,",
            "Chief Anon.",
        ],
        [
            "What is the price for having a mail server for the xwebdesign subdomain?",
            "We aim to have 25 accounts and want full security.",
        ],
        [
            "Dear {},",
            "Thank you for purchasing mail.com.",
            "See the invoice below:",
            "",
            "INVOICE",
            "MAIL.COM SERVER <MONTHLY>: $79.99",
            "INSTALLATION FEE <ONE-TIME>: $49.99",
            "",
            "Thank you for shopping with mail.com",
        ],
        [
            "Dear Joe",
            "See below the mail.com admin password:",
            "",
            "superuser",
            "",
            "I trust that jmail is secure enough that you won't somehow leak it.",
            "It's only the web portal, but you are the webmaster, so it's only fair.",
        ],
        [
            "This email server is reserved by W3D for the use of spoofing the FROM field of an email.",
            "Set the FROM field to null@null.null and SMTP will do the rest.",
            "The email server actively ignores any emails sent to it.",
            "If you send an email, it will be sent back to you and not stored.",
        ],
    ]
    bodies = ["\n".join(x) for x in bodies]
    emails = [
        Email(
            "welcome@rehack.mail",
            "{}@jmail.com".format(self.name),
            "Welcome to reHack",
            bodies[0],
        ),
        Email(
            "marketing@anon.mail",
            f"{self.name}@jmail.com",
            "AD: Try AnonMail",
            bodies[1],
        ),
        Email(
            "invites@5chan.mail.com",
            f"{self.name}@jmail.com",
            "A Personal Invitation",
            bodies[2],
        ),
        Email(
            "xwebdesign@jmail.com",
            "sales@root.mail.com",
            "Client: XWebDesign",
            bodies[3],
        ),
        Email(
            "sales@root.mail.com",
            "sales@xwebdesign.mail.com",
            "Invoice",
            bodies[4].format("XWebDesign"),
        ),
        Email(
            "sales@root.mail.com",
            "sales@jmail.mail.com",
            "Invoice",
            bodies[4].format("JMail"),
        ),
        Email("null@null.null", "null@null.null", "Notice", bodies[6]),
    ]
    mission_bodies = [
        [
            "Hello and welcome to reHack.",
            "I hope that you've been getting used to your Node.",
            "This is your first mission, out of many.",
            "This one's simple. You need to connect to the reHack Test Server.",
            "The IP address is: test.rehack.org",
            "If this works, you'll be denied access.",
            "",
            "Once you've connected once, you can run the 'mission' command.",
            "This command simply completes your mission. Simple, right?",
            "We'll find out.",
        ],
        [
            "OK. You did it. Now for the next bit.",
            "You need to run the nmap command on it.",
            "Run the following command:",
            "",
            "nmap test.rehack.org",
            "",
            "This will reveal the exposed ports on the node as well as how many you need to open.",
            "I'll be waiting.",
        ],
        [
            "You ran the nmap command, great. The output should have looked something like this:"
                "",
            "--------------------",
            "Found Target",
            "Hostname: reHack Test Server",
            "Min. Ports To Crack: 0",
            "--------------------",
            "[CLOSED] PORT 21: FTP",
            "[CLOSED] PORT 22: SSH",
            "--------------------",
            "",
            "As you can see, there are 2 closed ports: 21 and 22.",
            "The important part is the 'Min. Ports To Crack' section.",
            "It shows how many you need to open to hack the device.",
            "This node has weak security, so it can be hacked instantly.",
            "Let's do it!",
            "",
            "Use the porthack command on test.rehack.org.",
            "Once you're done, run 'mission' and read my next email.",
        ],
        [
            "Good job.",
            "Now for a bit of an explanation.",
            "",
            "There are different types of nodes (devices connected to the Internet).",
            "As such, some of them do different things, and have different levels of security.",
            "When you connect to a node as a normal user, it can do one thing, such as display a webpage, or just deny access.",
            "When you hack in, it performs a different function, such as opening an admin panel or allowing you to run commands on it.",
            "",
            "With multiple types of security comes multiple ways to break it. For instance, you may one day stumble on a node's admin password.",
            "If this happens, you can run the following command:",
            "",
            "login <IP address> <password>",
            "",
            "This will break into the system in the same way porthack does, but without you forcing your way in.",
            "",
            "Try it. The admin password for one of our throwaway test servers is 'trollface'.",
            "The IP address is {}.",
        ],
        [
            "You're doing well. Now for a REAL test.",
            "A forum called ColonSlash has been spreading lies about us.",
            "We as a collective are not pleased.",
            "I would like you to break in.",
            "If you run nmap, you'll notice that ports 21 and 22 are exposed.",
            "There are 2 built-in programs that expose those ports.",
            "To expose port 21, you use ftpkill.",
            "To expose port 22, you use sshkill.",
            "",
            "You need to do the following:",
            "* Hack colonsla.sh;",
            "* Run `ftp colonsla.sh`;",
            "* Navigate to `sys` and delete `core.sys`",
            "",
            "This will shut down their message board, although probably not permanently.",
        ],
        [
            "Good job. You completed the tutorial.",
            "If you want to complete more contracts, our contract server (contracts.rehack.org) is full of them.",
            "Alternatively, you could always look for companies to break into in your free time. A good list is the W3D (w3d.org).",
            "If you need help, our Intranet is a good resource: intranet.rehack.org",
            "If you find a new form of security and need specific help on it, the Wiki (wiki.rehack.org) is for you.",
            "",
            "Keep this email for reference purposes, and good luck.",
        ],
    ]
    mission_bodies = ["\n".join(x) for x in mission_bodies]
    missionEmails = [
        Email(
            "contracts@rehack.mail",
            f"{self.name}@jmail.com",
            "Tutorial Mission Pt. 1",
            mission_bodies[0],
        ),
        Email(
            "contracts@rehack.mail",
            f"{self.name}@jmail.com",
            "Tutorial Mission Pt. 2",
            mission_bodies[1],
        ),
        Email(
            "contracts@rehack.mail",
            f"{self.name}@jmail.com",
            "Tutorial Mission Pt. 3",
            mission_bodies[2],
        ),
        Email(
            "contracts@rehack.mail",
            f"{self.name}@jmail.com",
            "Tutorial Mission Pt. 4",
            mission_bodies[3].format(data.getNode("test2").address),
        ),
        Email(
            "contracts@rehack.mail",
            f"{self.name}@jmail.com",
            "Tutorial Mission Pt. 5",
            mission_bodies[4],
        ),
        Email(
            "contracts@rehack.mail",
            f"{self.name}@jmail.com",
            "You Finished The Tutorial",
            mission_bodies[5],
        ),
    ]
    for item in emails:
        sendEmail(item)
    MISSIONS = base_missions(self)
    MISSIONS += [
        ConnectMission(
            self,
            "start1",
            "Start (Pt. 1)",
            "test.rehack.org",
            missionEmails[0],
            reward=500,
            next_id="start2",
        ),
        NMapMission(
            self,
            "start2",
            "Start (Pt. 2)",
            "test.rehack.org",
            missionEmails[1],
            reward=500,
            next_id="start3",
        ),
        Mission(
            self,
            "start3",
            "Start (Pt. 3)",
            "test.rehack.org",
            missionEmails[2],
            reward=500,
            next_id="start4",
        ),
        Mission(
            self,
            "start4",
            "Start (Pt. 4)",
            "test2",
            missionEmails[3],
            reward=500,
            next_id="start5",
        ),
        HostKillMission(
            self,
            "start5",
            "Start (Pt. 5)",
            "colonsla.sh",
            missionEmails[4],
            reward=500,
            end_email=missionEmails[5],
        ),
    ]
    return MISSIONS

def scsi(self):
    def thatcd_end():
        """
        This function is the end function for the scsi_thatcd mission.
        """
        player = data.getNode("localhost")
        that = data.getNode("thatcd")
        that.hacked = False
        that.minPorts=65536
        that_irc = data.getNode("thatirc")
        that.users = [x for x in that.users if x.name != "septic"]
        that_irc.create_user(self.name, self.password)

        dm = that_irc.add_direct_message(["admin", player.name])
        dm.add_message("admin", "Hello @{}".format(player.name))
        dm.add_message("admin", "I was watching you while you broke into our system.")
        dm.add_message("admin", "I watched as you added a new user (septic) over ssh")
        dm.add_message("admin", "I have enough evidence to take to the police")
        dm.add_message("admin", "However, I'm better than that.")
        dm.add_message("admin", "septic isn't welcome in our forum, and nor are you. I wish you the best.")

        sendEmail(Email(
            "null@null.null",
            "{}@jmail.com".format(player.name),
            "[irc.that.cd] You have been invited to our IRC Server",
            """Hello!
You have been invited into the ThatCD IRC Server. The admin has already messaged you. Please log in with your reHack credentials."""
            ))
    
    def ffc_end():
        player = data.getNode("localhost")
        mht = data.getNode("mht")
        mhtforum = data.getNode("mhtforum")
        mhtftp = data.getNode("mhtftp")
        chan = data.getTorNode("5chan")
        nerdnet = data.getNode("nerdnet")

        with open("msgboard/mht.com/ffc") as f:
            story = mht.add_story("FFC Herb And Spice List Leaked", "Admin", player.date.clone(), f.read())
            story.reply("bit", "first IsDedCo, now FFC, what is happening?")
            story.reply("sizzle", "i bet rehack is behind it")
            story.reply("rehack", "none of our agents did it, that's all we can say")
            story.reply("hmm", "then it must be someone more elite")
            story.reply("bit", "the way they described it, it doesn't seem elite to me")
            story.reply("suspicions", "maybe 5chan did it? VCFORUM? SCSI, even?")
            story.reply("rehack", "whoever it is, they're continuing what the first leak started")
            story.reply("septic", "i know for a fact that more targets are coming :)")

        with open("data/ffc.txt") as f:
            mhtftp.pub.create_file("HerbsAndSpices.docx", f.read())

        dcsebets = nerdnet.get_board("n/dcsebets")

        nerdnet.duck = dcsebets.add_topic("u/dcsekiller", "Buy DUCK Now", """The recent MHT post is bad for FFC. Buy DUCK, it'll go up!""")
        nerdnet.duck.reply("u/foundation", "this may end badly")
    
    def dec_end():
        mht = data.getNode("mht")
        player = data.getNode("localhost")
        mhtftp = data.getNode("mhtftp")
        nerdnet = data.getNode("nerdnet")
        xdgnet = data.getNode("xdgnet")
        debnews = data.getNode("debnews")

        with open("msgboard/mht.com/dec") as f:
            story = mht.add_story("DEC Solutions Hacked, Source Code For Encryption Suite Leaked", "Admin", player.date.clone(), f.read())
            story.reply("bit", "another hack?")
            story.reply("admin", "2010 will be remembered as a bad year for governments and corporations alike")
            story.reply("null", "i knew there was something off with DEC, it even has an official brute-force program")
            story.reply("null", "s/official/internal")
            story.reply("admin", "i tried decbruter, and it takes ~3s to brute-force a DEC archive with a 64-character password, not good")
            story.reply("admin", "to be fair that was on a top-of-the-line GPU (Evasia SuperForce 480)")
            story.reply("entropy", "and considering the fact most ppl don't use such long passwords...")
            story.reply("admin", "the GUI actually limits you to 24-character passwords, which I can decrypt fast enough to have a frame rate")
            story.reply("suspicions", "DEC 2.0 better be more secure when it comes out")
            story.reply("digit", "but what do we use until then?")
            story.reply("admin", "something like VertCrypt, probably")
        if xdgnet:
            with open("msgboard/xdg.net/dec") as f:
                story = xdgnet.add_story("Debian Drops libdec From Its OS", "Jacob Marksman", player.date.clone(), f.read())

        with open("msgboard/debian/dec") as f:
            debnews.add_story("Debian Will Remove libdec Starting With Debian 5.0.6", "Debian Team", player.date.clone(), f.read())

        data.copyFile("rhdrop", "mhtftp", "dec-src-v1.0.zip", "incoming", "pub")

        technology = nerdnet.get_board("n/technology")

        nerdpost = technology.add_topic("u/admin", "DEC Solutions hack looks bad", "See full article: mht.com")
        nerdpost.reply("u/bit", "debian has ALREADY dropped libdec from their distro")
        nerdpost.reply("u/rehack", "sadly, i cannot claim the trophy of responsibility")
        nerdpost.reply("u/admin", "who did it then?")
        nerdpost.reply("u/vcforum", "it wasnt any of our members, apparently the poster tried to pin the blame on us")
    
    def vcf_end():
        player = data.getNode("localhost")
        vcforum = data.getTorNode("vcforum")
        vcforum.create_user(player.name, player.password)
        sendEmail(Email(
            "null@null.null",
            "{}@jmail.com".format(player.name),
            "VCFORUM Tor Address",
            vcforum.address,
        ))

    end_email = Email("null@null.null", "{}@jmail.com".format(self.name), "Mission Complete!", "Thanks for working with SCSI group.")

    that_nc = NodeCheck("thatcd")
    that_nc.add(UserNodeCheck("septic", "password"))

    ffc_nc = FileCheck("rhdrop")
    ffc_nc.add(FileCopiedCheck("HerbsAndSpices.docx", origin="ffcftp"))

    dec_nc = FileCheck("rhdrop")
    dec_nc.add(ZippedFileCopiedCheck("dec-src-v1.0.zip", origin="roynet", folder="incoming"))

    vcf_nc = FileCheck("bravado_ftp")
    vcf_nc.add(FileDeletedCheck("Bravado2010.zip"))


    bodies = [
        [
            "Hello and welcome to SCSI. As an introductory task, we'd like you to assist a friend of ours with joining a website.",
            "Have you heard of that.cd? It's a private BitTorrent tracker specialising in music. It has something like 1,000,000 torrents, all of which are uploaded at the highest quality.",
            "Unfortunately, that.cd is notoriosuly difficult to enter, and our friend here has tried the interview process and failed.",
            "That's where you come in.",
            "I want you to hack into the forum and ssh into it. Then, run this command:",
            "",
            "user add septic password",
            "",
            "This will create a new user 'septic' with the password 'password'.",
            "Security should be minimal, that.cd has a pretty bad reputation when it comes to making sure their Apache server and such is up-to-date.",
        ],
        [
            "So, you might have heard about the Mountain View heist in the news. I heard somewhere that the guy who did it ended up here, at SCSI.",
            "I want the string of heists to continue: let's target FFC.",
            "I hear they have an FTP server with important documents inside that just so happens to be accessible to the public.",
            "By default, FTP servers are poorly secured, so why don't you give it a go? Hack in and send the herbs and spices list to our drop server!",
            "Their website: ffc.com",
            "Our dropserver: drop.rehack.org",
        ],
        [
            "You've likely dealt with a .dec file before, right? It's an encrypted file that is quite flawed, yes?",
            "Well, I have a hunch that the software has some security issues. As such, I think we should steal the source code.",
            "I reckon this'll be a little complex, but their website should be a good starting point.",
            "Get inside their network, find the source code (should be in a .zip somewhere), and send it to the dropserver.",
            "",
            "Website: dec.com",
            "Dropserver: drop.rehack.org",
        ],
        [
            "Are you good enough for VCFORUM? Let's find out.",
            "The new Bravado 2010 has just been announced, and the design hasn't been revealed yet.",
            "As a luxury car enthusiast, this interests me. Unfortunately for Bravado, I am not a fan of their company.",
            "Their cars suck. Peroid. I want you to sabotage the launch of their new car by hacking in and deleting the engineering drawings and such.",
            "I don't know HOW you will do this, but I hope you do. Their website is here: bravado.com"
        ],
        [
            "No way, you did it! Well, you earned it. I've added you to VCFORUM.",
            "You can log in with the same username and password as your SCSI account.",
            "I've also sent a second email with the .onion address of VCFORUM, since you'll need that as well.",
        ],
    ]
    bodies = ["\n".join(x) for x in bodies]
    emails = [
        Email(
            "null@null.null",
            "{}@jmail.com".format(self.name),
            "Introductory Mission: ThatCD",
            bodies[0],
        ),
        Email(
            "null@null.null",
            "{}@jmail.com".format(self.name),
            "Peanuts And Chicken", ## So-called because it's about a chicken shop and it's peanuts (old-time slang for 'easy')
            bodies[1],
        ),
        Email(
            "null@null.null",
            "{}@jmail.com".format(self.name),
            "Breaking Insecure Security",
            bodies[2],
        ),
        Email(
            "null@null.null",
            "{}@jmail.com".format(self.name),
            "VCFORUM Recruitement Test",
            bodies[3],
        ),
        Email(
            "null@null.null",
            "{}@jmail.com".format(self.name),
            "RE: VCFORUM Recruitement Test",
            bodies[4],
        ),
    ]
    return [
        NodeCheckMission(
            self,
            "scsi_thatcd",
            "Introductory Mission: ThatCD",
            that_nc,
            emails[0],
            end_email,
            reward=1500,
            end_function=thatcd_end,
        ),
        FileCheckMission(
            self,
            "scsi_ffc",
            "Peanuts and Chicken",
            ffc_nc,
            emails[1],
            end_email,
            reward=1500,
            end_function=ffc_end,
        ),
        # FileCheckMission(
        #     self,
        #     "scsi_dec",
        #     "Breaking Insecure Security",
        #     dec_nc,
        #     emails[2],
        #     end_email,
        #     reward=3500,
        #     end_function=dec_end,
        # ),
        FileCheckMission(
            self,
            "scsi_vcforum",
            "VCFORUM Recruitement Test",
            vcf_nc,
            emails[3],
            emails[4],
            end_function=vcf_end,
        ),
    ]

def main(self):
    nodes.forum.chan_jobs.topics += chan_missions(self)
    nodes.lan.scsi_jobs.missions = scsi(self)
    return start_missions(self) + base_missions(self) + main_story_missions(self) + scsi(self) + chan_missions(self)
