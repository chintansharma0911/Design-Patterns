from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum


class MatchStatus(Enum):
    SCHEDULED = "Scheduled"
    LIVE = "Live"
    COMPLETED = "Completed"


class PlayerRole(Enum):
    BATSMAN = "Batsman"
    BOWLER = "Bowler"
    ALL_ROUNDER = "AllRounder"
    WICKET_KEEPER = "WicketKeeper"


class CommentaryType(Enum):
    TEXT = "Text"
    HIGHLIGHT = "Highlight"
    ALERT = "Alert"


class Extras(Enum):
    NO_BALL = "NoBall"
    WIDE = "Wide"
    LEG_BYE = "LegBye"
    BYE = "Bye"
    NONE = "None"


class Dismissal(Enum):
    BOWLED = "Bowled"
    CAUGHT = "Caught"
    RUN_OUT = "RunOut"
    LBW = "LBW"
    STUMPED = "Stumped"
    NONE = "None"


class PlayerStats:
    def __init__(self, runs: int = 0, wickets: int = 0):
        self.runs = runs
        self.wickets = wickets


class Player:
    def __init__(self, name: str, role: PlayerRole):
        self.playerId: UUID = uuid4()
        self.name: str = name
        self.role: PlayerRole = role
        self.stats: PlayerStats = PlayerStats()


class Team:
    def __init__(self, name: str, players: List[Player]):
        self.teamId: UUID = uuid4()
        self.name: str = name
        self.players: List[Player] = players


class BallEvent:
    def __init__(self, over: int, ballInOver: int, batsman: Player, bowler: Player,
                 runs: int, extras: Extras = Extras.NONE,
                 dismissal: Optional[Dismissal] = Dismissal.NONE):
        self.ballId: UUID = uuid4()
        self.over: int = over
        self.ballInOver: int = ballInOver
        self.batsman: Player = batsman
        self.bowler: Player = bowler
        self.runs: int = runs
        self.extras: Extras = extras
        self.dismissal: Optional[Dismissal] = dismissal
        self.timestamp: datetime = datetime.now()


class Over:
    def __init__(self, overNumber: int):
        self.overNumber: int = overNumber
        self.balls: List[BallEvent] = []

    def add_ball(self, ball: BallEvent):
        self.balls.append(ball)


class Innings:
    def __init__(self, inningsNumber: int):
        self.inningsNumber: int = inningsNumber
        self.overs: List[Over] = []
        self.runs: int = 0
        self.wickets: int = 0

    def add_over(self, over: Over):
        self.overs.append(over)
        for ball in over.balls:
            self.runs += ball.runs
            if ball.dismissal and ball.dismissal != Dismissal.NONE:
                self.wickets += 1


class Commentary:
    def __init__(self, matchId: UUID, text: str, type: CommentaryType):
        self.commentaryId: UUID = uuid4()
        self.matchId: UUID = matchId
        self.text: str = text
        self.type: CommentaryType = type
        self.timestamp: datetime = datetime.now()


class Match:
    def __init__(self, homeTeam: Team, awayTeam: Team, startTime: datetime):
        self.matchId: UUID = uuid4()
        self.homeTeam: Team = homeTeam
        self.awayTeam: Team = awayTeam
        self.status: MatchStatus = MatchStatus.SCHEDULED
        self.startTime: datetime = startTime
        self.currentInnings: Optional[Innings] = None
        self.commentaries: List[Commentary] = []

    def start_match(self):
        self.status = MatchStatus.LIVE
        self.currentInnings = Innings(1)

    def add_commentary(self, text: str, type: CommentaryType):
        commentary = Commentary(self.matchId, text, type)
        self.commentaries.append(commentary)

    def getScoreboard(self):
        if not self.currentInnings:
            return "Match not started"
        return {
            "runs": self.currentInnings.runs,
            "wickets": self.currentInnings.wickets,
            "overs": len(self.currentInnings.overs)
        }


# Example usage
if __name__ == "__main__":
    # Create players
    player1 = Player("Virat Kohli", PlayerRole.BATSMAN)
    player2 = Player("Jasprit Bumrah", PlayerRole.BOWLER)

    # Create teams
    teamA = Team("India", [player1, player2])
    teamB = Team("Australia", [])

    # Create match
    match = Match(teamA, teamB, datetime.now())
    match.start_match()

    # Add over and ball events
    over1 = Over(1)
    ball1 = BallEvent(1, 1, player1, player2, 4)
    ball2 = BallEvent(1, 2, player1, player2, 0, dismissal=Dismissal.NONE)
    over1.add_ball(ball1)
    over1.add_ball(ball2)

    match.currentInnings.add_over(over1)

    # Add commentary
    match.add_commentary("Kohli hits a four!", CommentaryType.HIGHLIGHT)

    # Print scoreboard
    print(match.getScoreboard())
