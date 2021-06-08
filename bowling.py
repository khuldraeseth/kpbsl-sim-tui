import curses
from math import floor
from time import sleep
#sleep = lambda n: None

from archs import archs
from big_text import concat, embiggen
from bowling_engine import bowling_frame
from scoreboard2 import scoreboard
from pinout import pinout
from strike import strike

class Frame:
    def __init__(self, y, x):
        self.firstBowl = None
        self.secondBowl = None
        self.score = None

        self.winFirst = curses.newwin(7, 6, y, x)
        self.winSecond = curses.newwin(7, 6, y, x+8)
        self.winScore = curses.newwin(7, 12, y+8, x+1)

    def getBowls(self):
        return [bowl for bowl in [self.firstBowl, self.secondBowl] if bowl is not None]

    def setFirst(self, n):
        self.firstBowl = n
        self.winFirst.move(0, 0)
        if n == 0:
            self.winFirst.addstr(embiggen('-'))
        elif n == 10:
            self.winSecond.move(0, 0)
            self.winSecond.addstr(embiggen('X'))
        else:
            self.winFirst.addstr(embiggen(n))

    def setSecond(self, n):
        self.secondBowl = n
        self.winSecond.move(0, 0)
        if n == 0:
            self.winSecond.addstr(embiggen('-'))
        elif self.firstBowl + n == 10:
            self.winSecond.addstr(embiggen('/'))
        else:
            self.winSecond.addstr(embiggen(n))

    def setScore(self, n):
        self.score = n
        self.winScore.move(0, 0)
        self.winScore.addstr(embiggen(n))

    def updateScore(self, rest):
        if self.firstBowl is None:
            return

        if self.firstBowl == 10:
            if len(rest) < 2:
                return
            self.setScore(10 + rest[0] + rest[1])
            return

        if self.secondBowl is None:
            return

        if self.firstBowl + self.secondBowl == 10:
            if len(rest) < 1:
                return
            self.setScore(self.firstBowl + self.secondBowl + rest[0])
            return

        self.setScore(self.firstBowl + self.secondBowl)

    def refresh(self):
        self.winFirst.refresh()
        self.winSecond.refresh()
        self.winScore.refresh()

class FrameTen:
    def __init__(self, y, x):
        self.firstBowl = None
        self.secondBowl = None
        self.thirdBowl = None
        self.score = None

        self.winFirst = curses.newwin(7, 6, y, x)
        self.winSecond = curses.newwin(7, 6, y, x+8)
        self.winThird = curses.newwin(7, 6, y, x+16)
        self.winScore = curses.newwin(7, 12, y+8, x+5)

    def getBowls(self):
        return [bowl for bowl in [self.firstBowl, self.secondBowl, self.thirdBowl] if bowl is not None]

    def setFirst(self, n):
        self.firstBowl = n
        self.winFirst.move(0, 0)
        if n == 0:
            self.winFirst.addstr(embiggen('-'))
        elif n == 10:
            self.winFirst.addstr(embiggen('X'))
        else:
            self.winFirst.addstr(embiggen(n))

    def setSecond(self, n):
        self.secondBowl = n
        self.winSecond.move(0, 0)
        if n == 0:
            self.winSecond.addstr(embiggen('-'))
        elif n == 10 and self.firstBowl == 10:
            self.winSecond.addstr(embiggen('X'))
        elif self.firstBowl + n == 10:
            self.winSecond.addstr(embiggen('/'))
        else:
            self.winSecond.addstr(embiggen(n))

    def setThird(self, n):
        self.thirdBowl = n
        self.winThird.move(0, 0)
        if n == 0:
            self.winThird.addstr(embiggen('-'))
        elif n == 10 and self.secondBowl != 0:
            self.winThird.addstr(embiggen('X'))
        elif self.secondBowl + n == 10 and self.firstBowl + self.secondBowl != 10:
            self.winThird.addstr(embiggen('/'))
        else:
            self.winThird.addstr(embiggen(n))

    def setScore(self, n):
        self.score = n
        self.winScore.move(0, 0)
        self.winScore.addstr(embiggen(n))

    def updateScore(self):
        if self.firstBowl is None or self.secondBowl is None or (self.firstBowl + self.secondBowl >= 10 and self.thirdBowl is None):
            return

        self.setScore(sum(self.getBowls()))

    def refresh(self):
        self.winFirst.refresh()
        self.winSecond.refresh()
        self.winThird.refresh()
        self.winScore.refresh()

