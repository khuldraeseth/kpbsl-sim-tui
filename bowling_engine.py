import random
import sys
from bisect import bisect

gamemultiplier = 1

def bowling_frame(stats):
    firstBowl = bisect(stats, random.random())
    if firstBowl == 10:
        return [10]

    secondBowl = bisect(stats, random.random() * stats[10 - firstBowl])
    return [firstBowl, secondBowl]

def bonus(frames, extra):
    score = 0

    for i in range(len(frames)):
        if frames[i] == [10]:
            score += sum(concat(frames[i+1:] + extra)[:2])
        elif sum(frames[i]) == 10:
            #score += (frames + extra)[i+1][0]
            score += sum(concat(frames[i+1:] + extra)[:1])
    
    return score

def score_game(frames, extra):
    return sum([sum(frame) for frame in frames]) + bonus(frames, extra)

def old_score_frame(bowls):
    if sum(bowls) == 10:
        return 10 + bowls[-1]
    return sum(bowls)

def old_bowl_game(arch):
    stats = [sum(archs[arch][:i]) for i in range(1,12)]
    return sum([old_score_frame(bowling_frame(stats)) for _ in range(10)])

def bowl_game(arch):
    stats = [sum(archs[arch][:i]) for i in range(1,12)]
    frames = [bowling_frame(stats) for _ in range(10)]
    extra = [bowling_frame(stats), bowling_frame(stats)]    # Just in case
    return score_game(frames, extra)
