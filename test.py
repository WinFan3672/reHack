"""
reHack Unit Tests
"""

count = 4 # Number of unit tests

print("(1/{}) Importing Game Code".format(count))
import rehack
import data

game = rehack.game

print("(2/{}) Initialising Game...".format(count))
player = rehack.game.player.PlayerNode("gordinator", "root")

print("(3/{}) Testing mission start function...".format(count))
for mission in player.MISSIONS:
    print("-> {}".format(mission.mission_id))
    print("  -> start()")
    mission.start()
    print("  -> check_end()")
    mission.check_end()
    print("  -> end()")
    mission.end()
print("(4/{}) Testing programs...".format(count))
for command in ["help"]:
    print("-> {}".format(command))
    player.run_command(command)

print("[info] Passed all tests")
