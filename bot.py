def bot(f, j):
    return bot_(f, j)

import random
from enum import Enum
from itertools import *;

# This bot tries to cooperate in a fair manner by alternating between claiming 3 and 4 while setting
# the veto to a non interfering value.
# When playing other bots it establishes cooperation by randomly claiming 3 or 4 until both players
# pick differently. At this point it continues to cooperate until the other player defects.
# When playing itself it encodes information into the veto which allows faster cooperating in self
# play and recognition of copies.

class State(Enum):
    FirstRound = 1
    EstablishingCooperation = 2
    Cooperating = 3
    FailedCooperation = 4
    LastRound = 5

def bot_(f, j):
    state = determine_state(f, j)

    if state == State.FirstRound:
        return 3, random_safe_veto(random)

    if state == State.EstablishingCooperation:
        return establish_cooperation(f, j), random_safe_veto(random)

    if state == State.Cooperating:
        claim, veto = cooperate(f, j)
        # Cheeky optimization for the 1 in 32 chance that we know this the last round and we are not
        # playing a copy. In this case we can veto their expected guess with impunity. This is good
        # late in the game assuming mostly cooperators remain but could be bad early because we are
        # reducing the copies of a bot that we can cooperate with.
        if last_round_of_cooperation_with_stranger(f, j):
            veto = f[-1][0]
        return claim, veto

    if state == State.FailedCooperation:
        # We could do something smarter here like exploiting simple bots that always claim a fixed
        # value. Or give defecting bots a chance to go back to cooperation if they make it up to us
        # in points first. I didn't have enough time to work on this and thought it was boring to
        # to write code specifically for the example bots that I thought no human player would ever
        # submit.
        return 4, 0

def determine_state(f, j):
    if len(f) == 0:
        return State.FirstRound

    if any(j[0] > 4 for j in j):
        return State.FailedCooperation

    if any(j0[0] == 4 and j1[0] == 4 for j0, j1 in pairwise(j)):
        return State.FailedCooperation

    if any(f[0] == j[1] for f, j in zip(f, j)):
        return State.FailedCooperation

    if all(f[0] == j[0] for f, j in zip(f, j)):
        return State.EstablishingCooperation

    return State.Cooperating

def random_safe_veto(random_):
    return random_.choice([0, 1, 2, 5, 6, 7])

# We want to cooperate as quickly as possible. Without optimizing for self play we would randomly
# pick from [3, 4] until both players pick differently and tit for tat from there.
# In the special case of self play we can converge faster by encoding extra information into the
# veto. A safe veto is one that does not lose the other player points so we randomly pick without
# [3, 4]. A simple algorithm could check whose veto is higher and let that player claim 4 next
# round. This has the problem that it could be abused for a slight point gain or that it might
# accidentally run into a feedback loop in non self play where the other player uses the opposite
# condition (in this example lower veto claims 4) which would lead to every round alternating
# between both players claiming 3 and 4 and not gaining points in the latter.
# We solve this by using an algorithm that appears random to any other bot but is deterministic for
# copies of this bot. Even if another author had the same idea we would not run into the feedback
# loop.
# For a better average self play claim we start with claim 3 and continue to claim 3 until the veto
# is able to decide which copy should claim 4 first. This could be abusable by a bot that
# deterministically claims 4 on the first round.
def establish_cooperation(f, j):
    if f[-1][1] == j[-1][1]:
        return 3
    random_ = random_state(f, j)
    choice = random_.choice([0, 7])
    return 4 if abs(choice - f[-1][1]) < abs(choice - j[-1][1]) else 3

def cooperate(f, j):
    claim = 3 if f[-1][0] == 4 else 4
    veto = random_safe_veto(random_state(f, j))
    return claim, veto

def random_state(f, j):
    # This number has been randomly chose. Xoring the previous guesses together ensures that when
    # playing itself both copies use the same random state while still being random per round as we
    # know that at least our previous veto is true random. Including the length prevents the vetos
    # getting stuck in a cycle.
    return random.Random(1421832459 ^ f[-1][1] ^ j[-1][1] ^ len(f))

def last_round_of_cooperation_with_stranger(f, j):
    if len(f) == 128 + 15:
        return not playing_copy(f, j)

def playing_copy(f, j):
    if j[0][0] != 3:
        return False
    
    for i in range(1, len(f)):
        state = determine_state(f[:i-1], j[:i-1])
        if state == State.Cooperating and f[i][1] != j[i][1]:
            return False
    return True

def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

# Tests

def badbot(f, j):
    return 3, 0

def selfishbot(f, j):
    return 7, 0

def titfortatbot(f, j):
    if len(f) == 0:
        return (3, 0)
    return j[-1]

def test_play(a, b):
    aa = []
    bb = []
    for _ in range(128+16):
        aaa = a(aa, bb)
        bbb = b(bb, aa)
        aa.append(aaa)
        bb.append(bbb)
        print(aa[-1], bb[-1])

if __name__ == "__main__":
    assert determine_state([(3, 0)], [(3, 0)]) == State.EstablishingCooperation
    assert determine_state([(4, 0)], [(4, 0)]) == State.EstablishingCooperation
    assert determine_state([(3, 0), (4, 0)], [(3, 0), (4, 0)]) == State.EstablishingCooperation
    assert determine_state([(3, 0), (4, 0), (3, 0)], [(3, 0), (3, 0), (4, 0)]) == State.Cooperating
    assert determine_state([(3, 0)], [(5, 0)]) == State.FailedCooperation
    assert determine_state([(3, 0)], [(3, 3)]) == State.FailedCooperation

    # test_play(bot, bot)
    # test_play(bot, badbot)
    # test_play(bot, selfishbot)
    # test_play(bot, titfortatbot)

    # smoke test exceptions
    def r():
        return random.randint(0, 7)

    for _ in range(100):
        f = []
        j = []
        for _ in range(10):
            f.append((r(), r()))
            j.append((r(), r()))
            claim, veto = bot(f, j)
            assert 0 <= claim and claim <= 7
            assert 0 <= veto and veto <= 7