class BowlerScore:
    def __init__(self, y, name):
        self.background = curses.newwin(25, 180, y, 0)
        self.background.addstr(scoreboard)

        self.name = curses.newwin(7, 146, y+1, 22)
        self.name.addstr(embiggen(name))

        self.score = curses.newwin(7, 18, y+1, 2)

        self.frames19 = [Frame(y+9, 2 + 16*i) for i in range(9)]
        self.frame10 = FrameTen(y+9, 146)

        self.pins = curses.newwin(7, 8, y+1, 170)

    def updateFrames(self):
        for idx, frame in enumerate(self.frames19):
            rest = concat(frame.getBowls() for frame in self.frames19[idx+1:]) + self.frame10.getBowls()
            frame.updateScore(rest)
        self.frame10.updateScore()

    def updateScore(self):
        self.score.addstr(0, 0, embiggen(self.getScore()))

    def getScore(self):
        return sum([frame.score for frame in [*self.frames19, self.frame10] if frame.score is not None])

    def refresh(self):
        self.background.refresh()
        self.name.refresh()

        self.updateFrames()

        for frame in self.frames19:
            frame.refresh()

        self.frame10.refresh()
        self.updateScore()
        self.score.refresh()

class Bowler:
    def __init__(self, y, log, name, arch, mult=1):
        self.name = name
        self.log = log
        self.score = BowlerScore(y, name)
        self.attrs = [sum(archs[arch][:i]) for i in range(1,12)]
        self.mult = mult

        self.framesDone = 0

    def refresh(self):
        self.score.updateScore()
        self.score.refresh()
        self.log.refresh()

    def showPins(self, n):
        self.score.pins.move(0, 0)
        self.score.pins.erase()
        self.score.pins.addstr(pinout(n))
        self.score.pins.refresh()

    def wait(self):
        self.refresh()
        sleep(1)

    def bowlNotLastFrame(self):
        frame = bowling_frame(self.attrs)
        self.score.frames19[self.framesDone].setFirst(frame[0])
        self.showPins(frame[0])
        if frame == [10]:
            self.log.addstr(0, 0, f"{self.name} bowled a strike!")
            self.log.addstr(3, 0, strike)
            self.wait()
        else:
            if frame[0] == 0:
                self.log.addstr(0, 0, f"{self.name} rolled the ball right into the gutter")
                self.wait()
            else:
                self.log.addstr(0, 0, f"{self.name} knocked down {frame[0]} {'pin' if frame[0] == 1 else 'pins'}")
                self.wait()
            self.score.frames19[self.framesDone].setSecond(frame[1])
            if frame[1] == 0:
                self.log.addstr(1, 0, f"{self.name} rolled the ball right into the gutter")
                self.wait()
            elif sum(frame) == 10:
                self.log.addstr(1, 0, f"{self.name} knocked down another {frame[1]} {'pin' if frame[1] == 1 else 'pins'} for a spare!")
                self.wait()
            else:
                self.log.addstr(1, 0, f"{self.name} knocked down another {frame[1]} {'pin' if frame[1] == 1 else 'pins'}")
                self.wait()

        self.framesDone += 1

    def bowlLastFrame(self):
        frame = bowling_frame(self.attrs)
        self.score.frame10.setFirst(frame[0])
        self.showPins(frame[0])
        if frame == [10]:
            self.log.addstr(0, 0, f"{self.name} bowled a strike! TWO bonus bowls...")
            self.log.addstr(3, 0, strike)
            self.wait()
            bonus = bowling_frame(self.attrs)
            self.score.frame10.setSecond(bonus[0])
            if bonus == [10]:
                self.log.addstr(1, 0, f"{self.name} bowled another strike with the first bonus bowl! A chance to strike out...")
                self.wait()
                megaBonus = bowling_frame(self.attrs)
                self.score.frame10.setThird(megaBonus[0])
                self.showPins(megaBonus[0])
                if megaBonus == [10]:
                    self.log.addstr(2, 0, f"A three-strike tenth frame! {self.name} has struck out!")
                    self.wait()
                elif megaBonus[0] == 0:
                    self.log.addstr(2, 0, f"{self.name} rolled the second bonus ball right into the gutter.")
                    self.wait()
                else:
                    self.log.addstr(2, 0, f"{self.name} knocked down {megaBonus[0]} pins with the bonus bowl")
                    self.wait()
            else:
                self.showPins(bonus[0])
                if bonus[0] == 0:
                    self.log.addstr(1, 0, f"{self.name} rolled the first bonus ball right into the gutter")
                    self.wait()
                else:
                    self.log.addstr(1, 0, f"{self.name} knocked down {bonus[0]} pins with the first bonus bowl")
                    self.wait()
                self.score.frame10.setThird(bonus[1])
                if bonus[1] == 0:
                    self.log.addstr(2, 0, f"{self.name} rolled the second bonus ball right into the gutter")
                    self.wait()
                elif sum(bonus) == 10:
                    self.log.addstr(2, 0, f"{self.name} knocked down {bonus[1]} pins with the second bonus bowl for a spare!")
                    self.wait()
                else:
                    self.log.addstr(2, 0, f"{self.name} knocked down another {bonus[1]} pins with the second bonus bowl")
                    self.wait()
        else:
            if frame[0] == 0:
                self.log.addstr(0, 0, f"{self.name} rolled the ball right into the gutter")
                self.wait()
            else:
                self.log.addstr(0, 0, f"{self.name} knocked down {frame[0]} {'pin' if frame[0] == 1 else 'pins'}")
                self.wait()
            self.score.frame10.setSecond(frame[1])
            if frame[1] == 0:
                self.log.addstr(1, 0, f"{self.name} rolled the ball right into the gutter")
                self.wait()
            elif sum(frame) == 10:
                self.log.addstr(1, 0, f"{self.name} knocked down another {frame[1]} {'pin' if frame[1] == 1 else 'pins'} for a spare! Bonus bowl...")
                self.wait()
                bonus = bowling_frame(self.attrs)
                self.score.frame10.setThird(bonus[0])
                self.showPins(bonus[0])
                if bonus == [10]:
                    self.log.addstr(2, 0, f"{self.name} bowled a strike with the bonus bowl!")
                    self.wait()
                elif bonus[0] == 0:
                    self.log.addstr(2, 0, f"{self.name} rolled the bonus ball right into the gutter")
                    self.wait()
                else:
                    self.log.addstr(2, 0, f"{self.name} knocked down {bonus[0]} pins with the bonus bowl")
                    self.wait()
            else:
                self.log.addstr(1, 0, f"{self.name} knocked down another {frame[1]} {'pin' if frame[1] == 1 else 'pins'}")
                self.wait()
        self.framesDone += 1

    def bowlFrame(self):
        self.log.erase()
        self.showPins(0)
        self.wait()
        if self.framesDone == 9:
            self.bowlLastFrame()
        else:
            self.bowlNotLastFrame()
        self.refresh()

    def finalize(self):
        self.log.erase()
        self.log.addstr(0, 0, self.name)
        self.log.addstr(3, 0, embiggen(floor(self.score.getScore() * self.mult)))
        self.refresh()

    def bowlGame(self):
        for _ in range(10):
            self.bowlFrame()
            self.refresh()
