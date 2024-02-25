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
        )
import nodes

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
        "WE RECENTLY NOTICED THAT YOU HAVE SECURED YOUR NETWORK, WITH HELP FROM reHACK.",
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

def pentest1_ctf_end(self):
    jmail = data.getNode("jmail")

    jmail.hacked = False

    for user in jmail.users:
        if user.name == "admin":
            user.password = data.genString(32)

    jmail.accounts = [x for x in jmail.accounts if x.name != "darkgroup1337"]

    for account in jmail.accounts:
        if account.name == "admin":
            account.password = data.genString(32)
    
    body = "\n".join([
        "Hello.",
        "I have noticed that you recently fell for my honeypot.",
        "I'm not mad. I'm impressed; you managed to get my password, as well as the burner I created.",
        "I've changed the passwords for both my admin account and the console to be safe.",
        "The reason I'm not mad is simple; I was aware of these stupid CTF things, and I wanted proof they exist.",
        "So I added holes in the security and waited.",
        "You got your 7500. I got confirmation.",
        "I imagine reHack don't know that I know. I'd like you to keep it that way.",
        "If they find out that the CTF is publicly known, it destroys the credibility of their pentesting business.",
        "It also means they need to discontinue it, which makes the networks weaker because nobody is incentivised to test their new security.",
        "",
        "Anyway, I wish you all the best in your quest."
        ])
    email = Email(
            "admin@jmail.com",
            "{}@jmail.com".format(self.name),
            "You Fell For It",
            body
        )

    sendEmail(email)

def pentest2_end():
    node = data.getNode("cinnamon")
    data.addFirewall("cinnamon", Firewall("cinnamon", 5))
    node.accounts = [MailAccount("admin")]
    node.minPorts = 65536


def chan_missions(self):
    """
    Missions located in the "Jobs" board in 5chan.
    """
    bodies = [
        [
            "Welcome to 5chan.",
            "To fund your future escapades, this mission doesn't require you to do anything.",
            "Simply complete it and get your reward.",
        ]
    ]
    end_email = Email(
            "null", 
            "{}@jmail.com".format(self.name),
            "Mission Complete",
            "Payment should be credited within the next 2 business days.",
            )
    bodies = ["\n".join(x) for x in bodies]
    emails = [
        Email(
            "null",
            "{}@jmail.com".format(self.name),
            "Welcome To 5chan",
            bodies[0],
        ),
    ]
    return [
        BlankMission(
            self,
            "5chan0",
            "Welcome To 5chan",
            None,
            emails[0],
            end_email,
            reward=2500,
        ),
    ]


def investigate_missions(self):

    bodies = [
            [
                "Hello. This is [DATA EXPUNGED], Administrator of reHack.",
                "We have noticed that you recently assisted with the exposé of Project Autocrat.",
                "I know that the news hasn't started recycling the stories yet, but I'm not an idiot.",
                "You have proven yourself to be VERY skilled, especially since you joined so recently.",
                "It is obvious you have a lot of talent that needs nurtuting.",
                "Hopefully, you can take hints as well.",
                "I have some things that need investigating. If you agree to this, simply complete the mission to proceed.",
            ],
            [
                "Hack into this server: {}",
            ],
            [
                "Thanks for the help. You probably want an explanation, right?",
                "Well, I don't trust you enough to divulge that. As in, I don't trust anyone.",
                "So you can take your questions and thake them where the sun don't shine.",
                "",
                "[DATA EXPUNGED]",
                "reHack Administrator"
            ],
            ]
    bodies = ["\n".join(x) for x in bodies]
    emails = [
            Email(
                "admin@rehack.mail",
                "{}@jmail.com".format(self.name),
                "Investigations",
                bodies[0],
            ),
            Email(
                "admin@rehack.mail",
                "{}@jmail.com".format(self.name),
                "Investigations (Part 2)",
                bodies[1].format(data.getNode("shodan").address),
            ),
            Email(
                "admin@rehack.mail",
                "{}@jmail.com".format(self.name),
                "Investigations (Part 3)",
                bodies[1].format(data.getNode("testhub").address),
            ),
            Email(
                "admin@rehack.mail",
                "{}@jmail.com".format(self.name),
                "Investigations (Part 4)",
                bodies[1].format(data.getNode("dexpertweb").address),
            ),
            Email(
                "admin@rehack.mail",
                "{}@jmail.com".format(self.name),
                "Great Job",
                bodies[2],
            ),
            ]
    return [
            BlankMission(
                self,
                "investigate1",
                "Investigate",
                None,
                emails[0],
                next_id = "investigate2"
            ),
            Mission(
                self,
                "investigate2",
                "Investigate (Part 2)",
                "shodan",
                emails[1],
                next_id = "investigate3",
            ),
            Mission(
                self,
                "investigate3",
                "Investigate (Part 3)",
                "testhub",
                emails[2],
                next_id = "investigate4",
            ),
            Mission(
                self,
                "investigate4",
                "Investigate (Part 4)",
                "dexpertweb",
                emails[3],
                emails[4],
                reward=2500,
            ),
            ]

