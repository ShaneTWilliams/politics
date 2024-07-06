import enum
import typing
import datetime
import abc

HASH_MODULUS = 1000000000

class ElectionType(enum.Enum):
    GENERAL = 1
    BYELECTION = 2

class ElectionResult(enum.Enum):
    ELECTED = 1
    ACCLAIMED = 2
    DEFEATED = 3
    ELECTED_COURT_DECISION = 4

    @staticmethod
    def from_string(s: str):
        return {
            "Elected": ElectionResult.ELECTED,
            "Elected (Acclamation)": ElectionResult.ACCLAIMED,
            "Defeated": ElectionResult.DEFEATED,
            "Elected (Court decision)": ElectionResult.ELECTED_COURT_DECISION
        }[s]

class Gender(enum.Enum):
    FEMALE = 1
    MALE = 2
    OTHER = 3
    UNKNOWN = 4

class Province(enum.Enum):
    AB = 1
    BC = 2
    MB = 3
    NB = 4
    NL = 5
    NS = 6
    NT = 7
    NU = 8
    ON = 9
    PE = 10
    QC = 11
    SK = 12
    YT = 13

    @staticmethod
    def from_name(name: str):
        return {
            "Alberta": Province.AB,
            "British Columbia": Province.BC,
            "Manitoba": Province.MB,
            "New Brunswick": Province.NB,
            "Newfoundland and Labrador": Province.NL,
            "Nova Scotia": Province.NS,
            "Northwest Territories": Province.NT,
            "Nunavut": Province.NU,
            "Ontario": Province.ON,
            "Prince Edward Island": Province.PE,
            "Quebec": Province.QC,
            "Saskatchewan": Province.SK,
            "Yukon": Province.YT
        }[name]

class Color(enum.Enum):
    RED = 1
    ORANGE = 2
    YELLOW = 3
    GREEN = 4
    BLUE = 5
    PURPLE = 6
    GREY = 7
    BLACK = 8
    WHITE = 9
    BROWN = 10
    PINK = 11


class Record(abc.ABC):
    @abc.abstractmethod
    def id(self) -> str:
        pass

    def __hash__(self):
        return hash(self.id())

    def to_json(self):
        ret = {}
        for k, v in vars(self).items():
            if isinstance(v, enum.Enum):
                ret[k] = v.name
            elif isinstance(v, Record):
                ret[k] = v.id()
            elif isinstance(v, datetime.date):
                ret[k] = {
                    "year": v.year,
                    "month": v.month,
                    "day": v.day
                }
            else:
                ret[k] = v

        return ret


class Party(Record):
    def __init__(self, name: str, color: str):
        self.name = name
        self.color = color

    def id(self):
        return str(hash(self.name) % HASH_MODULUS)


class Parliament(Record):
    def __init__(self, number: int):
        self.number = number

    def id(self):
        return str(self.number)


class Riding(Record):
    def __init__(
        self,
        name: str,
        province: Province,
        geometry: str,
        start_date: datetime.date,
        end_date: datetime.date
    ):
        self.name = name
        self.province = province
        self.geometry = geometry
        self.start_date = start_date
        self.end_date = end_date

    def id(self):
        # Riding geometry changes over time.
        return str((hash(self.geometry) + hash(self.name)) % HASH_MODULUS)


class Election(Record):
    def __init__(
        self,
        date: datetime.date,
        type: ElectionType,
        parliament: Parliament,
    ):
        self.date = date
        self.type = type
        self.parliament = parliament
        self.runs = []

    def id(self):
        return str(hash(self.date) % HASH_MODULUS)


class Candidate(Record):
    def __init__(
        self,
        first_name: str,
        last_name: str,
        gender: Gender,
        occupation: str
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.occupation = occupation

    def id(self):
        return str(hash(self.first_name + self.last_name) % HASH_MODULUS)


class Run(Record):
    def __init__(
        self,
        election: Election,
        riding: Riding,
        candidate: Candidate,
        party: Party,
        result: ElectionResult,
        votes: int,
    ):
        self.election = election
        self.riding = riding
        self.candidate = candidate
        self.party = party
        self.result = result
        self.votes = votes

    def id(self):
        return str((hash(self.election) + hash(self.riding) + hash(self.candidate)) % HASH_MODULUS)
