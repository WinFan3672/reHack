from resource.classes import *
from game import programs
import game.programs.connect
import resource.information as resourceInfo
from resource.libs import *
import random
import json
import copy
import string
import data

nerdnet = programs.Forum("NerdNet: Being Right > Money (Est. 2010)", "nerdnet", "nerd.net")
nerdnet.boards = [] ## Delete "General Discussion"

meta = nerdnet.add_board("n/nerdnet")
finance = nerdnet.add_board("n/finance")
funny = nerdnet.add_board("n/funny")
relationships = nerdnet.add_board("n/relationshipadvice")
programming = nerdnet.add_board("n/programming")
hacking = nerdnet.add_board("n/hacking")
tech = nerdnet.add_board("n/technology")

subnerds = meta.add_board("n/nerdnet/subnerd_requests")
reports = meta.add_board("n/nerdnet/reports")

dcsebets = nerdnet.add_board("n/dcsebets")

rehack = hacking.add_topic("u/rehack", "[AD] Want To Learn Pentesting At a Professional Level? Join reHack!", """If you're reading this, you PROBABLY want to do hacking.
Well, unfortunately, most people seem to think that all hacking is illegal. They are wrong. While hacking can be very, very illegal, there are branches of it that are not.
reHack speciailises in one branch: penetration testing. You get hired by a company and you let loose whatever you can onto their systems, and tell them what vulnerabilities you found,
what data you could access, how much control you had over their network, etc. reHack is a company specialising in recruiting agents. Companies needing agents pay us money, 
and we find them agents (that's you!) to do the work. Once the company is happy, the agent is paid and the company goes about its merry way.

When you join, we offer:
* Free work;
* Resources and tools to learn the necessary skills;
* Extensive tutorial contracts to learn new skills;
* A thriving community of enthusiastic hackers;
* Generous pay (we tax companies 20%, which they take into account when making listings).

If this interests you, go to rehack.org and sign up today. It's free*!
*Agents will need to pass an examination, which we do offer (paid) training for if you fail.
""")

req_memes = subnerds.add_topic("u/drytron", "REQUEST: n/memes", """I think n/memes would be a very popular subnerd, and would provide a one-of-a-kind centralised place to store memes.""")
req_memes.reply("u/admin", "Don't think so. Storage/bandwidth costs would be sky-high, and we don't make any money yet.")

isp = tech.add_topic("u/facetious", "Super Scummy ISPs", """Have any of you visited the WarpMedia website?
Recently, they vowed to provide one price for all homes in the UK for their broadband, leading to INSANE prices like £500/Mo for 10gbps broadband.
What the Hell? Is ANY of this good 'value'?""")
isp.reply("u/admin", "looks like you get ripped of no matter how little or how much you pay for")

dcsebets_welcome = dcsebets.add_topic("u/dcse_killer", "Welcome to n/dcsebets!", """DCSE Bets is a subnerd dedicated to getting rich through the DC Stock Exchangce (DCSE), through the use of high-rick and non-confirmist strategies.""")

future_plans = meta.add_topic("u/admin", "Plans For The Future", """1. A new Ranking system

The idea is to let users Up-Rank or Down-Rank a post or reply to that post if they think it's good or bad.
That way, content is sorted based on rank. Bad posts would get pushed away, and good posts boosted in a way that is moderated entirely by users.

2. A new profile system.

Each user has a profile with a certain amount of rankpoints. Every time someone up-ranks your post, you get +0.25, or +0.125 for a reply, and you lose that much per down-rank.

3. Profile tiers (WIP)

* <= 0 Rank: Unverified User
    This is where everyone starts out.
* >= 1 Rank: Standard User
    Once a user is verified by gaining one Rank, they can make posts.
* >= 1000 Rank: Standard+ User
    Each Standard+ user can hand out one "Award" a day, which gives a variable amount of Rank to another user.
* >= 5000 Rank: Plus User
    These users have a [+] next to their u/name, which stands out from other users. They can also give 5 awards per day.
* >= 10000 Rank: Plus+ User
    ???

4. Awards

Standard+ and higher users get daily free Awards to give out. You cannot give yourself awards, and the amount of free awards you have per day resets, and does not stack.
You can also buy ranks if you don't have any.

* 'Good': +10 Rank ($0.99)
* 'Bad': -10 Rank ($0.99)
* 'Gold': +50 Rank ($4.99)
* 'Silver': +25 Rank ($3.99)
* 'Funny': +1 Rank (FREE)
* 'Wholesome': +1 Rank (FREE)
* 'Interesting': +1 Rank (FREE)
* 'Thought-Provoking': +1 Rank (FREE)

Awards are given to Posts or Replies. Each user's profile page shows how many awards they have received, as well as a RankPoints breakdown showing where a user's RP comes from.

5. Custom Client and Sverer

To make all of this possible, NerdNet will need a custom server and client, instead of the Forum software we currently use. The current software we use has a LOT of plugins (some custom), and currently it is too limiting for what we are trying to achieve.

More news coming soon.""")

def main():
    return [nerdnet]

def tor():
    return []