def autocrat_missions(self):
    end_email = Email(
            "contracts@rehack.mail",
            "{}@jmail.com".format(self.name),
            "Contract Complete",
            "Congratulations on completing the contract.\nIf you want to complete more contracts, visit contracts.rehack.org",
            )
    bodies = [
            [
                "This is weird. Very weird. Much weirder than anticipated.",
                "Using the servers linked to the website, I'm gonna need you to find the LAN for the CIA's Langley office.",
                "Once you've done that, hack it.",
                "You'll need a special tool (lancrack) to do it, but the previous mission's rewards should cover for that.",
                "Make this quick.",
                "Also, I saw that the CIA's mail server is linked to the website. Ignore it. It's useless to us.",
                ],
            [
                "Not bad.",
                "This really is a collaborative approach.",
                "I looked at the LAN and noticed it has some LAN's inside of LAN's, which is rather uncommon.",
                "However, it does have a 'Network Monitor', which I assume monitors traffic on the LAN and its sub-LANs.",
                "I need you to just hack that 'Network Monitor'. Should be easy.",
                ],
            [
                "I looked at the monitor you hacked, and it's strange.",
                "It definitely isn't made by the CIA, so I think this is some script kiddie packet sniffing or whatever.",
                "Looks like the CIA isn't all it's cracked up to be.",
                "How about that Server Room Net Switch? Can you break into that?",
                ],
            [
                "We're nearly done, I can feel it.",
                "I need you to hack into the `Target Companies and Orgs` node on that network we just hacked.",
                "Once you're done, get back to me."
            ],
            [
                "No way, you did it! Okay, this is crazy. We now have the Project Autocrat mainframe's IP address, courtesy of a LAN Tracker.",
                "All right. Hack into the mainframe.",
                "I think I know where the admin password is located: the CIA mail server (cia.mail.gov).",
                "The password should be easy to brute-force.",
            ],
            [
                "We did it. The information contained here is insane.",
                "I'll be making reports to various journalists, and hopefully, a massive story about it will break out.",
                "I've emailed the leader of VC-Forum to consider inviting you into the group. He'll get in touch soon, if he agrees.",
                "In the meantime, I think your (current) employer has something to say about all this, so you might not want to ignore that mission."
            ],
            ]
    bodies = ["\n".join(x) for x in bodies]
    emails = [
            Email(
                "contracts@rehack.mail",
                "{}@jmail.com".format(self.name),
                "Autocrat (Part 1)",
                bodies[0],
                ),
            Email(
                "contracts@rehack.mail",
                "{}@jmail.com".format(self.name),
                "Autocrat (Part 2)",
                bodies[1],
                ),
            Email(
                "contracts@rehack.mail",
                "{}@jmail.com".format(self.name),
                "Autocrat (Part 3)",
                bodies[2],
                ),
            Email(
                "contracts@rehack.mail",
                "{}@jmail.com".format(self.name),
                "Autocrat (Part 4)",
                bodies[3],
                ),
            Email(
                "contracts@rehack.mail",
                "{}@jmail.com".format(self.name),
                "Autocrat (Part 5)",
                bodies[4],
                ),
            Email(
                "contracts@rehack.mail",
                "{}@jmail.com".format(self.name),
                "Thanks for the work",
                bodies[5],
                ),
            ]
    return [
            Mission(
                self,
                "autocrat1",
                "Autocrat (Part 1)",
                "cialan",
                emails[0], 
                end_email,
                reward=2500,
                next_id="autocrat2"
                ),
            LANMission(
                self,
                "autocrat2",
                "Autocrat (Part 2)",
                "netmonitor",
                "cialan",
                emails[1],
                end_email,
                reward=2500,
                next_id="autocrat3",
                ),
            LANMission(
                self,
                "autocrat3",
                "Autocrat (Part 3)",
                "servers",
                "cialan",
                emails[2],
                end_email,
                reward=2500,
                next_id = "autocrat4",
                ),
            NestedLANMission(
                self,
                "autocrat4",
                "Autocrat (Part 4)",
                "targets",
                "cialan",
                "servers",
                emails[3],
                reward=15000,
                next_id = "autocrat5",
                ),
            Mission(
                self,
                "autocrat5",
                "Autocrat (Part 5)",
                "autocratmain",
                emails[4],
                emails[5],
                reward=15000,
                next_id = "investigate1",
                ),
            ]

