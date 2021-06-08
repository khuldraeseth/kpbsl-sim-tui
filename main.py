#!/usr/bin/env python3

import curses
from curses import wrapper
from time import sleep
import re

from bowling import Bowler

class ProtoBowler:
    def __init__(self):
        self.name = input("What is the bowler's name? ")
        self.arch = input("What is the bowler's archetype? ").lower().replace(' ', '-')
        self.juiced = re.match("[Yy](?:e[as])?", input("Is the bowler using an odds changer powerup (y/N)? ")) is not None
        self.mult = 1
        if re.match("[Yy](?:e[as])?", input("Is the bowler using a multiplier powerup (y/N)? ")) is not None:
            self.mult = float(input("What multiplier is to be applied? "))
        print()

    def mkBowler(self, y, win):
        return Bowler(y, win, self.name, self.arch + ("-reduced" if self.juiced else ""), self.mult)

def mkBowler(y, win):
    name = input("What is the bowler's name? ")
    arch = input("What is the bowler's archetype? ").lower().replace(' ', '-')
    juiced = re.match("[Yy](?:e[as])?", input("Is the bowler using an odds changer powerup (y/N)? ")) is not None
    mult = 1
    if re.match("[Yy](?:e[as])?", input("Is the bowler using a multiplier powerup (y/N)? ")) is not None:
        mult = float(input("What multiplier is to be applied? "))
    
    return Bowler(y, win, name, arch + "-reduced" if juiced else "", mult)

def runBowling(stdscr, p1, p2):

    b1 = p1.mkBowler(0, curses.newwin(12, 80, 25, 0))
    b2 = p2.mkBowler(37, curses.newwin(12, 80, 25, 90))

    curses.noecho()
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    b1.refresh()
    b2.refresh()

    for _ in range(10):
        b1.bowlFrame()
        b2.bowlFrame()

    sleep(2)

    b1.finalize()
    b2.finalize()

    stdscr.getkey()

def main():
    p1 = ProtoBowler()
    p2 = ProtoBowler()
    input("Make sure you've entered correct information, then press Enter to continue!")
    wrapper(runBowling, p1, p2)

if __name__ == "__main__":
    main()
