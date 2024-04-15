from dataclasses import dataclass


@dataclass
class Player:
    Name: str
    Wins: int
    Losses: int
    Ties: int