def base_missions(self):
    bodies = [
            [
            "We see you have helped a client secure their network.",
            "In every mission in our Pentest Series, we like to include a secret CTF-style challenge at the end.",
            "We'd like you to hack into the same network the client just secured, and if you hack it, we'll pay you nicely.",
            "If you can't hack in, just cancel the mission. We get it. Not all sysadmins suck at their job."
            "",
            "Good luck!",
            ],
            [
                "Well done. Your generous payment has been provided.",
                "The client has not been informed about this.",
                "Please keep this a secret, in order to keep up with the spirit of the CTF challenges."
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
            end_function = lambda: pentest1_ctf_end(self),
        ),
    ]


def main_story_missions(self):
    bodies = [
            [
                "Welcome, fellow hacker.",
                "This tutorial covers the 'scan' command.",
                "In standard nodes (you can check a node's type using 'nodecheck'), there are several commands built in.",
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
                "* You can use 'mailman' to log into email accounts if you find them.",
                "   * If you find the admin password, don't bother. Use 'login' and connect, because it lets you see everything."
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
                "Hello. I need to be discreet about this as I am asking you to hack my employer.",
                "I want to access the secret recipe for Mountain View, and I know that it's on the mainframe.",
                "If you can get into their mainframe for me, I would be willing to pay you nicely for it.",
                "As a warning, their security is top notch and I doubt you'll be able to break in directly.",
                "You might need to fish around for the admin password or something.",
                "Get back to me if you find anything.",
                "",
                "Oh, yeah, their website is 'mountain.view'.",
                ],
        [
                "Hey, thanks a lot.",
                "The administration team is very small, so I guess you know who I am now.",
                "I found the recipe, so there's that.",
                "I'm gonna have to clear your tracks as well as mine, but I'm a sysadmin, I designed that mainframe, I can do it.",
                "I'm gonna hold onto the formula for a couple years before selling it on some kinda marketplace.",
                "",
                "Anyway, I wish you luck on your quest.",
                "Oh, and Mountain View contains flourine, so I don't think I'll be drinking it anytime soon.",
                ],
        [
                "Hello, fellow hacker.",
                "I think I just uncovered a conspiracy.",
                "I recently uncovered a secret CIA project called 'Project Autocrat'.",
                "It's really suspicious, and I need you to break into the CIA website (cia.gov).",
                "Then, I'll use the resources at my disposal to try and work out what Project Aurocrat is.",
                "Get going.",
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
                "If you have the IP of a LAN's router, you can use lancrack to opern port 1, and lanconnect to connect to it.",
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
                "Advanced Tutorial #1",
                bodies[0],
                ),
            Email(
                "contracts@rehack.mail",
                "{}@jmail.com".format(self.name),
                "Advanced Tutorial #2",
                bodies[1],
                ),
            Email(
                "contracts@rehack.mail",
                "{}@jmail.com".format(self.name),
                "Advanced Tutorial #3",
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
                "Hidden In The Depths",
                bodies[5],
                ),
            Email(
                "contracts@rehack.mail",
                "{}@jmail.com".format(self.name),
                "Advanced Tutorial #4",
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
    return [
            Mission(
                self,
                "advanced1",
                "Advanced Tutorial #1",
                "cocamain",
                emails[0],
                end_email,
                reward=750,
                ),
            Mission(
                self,
                "advanced2",
                "Advanced Tutorial #2",
                "brutertest",
                emails[1],
                end_email,
                reward=750,
                ),
            Mission(
                self,
                "advanced3",
                "Advanced Tutorial #3",
                "firewalltest",
                emails[2],
                end_email,
                reward=1450,
                ),
            LANMission(
                self,
                "advanced4",
                "Advanced Tutorial #4",
                "hackme",
                "testlan",
                emails[6],
                end_email,
                reward=3500,
                ),
            Mission(
                self,
                "mission1",
                "Top of the Mountain",
                "mountainmain",
                emails[3],
                emails[4],
                reward=500,
                ),
            Mission(
                self,
                "mission2",
                "Government Intervention",
                "ciaweb",
                emails[5],
                end_email,
                reward=2500,
                next_id = "autocrat1",
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
                "Pentesting Series: Mail.com",
                "cinnamon",
                emails[9],
                emails[10],
                reward=10000,
                )


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
                "We also use port masking and hide our MX records, meaning script kiddies can't break in easily.",
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
                "Hello,",
                "",
                "This is a message intended for easter egg hunters.",
                "Thank you for enjoying my game.",
                "I put a lot of effort into creating a lot of complex systems (such as mail servers)",
                "and I'm really proud of my work.",
                "All I can leave you with is a hint for some gameplay:",
                "",
                "There's a hidden ISP database that offers some pretty powerful functionality.",
                "It allows you to reassign any IP address, including your own, so that any traces you leave behind are gone.",
                "",
                "Connect to it: 1.1.1.1",
                "Before you do that, the admin password is [CENSORED]. Use the login command to take advantage of that.",
                "",
                "Signed,",
                "WinFan3672",
                "Creator of reHack",
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
            Email("null@null.null", "admin@winfan3672.mail.com", "A Message", bodies[6]),
            Email("null@null.null", "null@null.null", "Notice", bodies[7]),
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
                "Break into colonsla.sh and run 'mission' once you are done.",
                ],
        [
                "Great job. I'll be sure to poke around and get my revenge later.",
                "For now, you'll need to pick up some tools, if you will.",
                "The built-in software is great, but hackers often need new tools.",
                "That is where the software store comes in.",
                "The software store is accessible using the 'store' command.",
                "Using this software store, purchase the following software:",
                "",
                "* webworm",
                "* mxlookup",
                "",
                "The total cost is 500 credits. You should have more than enough.",
                "If not, you've softlocked yourself.",
                ],
        [
                "This is the final part of the tutorial.",
                "Hack into the following IP: test.hub",
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
                "Tutorial Mission Pt. 6",
                mission_bodies[5],
                ),
            Email(
                "contracts@rehack.mail",
                f"{self.name}@jmail.com",
                "Tutorial Mission Pt. 7",
                mission_bodies[6],
                ),
            Email(
                "contracts@rehack.mail",
                f"{self.name}@jmail.com",
                "You Finished The Tutorial",
                mission_bodies[7],
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
            Mission(
                self,
                "start5",
                "Start (Pt. 5)",
                "colonsla.sh",
                missionEmails[4],
                reward=500,
                next_id="start6",
                ),
            BuyMission(
                self,
                "start6",
                "Start (Pt. 6)",
                ["webworm", "mxlookup"],
                missionEmails[5],
                reward=500,
                next_id="start7",
                ),
        Mission(
                self,
                "start7",
                "Start (Pt. 7)",
                "test.hub",
                missionEmails[6],
                reward=2500,
                end_email=missionEmails[7],
                ),
    ]
    return MISSIONS

def main(self):
    nodes.chan_jobs.topics += (chan_missions(self))
    return start_missions(self) + base_missions(self) + main_story_missions(self) + autocrat_missions(self) + investigate_missions(self)
