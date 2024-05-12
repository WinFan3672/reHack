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

dcsebets_welcome = dcsebets.add_topic("u/dcse_killer", "Welcome to n/dcsebets!", """DCSE Bets is a subnerd dedicated to getting rich through the DC Stock Exchangce (DCSE), through the use of high-risk and non-confirmist strategies.""")

dcsebets_tutorial = dcsebets.add_topic("u/dcse_killer", "How To Trade On DCSE", """1. Connect to trade.dcse.com
2. Create an account
3. Purchase some shares
4. Profit""")

future_plans = meta.add_topic("u/admin", "Plans For The Future", """1. A new Ranking system

The idea is to let users Up-Rank or Down-Rank a post or reply to that post if they think it's good or bad.
That way, content is sorted based on rank. Bad posts would get pushed away, and good posts boosted in a way that is moderated entirely by users.

2. A new profile system.

Each user has a profile with a certain amount of rankpoints. Every time someone up-ranks your post, you get +0.25, and you lose that much per down-rank. Replying to a post or posting gives you +0.125.

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
    Plus+ users are able to moderate any subnerd. The settings for the subnerd will be able to block specific users or disable all Plus+ moderation entirely.

4. Awards

Standard+ and higher users get daily free Awards to give out. You cannot give yourself awards, and the amount of free awards you have per day resets, and does not stack. Some awards are purchaseable, and are more powerful.

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

future_plans.reply("u/nerd", "The Plus+ thing concerns me. I think this will introduce a culture of power-hungry moderators who 'get off', so to speak, off their own abilities to silence criticism.")
future_plans.reply("u/admin", "you may have a point")
future_plans.reply("u/mht", "What will we think when we look back at this very early post in ten years' time?")
future_plans.reply("u/admin", "I don't think nerdnet will survive that long :)")
future_plans.reply("u/mht", "I beg to differ - nerds will LOVE it, and they will flock to it")
future_plans.reply("u/admin", "I imagine the network effect will help as well")
future_plans.reply("u/mht", "Ah, the network effect is a but double-edged sword, remember what happened to OurSpaces?")
future_plans.reply("u/bit", "My grandmother was so displeased when it shut down, she phoned me about it and everything")
future_plans.reply("u/gold", "A genuine idea: awards should have a pay-it-forward deal, where if someone gives you an award, you can then award it to someone else")
future_plans.reply("u/admin", "I'll only do that for the free ones, but it's a great idea")
future_plans.reply("u/admin", "It'll have to be a temporary thing - after 24h, the award goes poof")
future_plans.reply("u/rehack", "Perhaps some of our agents may be able to assist you with building server software?")
future_plans.reply("u/admin", "I don't trust hackers, least of all black-hats like you lot")
future_plans.reply("u/rehack", "I imagine you read all the ColonSlash propaganda?")
future_plans.reply("u/admin", "As a matter of fact, I did")
future_plans.reply("u/rehack", "And you never saw the notice at the bottom saying it was AI-generated?")
future_plans.reply("u/rehack", "Nonesense! It's 2010, AI can barely identify plant pots in images!")
future_plans.reply("u/admin", "Funny you mention that, actually, I installed the SearchOS Item Identify software earlier today, it's quite cool")
future_plans.reply("u/someone", "I wonder how far Artificial Intelligence and Machine Learning will come in ten years? fifteen? twenty?")
future_plans.reply("u/admin", "I doubt it'd be able to play Chess any better than it already does")
future_plans.reply("u/neckbeards_alliance", "genine question: are the award prices final? Silver looks like bad value compared to Gold")
future_plans.reply("u/admin", "they might change in the final impementation, and inflation will likely push it up over time :)")
future_plans.reply("u/admin", "and of course silver is bad value, it's a funnel towards paying $1 more for gold")
future_plans.reply("u/dcse_killer", "do you plan on going public any time (haha)")
future_plans.reply("u/admin", "speaking genuinely, n/dcsebets will be locked down temporarily during that period")
future_plans.reply("u/dcse_killer", "people in The Community will know what to do when the time comes")
future_plans.reply("u/admin", "well, a short squeeze sounds good to me")
future_plans.reply("u/dcse_killer", "wait until the crash, that will be fun")
future_plans.reply("u/rehack", "you still believe the ColonSlash garbage, u/admin?")
future_plans.reply("u/admin", "i need some more conclusive evidence than *that*")
future_plans.reply("u/rehack", "the ONLY thing ColonSlash has posted is that expose")
future_plans.reply("u/admin", "nothing before, nothing since?")
future_plans.reply("u/rehack", "uh-huh")
future_plans.reply("u/admin", "that *is* suspicious")

web_server = programming.add_topic("u/neckbeards_alliance", "Apache or WebEngine?", """Which one is best? I need to know.""")
web_server.reply("u/horseman", "WebEngine is way lighter and just as powerful, plus it has a better license")
web_server.reply("u/neckbeards_alliance", "Do NOT open up the Apache License VS BSD 'debate' can of worms, you'll just piss off a bunch of nerds")
web_server.reply("u/strange_fluid", "I hear WebEngine is gonna make a proprietary version of their software soon")
web_server.reply("u/admin", "yeah well they can't do anything to the original, if they take THAT proprietary instead of spinning it off, someone'll fork it")
web_server.reply("u/neckbeards_alliance", "someone will fork it --> someone else will do it anyway, why should I fork it? --> No-one will fork it")

tor_node = meta.add_topic("u/admin", "We have a Tor mirror!", "The folks over at Tor project handed us access to nerd-net.onion, so we have a mirror! It SHOULD work perfectly.")
tor_node.reply("u/bit", "cool, but it doesn't support logins, so what's the point?")
tor_node.reply("u/admin", "for browsing anonymously. when you post however, you are de-anoymised by nature, so you might as well give us your IP")
tor_node.reply("u/neckbeards_alliance", "it's a conspiracy theory to discourage usage of the Tor node, funneling ppl towards the clearnet version")
tor_node.reply("u/admin", "FINE! logins and signups have been enabled for the tor versions")

def main():
    return [nerdnet]

def tor():
    return []
