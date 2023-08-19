from resource.classes import *
import resource.information as resourceInfo
from resource.libs import *
from game.player import *
import data
from game.programs import Mission, ConnectMission, NMapMission, BuyMission

def main_story_missions(self):
    bodies = [
        [
            "Welcome to an Advanced Tutorial.",
            "This series covers more advanced topics not covered in the initial tutorial.",
            "This tutorial covers the 'scan' command.",
            "In standard nodes (you can check a node's type using 'nodecheck'), there are several commands built in.",
            "One of them is 'scan'. It lists all nodes linked to a node.",
            "This is extremely useful as it allows you to search through more of a network that is normally hidden.",
            "To demonstrate, connect to coca.com and hack in.",
            "Once you've done that, connect to it and run the scan command and find the mainframe password.",
            "Using the mainframe password, log in using the login command."
            "",
            "They should have the following:",
            "* A mail server",
            "   * This is really easy to break into and should have a lot of useful info.",
            "* A mainframe",
            "   * This needs a password.",
            "* A few employee nodes.",
            "   * Hack in and run 'ls'. You never know if they left some text notes.",
            "",
            "Once you're done, run 'mission' on your node and continue the Advanced Tutorials.",
        ],
        ]
    bodies = ["\n".join(x) for x in bodies]
    end_email = Email("contracts@rehack.org","{}@jmail.com".format(self.name),"Contract Complete","Congratulations. The contract is complete.\nGet more at contracts.rehack.org")
    emails = [
        Email("contracts@rehack.org","{}@jmail.com".format(self.name),"Advanced Tutorial #1",bodies[0]),
        ]
    return [
        Mission(self,"advanced1","Advanced Tutorial #1",None,emails[0],reward=750)
        ]
def start_missions(self):
    bodies = [
            [
            "Welcome to reHack!",
            "",
            "As you're new here, you'll want to check out our intranet (intranet.rehack.org).",
            "You can do this using the 'connect' command.",
            "Our intranet contains some useful resources as well as some info for beginners such as yourself.",
            "We look forward to seeing you succeed."
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
                "To register, purchase the AnonMail client using the 'store' command, free for a limited time.",
            ],
            [
                "Hello, fellow hacker.",
                "",
                "I would like to personally invite you to join our forum, 5chan.",
                "In case you don't know, reHack and 5chan have a, let's just say, toxic relationship.",
                "That is to say, reHack'ers target anons on 5chan all the time.",
                "However, I feel that you might be different.",
                "Because our website URL changes all the time, you'll need to check it out in the",
                "WorldWide Web Directory: w3d.org.",
                "",
                "I hope to see you on 5chan, fellow anon.",
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
                "Before you do that, the admin password is potholes. Use the login command to take advantage of that.",
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
            [
                "The email you provided was sent to null@null.null.",
                "This is usually because you are replying to an email which had its FROM address spoofed.",
                "For security purposes, your email has been sent back to you:",
                "FROM: {}",
                "TO: null@null.null",
                "SUBJECT: {}",
                "",
                "{}",
            ],
        ]
    bodies = ["\n".join(x) for x in bodies]
    emails = [
        Email("welcome@rehack.mail","{}@jmail.com".format(self.name),"Welcome to reHack",bodies[0]),
        # Email("marketing@anon.mail",f"{self.name}@jmail.com","AD: Try AnonMail",bodies[1]),
        # Email("null@null",f"{self.name}@jmail.com","A Personal Invitation",bodies[2])
        Email("xwebdesign@jmail.com","sales@root.mail.com","Client: XWebDesign",bodies[3]),
        Email("sales@root.mail.com","sales@xwebdesign.mail.com","Invoice",bodies[4].format("XWebDesign")),
        Email("sales@root.mail.com","sales@jmail.mail.com","Invoice",bodies[4].format("JMail")),
        Email("null@null.null","admin@winfan3672.mail.com","A Message",bodies[6]),
        Email("null@null.null","null@null.null","Notice",bodies[7]),
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
            "Once you're done, run 'mission' and read my next email."
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
            "Hack into the following IP: test.hub"
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
        Email("contracts@rehack.org",f"{self.name}@jmail.com","Tutorial Mission Pt. 1",mission_bodies[0]),
        Email("contracts@rehack.org",f"{self.name}@jmail.com","Tutorial Mission Pt. 2",mission_bodies[1]),
        Email("contracts@rehack.org",f"{self.name}@jmail.com","Tutorial Mission Pt. 3",mission_bodies[2]),
        Email("contracts@rehack.org",f"{self.name}@jmail.com","Tutorial Mission Pt. 4",mission_bodies[3].format(data.getNode("test2").address)),
        Email("contracts@rehack.org",f"{self.name}@jmail.com","Tutorial Mission Pt. 5",mission_bodies[4]),
        Email("contracts@rehack.org",f"{self.name}@jmail.com","Tutorial Mission Pt. 6",mission_bodies[5]),
        Email("contracts@rehack.org",f"{self.name}@jmail.com","Tutorial Mission Pt. 7",mission_bodies[6]),
        Email("contracts@rehack.org",f"{self.name}@jmail.com","You Finished The Tutorial",mission_bodies[7]),
        ]
    for item in emails:
        sendEmail(item)
    return [
        ConnectMission(self, "start1","Start (Pt. 1)","test.rehack.org",missionEmails[0],reward=500,next_id = "start2"),
        NMapMission(self, "start2","Start (Pt. 2)","test.rehack.org",missionEmails[1],reward=500,next_id="start3"),
        Mission(self, "start3","Start (Pt. 3)","test.rehack.org",missionEmails[2],reward=500,next_id="start4"),
        Mission(self, "start4","Start (Pt. 4)","test2",missionEmails[3],reward=500,next_id="start5"),
        Mission(self, "start5","Start (Pt. 5)","colonsla.sh",missionEmails[4],reward=500,next_id="start6"),
        BuyMission(self, "start6","Start (Pt. 6)",["webworm","mxlookup"],missionEmails[5],reward=500,next_id = "start7"),
        Mission(self, "start7","Start (Pt. 7)","test.hub",missionEmails[6],reward=2500, end_email = missionEmails[7]),
        ]