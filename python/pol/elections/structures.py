import abc
import base64
import datetime
import enum
import hashlib
import typing
import xml

from shapely.geometry import Polygon


def hash_string(s: str):
    hash_bytes = hashlib.sha1(s.encode()).digest()
    return base64.urlsafe_b64encode(hash_bytes).decode()[:10]


class ElectionType(enum.Enum):
    GENERAL = 1
    BYELECTION = 2

    @staticmethod
    def from_string(s: str):
        return {
            "By-Election": ElectionType.BYELECTION,
            "General": ElectionType.GENERAL,
        }[s]


class ParliamentarianType(enum.Enum):
    MP = 1
    SENATOR = 2

    @staticmethod
    def from_string(s: str):
        return {
            "MP": ParliamentarianType.MP,
            "Senator": ParliamentarianType.SENATOR,
        }[s]


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
            "Elected (Court decision)": ElectionResult.ELECTED_COURT_DECISION,
        }[s]


class Gender(enum.Enum):
    FEMALE = 1
    MALE = 2
    OTHER = 3
    UNKNOWN = 4

    @staticmethod
    def from_string(s: str):
        return {
            "Man": Gender.MALE,
            "Woman": Gender.FEMALE,
            "Another Gender": Gender.OTHER,
            "Data unavailable": Gender.UNKNOWN,
        }[s]


class DetailViewName(enum.Enum):
    # REFERENCE: https://upload.wikimedia.org/wikipedia/commons/f/f8/Canada_Election_2021_Results_Map.svg
    ST_JOHNS = enum.auto()
    PEI = enum.auto()
    MONCTON = enum.auto()
    HALIFAX = enum.auto()
    MONTREAL = enum.auto()
    QUEBEC_CITY = enum.auto()
    SOUTHERN_QUEBEC = enum.auto()
    TROIS_RIVIERES = enum.auto()
    OTTAWA = enum.auto()
    TORONTO = enum.auto()
    GOLDEN_HORSESHOE = enum.auto()
    LONDON = enum.auto()
    REGINA = enum.auto()
    WINNIPEG = enum.auto()
    ESSEX = enum.auto()
    SASKATOON = enum.auto()
    CALGARY = enum.auto()
    EDMONTON = enum.auto()
    VANCOUVER = enum.auto()
    VICTORIA = enum.auto()


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
            "Yukon": Province.YT,
        }[name]


class PartyName(enum.Enum):
    ABOLITIONIST_PARTY_OF_CANADA = enum.auto()
    ACCOUNTABILITY_COMPETENCY_AND_TRANSPARENCY = enum.auto()
    ALL_CANADIAN_PARTY = enum.auto()
    ALLIANCE_OF_THE_NORTH = enum.auto()
    ANIMAL_ALLIANCE_ENVIRONMENT_VOTERS_PARTY_OF_CANADA = enum.auto()
    ANIMAL_PROTECTION_PARTY_OF_CANADA = enum.auto()
    ANTI_CONFEDERATE = enum.auto()
    ANTI_CONSCRIPTIONIST = enum.auto()
    AUTONOMIST = enum.auto()
    BLOC_QUÉBÉCOIS = enum.auto()
    BLOC_POPULAIRE_CANADIEN = enum.auto()
    CANADA_PARTY = enum.auto()
    CANADAS_FOURTH_FRONT = enum.auto()
    CANADIAN_ACTION_PARTY = enum.auto()
    CANADIAN_DEMOCRAT = enum.auto()
    CANADIAN_FUTURE_PARTY = enum.auto()
    CANADIAN_LABOUR = enum.auto()
    CANADIAN_NATIONALIST_PARTY = enum.auto()
    CANADIAN_PARTY = enum.auto()
    CANADIAN_REFORM_CONSERVATIVE_ALLIANCE = enum.auto()
    CANDIDATE_OF_THE_ELECTORS = enum.auto()
    CAPITAL_FAMILIAL = enum.auto()
    CENTRIST_PARTY_OF_CANADA = enum.auto()
    CHRISTIAN_HERITAGE_PARTY_OF_CANADA = enum.auto()
    CHRISTIAN_LIBERAL = enum.auto()
    COOPERATIVE_COMMONWEALTH_FEDERATION = enum.auto()
    COMMUNIST_PARTY_OF_CANADA = enum.auto()
    CONFEDERATION_OF_REGIONS_WESTERN_PARTY = enum.auto()
    CONSERVATIVE_1867_1942 = enum.auto()
    CONSERVATIVE_PARTY_OF_CANADA = enum.auto()
    CONSERVATIVE_LABOUR = enum.auto()
    COOPERATIVE_BUILDERS_OF_CANADA = enum.auto()
    DEMOCRAT = enum.auto()
    DROIT_VITAL_PERSONNEL = enum.auto()
    EQUAL_RIGHTS = enum.auto()
    ESPRIT_SOCIAL = enum.auto()
    FARMER = enum.auto()
    FIRST_PEOPLES_NATIONAL_PARTY_OF_CANADA = enum.auto()
    FREE_PARTY_CANADA = enum.auto()
    GREEN_PARTY_OF_CANADA = enum.auto()
    INDEPENDENT = enum.auto()
    INDEPENDENT_COOPERATIVE_COMMONWEALTH_FEDERATION = enum.auto()
    INDEPENDENT_CONSERVATIVE = enum.auto()
    INDEPENDENT_LABOUR = enum.auto()
    INDEPENDENT_LIBERAL = enum.auto()
    INDEPENDENT_LIBERAL_PROGRESSIVE = enum.auto()
    INDEPENDENT_NATIONALIST = enum.auto()
    INDEPENDENT_PROGRESSIVE = enum.auto()
    INDEPENDENT_PROGRESSIVE_CONSERVATIVE = enum.auto()
    INDEPENDENT_SOCIAL_CREDIT = enum.auto()
    LABOR_PROGRESSIVE_PARTY = enum.auto()
    LABOUR = enum.auto()
    LIBERAL_LABOUR_PARTY = enum.auto()
    LIBERAL_LABOUR_PROGRESSIVE = enum.auto()
    LIBERAL_PARTY_OF_CANADA = enum.auto()
    LIBERAL_PROGRESSIVE = enum.auto()
    LIBERAL_PROTECTIONIST = enum.auto()
    LIBERAL_CONSERVATIVE = enum.auto()
    LIBERTARIAN_PARTY_OF_CANADA = enum.auto()
    LOCATAIRE_CANDIDAT = enum.auto()
    MARIJUANA_PARTY = enum.auto()
    MARXIST_LENINIST_PARTY_OF_CANADA = enum.auto()
    MAVERICK_PARTY = enum.auto()
    MCCARTHYITE = enum.auto()
    NATIONAL_ADVANCEMENT_PARTY_OF_CANADA = enum.auto()
    NATIONAL_CITIZENS_ALLIANCE = enum.auto()
    NATIONAL_CITIZENS_ALLIANCE_OF_CANADA = enum.auto()
    NATIONAL_CREDIT_CONTROL = enum.auto()
    NATIONAL_GOVERNMENT = enum.auto()
    NATIONAL_LABOUR = enum.auto()
    NATIONAL_LIBERAL_PROGRESSIVE = enum.auto()
    NATIONAL_LIBERAL_AND_CONSERVATIVE_PARTY_1921 = enum.auto()
    NATIONAL_PARTY_OF_CANADA = enum.auto()
    NATIONAL_SOCIALIST = enum.auto()
    NATIONAL_UNITY = enum.auto()
    NATIONALIST = enum.auto()
    NATIONALIST_CONSERVATIVE = enum.auto()
    NATIONALIST_LIBERAL = enum.auto()
    NATURAL_LAW_PARTY_OF_CANADA = enum.auto()
    NEW_CANADA_PARTY = enum.auto()
    NEW_DEMOCRACY = enum.auto()
    NEW_DEMOCRATIC_PARTY = enum.auto()
    NEW_PARTY = enum.auto()
    NEWFOUNDLAND_AND_LABRADOR_FIRST_PARTY = enum.auto()
    NO_AFFILIATION_TO_A_RECOGNISED_PARTY = enum.auto()
    NON_PARTISAN_LEAGUE = enum.auto()
    OPPOSITION = enum.auto()
    OPPOSITION_LABOUR = enum.auto()
    PARTI_HUMAIN_FAMILIAL = enum.auto()
    PARTI_NATIONALISTE_DU_QUÉBEC = enum.auto()
    PARTI_OUVRIER_CANADIEN = enum.auto()
    PARTI_PATRIOTE = enum.auto()
    PARTI_DE_LA_DÉMOCRATISATION_ÉCONOMIQUE = enum.auto()
    PARTI_POUR_LINDÉPENDANCE_DU_QUÉBEC = enum.auto()
    PARTY_FOR_THE_COMMONWEALTH_OF_CANADA = enum.auto()
    PATRONS_OF_INDUSTRY = enum.auto()
    PEOPLES_PARTY_OF_CANADA = enum.auto()
    PEOPLES_POLITICAL_POWER_PARTY_OF_CANADA = enum.auto()
    PIRATE_PARTY_OF_CANADA = enum.auto()
    PROGRESSIVE = enum.auto()
    PROGRESSIVE_CANADIAN_PARTY = enum.auto()
    PROGRESSIVE_CONSERVATIVE_PARTY = enum.auto()
    PROGRESSIVE_WORKERS_MOVEMENT = enum.auto()
    PROHIBITIONIST = enum.auto()
    PROTECTIONIST = enum.auto()
    PROTESTANT_PROTECTIVE_ASSOCIATION = enum.auto()
    RADICAL_CHRÉTIEN = enum.auto()
    RALLIEMENT_DES_CRÉDITISTES = enum.auto()
    RECONSTRUCTION_PARTY = enum.auto()
    REFORM = enum.auto()
    REFORM_PARTY_OF_CANADA = enum.auto()
    REPUBLICAN = enum.auto()
    REPUBLICAN_PARTY = enum.auto()
    RHINOCEROS_PARTY = enum.auto()
    RHINOCEROS_PARTY_OF_CANADA = enum.auto()
    SENIORS_PARTY_OF_CANADA = enum.auto()
    SOCIAL_CREDIT_PARTY_OF_CANADA = enum.auto()
    SOCIAL_CREDIT_NATIONAL_UNITY = enum.auto()
    SOCIALIST = enum.auto()
    SOCIALIST_LABOUR = enum.auto()
    STOP_CLIMATE_CHANGE_PARTY = enum.auto()
    STRENGTH_IN_DEMOCRACY = enum.auto()
    TECHNOCRAT = enum.auto()
    THE_BRIDGE_PARTY_OF_CANADA = enum.auto()
    TRADES_UNION = enum.auto()
    UNION_POPULAIRE = enum.auto()
    UNION_OF_ELECTORS = enum.auto()
    UNIONIST = enum.auto()
    UNIONIST_LIBERAL = enum.auto()
    UNITED_FARMERS = enum.auto()
    UNITED_FARMERS_OF_ALBERTA = enum.auto()
    UNITED_FARMERS_OF_ONTARIO = enum.auto()
    UNITED_FARMERS_OF_ONTARIO_LABOUR = enum.auto()
    UNITED_FARMERS_LABOUR = enum.auto()
    UNITED_PARTY_OF_CANADA = enum.auto()
    UNITED_PROGRESSIVE = enum.auto()
    UNITED_REFORM = enum.auto()
    UNITED_REFORM_MOVEMENT = enum.auto()
    UNITY = enum.auto()
    UNKNOWN = enum.auto()
    VETERANS_COALITION_PARTY_OF_CANADA = enum.auto()
    VETERANS_PARTY = enum.auto()
    WESTERN_BLOCK_PARTY = enum.auto()
    WORK_LESS_PARTY = enum.auto()
    NEORHINO = enum.auto()

    @staticmethod
    def from_name(name: str):
        return {
            "Abolitionist Party of Canada": PartyName.ABOLITIONIST_PARTY_OF_CANADA,
            "Accountability, Competency and Transparency": PartyName.ACCOUNTABILITY_COMPETENCY_AND_TRANSPARENCY,
            "All Canadian Party": PartyName.ALL_CANADIAN_PARTY,
            "Alliance of the North": PartyName.ALLIANCE_OF_THE_NORTH,
            "Animal Alliance Environment Voters Party of Canada": PartyName.ANIMAL_ALLIANCE_ENVIRONMENT_VOTERS_PARTY_OF_CANADA,
            "Animal Protection Party of Canada": PartyName.ANIMAL_PROTECTION_PARTY_OF_CANADA,
            "Anti-Confederate": PartyName.ANTI_CONFEDERATE,
            "Anti-Conscriptionist": PartyName.ANTI_CONSCRIPTIONIST,
            "Autonomist": PartyName.AUTONOMIST,
            "Bloc Québécois": PartyName.BLOC_QUÉBÉCOIS,
            "Bloc populaire canadien": PartyName.BLOC_POPULAIRE_CANADIEN,
            "Canada Party": PartyName.CANADA_PARTY,
            "Canada's Fourth Front": PartyName.CANADAS_FOURTH_FRONT,
            "Canadian Action Party": PartyName.CANADIAN_ACTION_PARTY,
            "Canadian Democrat": PartyName.CANADIAN_DEMOCRAT,
            "Canadian Future Party": PartyName.CANADIAN_FUTURE_PARTY,
            "Canadian Labour": PartyName.CANADIAN_LABOUR,
            "Canadian Nationalist Party": PartyName.CANADIAN_NATIONALIST_PARTY,
            "Canadian Party": PartyName.CANADIAN_PARTY,
            "Canadian Reform Conservative Alliance": PartyName.CANADIAN_REFORM_CONSERVATIVE_ALLIANCE,
            "Candidate of the Electors": PartyName.CANDIDATE_OF_THE_ELECTORS,
            "Capital Familial": PartyName.CAPITAL_FAMILIAL,
            "Centrist Party of Canada": PartyName.CENTRIST_PARTY_OF_CANADA,
            "Christian Heritage Party of Canada": PartyName.CHRISTIAN_HERITAGE_PARTY_OF_CANADA,
            "Christian Liberal": PartyName.CHRISTIAN_LIBERAL,
            "Co-operative Commonwealth Federation": PartyName.COOPERATIVE_COMMONWEALTH_FEDERATION,
            "Communist Party of Canada": PartyName.COMMUNIST_PARTY_OF_CANADA,
            "Confederation of Regions Western Party": PartyName.CONFEDERATION_OF_REGIONS_WESTERN_PARTY,
            "Conservative (1867-1942)": PartyName.CONSERVATIVE_1867_1942,
            "Conservative Party of Canada": PartyName.CONSERVATIVE_PARTY_OF_CANADA,
            "Conservative-Labour": PartyName.CONSERVATIVE_LABOUR,
            "Cooperative Builders of Canada": PartyName.COOPERATIVE_BUILDERS_OF_CANADA,
            "Democrat": PartyName.DEMOCRAT,
            "Droit vital personnel": PartyName.DROIT_VITAL_PERSONNEL,
            "Equal Rights": PartyName.EQUAL_RIGHTS,
            "Esprit Social": PartyName.ESPRIT_SOCIAL,
            "Farmer": PartyName.FARMER,
            "First Peoples National Party of Canada": PartyName.FIRST_PEOPLES_NATIONAL_PARTY_OF_CANADA,
            "Free Party Canada": PartyName.FREE_PARTY_CANADA,
            "Green Party of Canada": PartyName.GREEN_PARTY_OF_CANADA,
            "Independent": PartyName.INDEPENDENT,
            "Independent Co-operative Commonwealth Federation": PartyName.INDEPENDENT_COOPERATIVE_COMMONWEALTH_FEDERATION,
            "Independent Conservative": PartyName.INDEPENDENT_CONSERVATIVE,
            "Independent Labour": PartyName.INDEPENDENT_LABOUR,
            "Independent Liberal": PartyName.INDEPENDENT_LIBERAL,
            "Independent Liberal Progressive": PartyName.INDEPENDENT_LIBERAL_PROGRESSIVE,
            "Independent Nationalist": PartyName.INDEPENDENT_NATIONALIST,
            "Independent Progressive": PartyName.INDEPENDENT_PROGRESSIVE,
            "Independent Progressive Conservative": PartyName.INDEPENDENT_PROGRESSIVE_CONSERVATIVE,
            "Independent Social Credit": PartyName.INDEPENDENT_SOCIAL_CREDIT,
            "Labor-Progressive Party": PartyName.LABOR_PROGRESSIVE_PARTY,
            "Labour": PartyName.LABOUR,
            "Liberal Labour Party": PartyName.LIBERAL_LABOUR_PARTY,
            "Liberal Labour Progressive": PartyName.LIBERAL_LABOUR_PROGRESSIVE,
            "Liberal Party of Canada": PartyName.LIBERAL_PARTY_OF_CANADA,
            "Liberal Progressive": PartyName.LIBERAL_PROGRESSIVE,
            "Liberal Protectionist": PartyName.LIBERAL_PROTECTIONIST,
            "Liberal-Conservative": PartyName.LIBERAL_CONSERVATIVE,
            "Libertarian Party of Canada": PartyName.LIBERTARIAN_PARTY_OF_CANADA,
            "Locataire (candidat)": PartyName.LOCATAIRE_CANDIDAT,
            "Marijuana Party": PartyName.MARIJUANA_PARTY,
            "Marxist-Leninist Party of Canada": PartyName.MARXIST_LENINIST_PARTY_OF_CANADA,
            "Maverick Party": PartyName.MAVERICK_PARTY,
            "McCarthyite": PartyName.MCCARTHYITE,
            "National Advancement Party of Canada": PartyName.NATIONAL_ADVANCEMENT_PARTY_OF_CANADA,
            "National Citizens Alliance": PartyName.NATIONAL_CITIZENS_ALLIANCE,
            "National Citizens Alliance of Canada": PartyName.NATIONAL_CITIZENS_ALLIANCE_OF_CANADA,
            "National Credit Control": PartyName.NATIONAL_CREDIT_CONTROL,
            "National Government": PartyName.NATIONAL_GOVERNMENT,
            "National Labour": PartyName.NATIONAL_LABOUR,
            "National Liberal Progressive": PartyName.NATIONAL_LIBERAL_PROGRESSIVE,
            "National Liberal and Conservative Party (1921)": PartyName.NATIONAL_LIBERAL_AND_CONSERVATIVE_PARTY_1921,
            "National Party of Canada": PartyName.NATIONAL_PARTY_OF_CANADA,
            "National Socialist": PartyName.NATIONAL_SOCIALIST,
            "National Unity": PartyName.NATIONAL_UNITY,
            "Nationalist": PartyName.NATIONALIST,
            "Nationalist Conservative": PartyName.NATIONALIST_CONSERVATIVE,
            "Nationalist Liberal": PartyName.NATIONALIST_LIBERAL,
            "Natural Law Party of Canada": PartyName.NATURAL_LAW_PARTY_OF_CANADA,
            "New Canada Party": PartyName.NEW_CANADA_PARTY,
            "New Democracy": PartyName.NEW_DEMOCRACY,
            "New Democratic Party": PartyName.NEW_DEMOCRATIC_PARTY,
            "New Party": PartyName.NEW_PARTY,
            "Newfoundland and Labrador First Party": PartyName.NEWFOUNDLAND_AND_LABRADOR_FIRST_PARTY,
            "No affiliation to a recognised party": PartyName.NO_AFFILIATION_TO_A_RECOGNISED_PARTY,
            "Non-Partisan League": PartyName.NON_PARTISAN_LEAGUE,
            "Opposition": PartyName.OPPOSITION,
            "Opposition-Labour": PartyName.OPPOSITION_LABOUR,
            "Parti Humain Familial": PartyName.PARTI_HUMAIN_FAMILIAL,
            "Parti Nationaliste du Québec": PartyName.PARTI_NATIONALISTE_DU_QUÉBEC,
            "Parti Ouvrier Canadien": PartyName.PARTI_OUVRIER_CANADIEN,
            "Parti Patriote": PartyName.PARTI_PATRIOTE,
            "Parti de la Démocratisation Économique": PartyName.PARTI_DE_LA_DÉMOCRATISATION_ÉCONOMIQUE,
            "Parti pour l'Indépendance du Québec": PartyName.PARTI_POUR_LINDÉPENDANCE_DU_QUÉBEC,
            "Party for the Commonwealth of Canada": PartyName.PARTY_FOR_THE_COMMONWEALTH_OF_CANADA,
            "Patrons of Industry": PartyName.PATRONS_OF_INDUSTRY,
            "People's Party of Canada": PartyName.PEOPLES_PARTY_OF_CANADA,
            "People's Party of Canada ": PartyName.PEOPLES_PARTY_OF_CANADA,
            "People's Political Power Party of Canada": PartyName.PEOPLES_POLITICAL_POWER_PARTY_OF_CANADA,
            "Pirate Party of Canada": PartyName.PIRATE_PARTY_OF_CANADA,
            "Progressive": PartyName.PROGRESSIVE,
            "Progressive Canadian Party": PartyName.PROGRESSIVE_CANADIAN_PARTY,
            "Progressive Conservative Party": PartyName.PROGRESSIVE_CONSERVATIVE_PARTY,
            "Progressive Workers Movement": PartyName.PROGRESSIVE_WORKERS_MOVEMENT,
            "Prohibitionist": PartyName.PROHIBITIONIST,
            "Protectionist": PartyName.PROTECTIONIST,
            "Protestant Protective Association": PartyName.PROTESTANT_PROTECTIVE_ASSOCIATION,
            "Radical Chrétien": PartyName.RADICAL_CHRÉTIEN,
            "Ralliement des créditistes": PartyName.RALLIEMENT_DES_CRÉDITISTES,
            "Reconstruction Party": PartyName.RECONSTRUCTION_PARTY,
            "Reform": PartyName.REFORM,
            "Reform Party of Canada": PartyName.REFORM_PARTY_OF_CANADA,
            "Republican": PartyName.REPUBLICAN,
            "Republican Party": PartyName.REPUBLICAN_PARTY,
            "Rhinoceros Party": PartyName.RHINOCEROS_PARTY,
            "Rhinoceros Party of Canada": PartyName.RHINOCEROS_PARTY_OF_CANADA,
            "Seniors Party of Canada": PartyName.SENIORS_PARTY_OF_CANADA,
            "Social Credit Party of Canada": PartyName.SOCIAL_CREDIT_PARTY_OF_CANADA,
            "Social Credit-National Unity": PartyName.SOCIAL_CREDIT_NATIONAL_UNITY,
            "Socialist": PartyName.SOCIALIST,
            "Socialist Labour": PartyName.SOCIALIST_LABOUR,
            "Stop Climate Change Party": PartyName.STOP_CLIMATE_CHANGE_PARTY,
            "Strength in Democracy": PartyName.STRENGTH_IN_DEMOCRACY,
            "Technocrat": PartyName.TECHNOCRAT,
            "The Bridge Party of Canada": PartyName.THE_BRIDGE_PARTY_OF_CANADA,
            "Trades Union": PartyName.TRADES_UNION,
            "Union Populaire": PartyName.UNION_POPULAIRE,
            "Union of Electors": PartyName.UNION_OF_ELECTORS,
            "Unionist": PartyName.UNIONIST,
            "Unionist (Liberal)": PartyName.UNIONIST_LIBERAL,
            "United Farmers": PartyName.UNITED_FARMERS,
            "United Farmers of Alberta": PartyName.UNITED_FARMERS_OF_ALBERTA,
            "United Farmers of Ontario": PartyName.UNITED_FARMERS_OF_ONTARIO,
            "United Farmers of Ontario-Labour": PartyName.UNITED_FARMERS_OF_ONTARIO_LABOUR,
            "United Farmers-Labour": PartyName.UNITED_FARMERS_LABOUR,
            "United Party of Canada": PartyName.UNITED_PARTY_OF_CANADA,
            "United Progressive": PartyName.UNITED_PROGRESSIVE,
            "United Reform": PartyName.UNITED_REFORM,
            "United Reform Movement": PartyName.UNITED_REFORM_MOVEMENT,
            "Unity": PartyName.UNITY,
            "Unknown": PartyName.UNKNOWN,
            "Veterans Coalition Party of Canada": PartyName.VETERANS_COALITION_PARTY_OF_CANADA,
            "Veterans Party": PartyName.VETERANS_PARTY,
            "Western Block Party": PartyName.WESTERN_BLOCK_PARTY,
            "Work Less Party": PartyName.WORK_LESS_PARTY,
            "neorhino.ca": PartyName.NEORHINO,
        }[name]

    @property
    def color(self):
        return {
            PartyName.ABOLITIONIST_PARTY_OF_CANADA: Color.BLACK,
            PartyName.ACCOUNTABILITY_COMPETENCY_AND_TRANSPARENCY: Color.BLACK,
            PartyName.ALL_CANADIAN_PARTY: Color.BLACK,
            PartyName.ALLIANCE_OF_THE_NORTH: Color.BLACK,
            PartyName.ANIMAL_ALLIANCE_ENVIRONMENT_VOTERS_PARTY_OF_CANADA: Color.BLACK,
            PartyName.ANIMAL_PROTECTION_PARTY_OF_CANADA: Color.BLACK,
            PartyName.ANTI_CONFEDERATE: Color.ORANGE,
            PartyName.ANTI_CONSCRIPTIONIST: Color.BLACK,
            PartyName.AUTONOMIST: Color.BLACK,
            PartyName.BLOC_QUÉBÉCOIS: Color.CYAN,
            PartyName.BLOC_POPULAIRE_CANADIEN: Color.BLACK,
            PartyName.CANADA_PARTY: Color.BLACK,
            PartyName.CANADAS_FOURTH_FRONT: Color.BLACK,
            PartyName.CANADIAN_ACTION_PARTY: Color.BLACK,
            PartyName.CANADIAN_DEMOCRAT: Color.BLACK,
            PartyName.CANADIAN_FUTURE_PARTY: Color.BLACK,
            PartyName.CANADIAN_LABOUR: Color.BLACK,
            PartyName.CANADIAN_NATIONALIST_PARTY: Color.BLACK,
            PartyName.CANADIAN_PARTY: Color.BLACK,
            PartyName.CANADIAN_REFORM_CONSERVATIVE_ALLIANCE: Color.GREEN,
            PartyName.CANDIDATE_OF_THE_ELECTORS: Color.BLACK,
            PartyName.CAPITAL_FAMILIAL: Color.BLACK,
            PartyName.CENTRIST_PARTY_OF_CANADA: Color.BLACK,
            PartyName.CHRISTIAN_HERITAGE_PARTY_OF_CANADA: Color.BLACK,
            PartyName.CHRISTIAN_LIBERAL: Color.BLACK,
            PartyName.COOPERATIVE_COMMONWEALTH_FEDERATION: Color.ORANGE,
            PartyName.COMMUNIST_PARTY_OF_CANADA: Color.BLACK,
            PartyName.CONFEDERATION_OF_REGIONS_WESTERN_PARTY: Color.BLACK,
            PartyName.CONSERVATIVE_1867_1942: Color.BLUE,
            PartyName.CONSERVATIVE_PARTY_OF_CANADA: Color.BLUE,
            PartyName.CONSERVATIVE_LABOUR: Color.BLACK,
            PartyName.COOPERATIVE_BUILDERS_OF_CANADA: Color.BLACK,
            PartyName.DEMOCRAT: Color.BLACK,
            PartyName.DROIT_VITAL_PERSONNEL: Color.BLACK,
            PartyName.EQUAL_RIGHTS: Color.BLACK,
            PartyName.ESPRIT_SOCIAL: Color.BLACK,
            PartyName.FARMER: Color.BLACK,
            PartyName.FIRST_PEOPLES_NATIONAL_PARTY_OF_CANADA: Color.BLACK,
            PartyName.FREE_PARTY_CANADA: Color.BLACK,
            PartyName.GREEN_PARTY_OF_CANADA: Color.GREEN,
            PartyName.INDEPENDENT: Color.GREY,
            PartyName.INDEPENDENT_COOPERATIVE_COMMONWEALTH_FEDERATION: Color.GREY,
            PartyName.INDEPENDENT_CONSERVATIVE: Color.GREY,
            PartyName.INDEPENDENT_LABOUR: Color.GREY,
            PartyName.INDEPENDENT_LIBERAL: Color.GREY,
            PartyName.INDEPENDENT_LIBERAL_PROGRESSIVE: Color.GREY,
            PartyName.INDEPENDENT_NATIONALIST: Color.GREY,
            PartyName.INDEPENDENT_PROGRESSIVE: Color.GREY,
            PartyName.INDEPENDENT_PROGRESSIVE_CONSERVATIVE: Color.GREY,
            PartyName.INDEPENDENT_SOCIAL_CREDIT: Color.GREY,
            PartyName.LABOR_PROGRESSIVE_PARTY: Color.BLACK,
            PartyName.LABOUR: Color.GREEN,
            PartyName.LIBERAL_LABOUR_PARTY: Color.PINK,
            PartyName.LIBERAL_LABOUR_PROGRESSIVE: Color.BLACK,
            PartyName.LIBERAL_PARTY_OF_CANADA: Color.RED,
            PartyName.LIBERAL_PROGRESSIVE: Color.YELLOW,
            PartyName.LIBERAL_PROTECTIONIST: Color.BLACK,
            PartyName.LIBERAL_CONSERVATIVE: Color.PURPLE,
            PartyName.LIBERTARIAN_PARTY_OF_CANADA: Color.BLACK,
            PartyName.LOCATAIRE_CANDIDAT: Color.BLACK,
            PartyName.MARIJUANA_PARTY: Color.BLACK,
            PartyName.MARXIST_LENINIST_PARTY_OF_CANADA: Color.BLACK,
            PartyName.MAVERICK_PARTY: Color.BLACK,
            PartyName.MCCARTHYITE: Color.BLACK,
            PartyName.NATIONAL_ADVANCEMENT_PARTY_OF_CANADA: Color.BLACK,
            PartyName.NATIONAL_CITIZENS_ALLIANCE: Color.BLACK,
            PartyName.NATIONAL_CITIZENS_ALLIANCE_OF_CANADA: Color.BLACK,
            PartyName.NATIONAL_CREDIT_CONTROL: Color.BLACK,
            PartyName.NATIONAL_GOVERNMENT: Color.BLUE,
            PartyName.NATIONAL_LABOUR: Color.BLACK,
            PartyName.NATIONAL_LIBERAL_PROGRESSIVE: Color.BLACK,
            PartyName.NATIONAL_LIBERAL_AND_CONSERVATIVE_PARTY_1921: Color.BLACK,
            PartyName.NATIONAL_PARTY_OF_CANADA: Color.BLACK,
            PartyName.NATIONAL_SOCIALIST: Color.BLACK,
            PartyName.NATIONAL_UNITY: Color.BLACK,
            PartyName.NATIONALIST: Color.BLACK,
            PartyName.NATIONALIST_CONSERVATIVE: Color.CYAN,
            PartyName.NATIONALIST_LIBERAL: Color.BLACK,
            PartyName.NATURAL_LAW_PARTY_OF_CANADA: Color.BLACK,
            PartyName.NEW_CANADA_PARTY: Color.BLACK,
            PartyName.NEW_DEMOCRACY: Color.BLACK,
            PartyName.NEW_DEMOCRATIC_PARTY: Color.ORANGE,
            PartyName.NEW_PARTY: Color.BLACK,
            PartyName.NEWFOUNDLAND_AND_LABRADOR_FIRST_PARTY: Color.BLACK,
            PartyName.NO_AFFILIATION_TO_A_RECOGNISED_PARTY: Color.BLACK,
            PartyName.NON_PARTISAN_LEAGUE: Color.BLACK,
            PartyName.OPPOSITION: Color.RED,
            PartyName.OPPOSITION_LABOUR: Color.BLACK,
            PartyName.PARTI_HUMAIN_FAMILIAL: Color.BLACK,
            PartyName.PARTI_NATIONALISTE_DU_QUÉBEC: Color.BLACK,
            PartyName.PARTI_OUVRIER_CANADIEN: Color.BLACK,
            PartyName.PARTI_PATRIOTE: Color.BLACK,
            PartyName.PARTI_DE_LA_DÉMOCRATISATION_ÉCONOMIQUE: Color.BLACK,
            PartyName.PARTI_POUR_LINDÉPENDANCE_DU_QUÉBEC: Color.BLACK,
            PartyName.PARTY_FOR_THE_COMMONWEALTH_OF_CANADA: Color.BLACK,
            PartyName.PATRONS_OF_INDUSTRY: Color.BLACK,
            PartyName.PEOPLES_PARTY_OF_CANADA: Color.PURPLE,
            PartyName.PEOPLES_POLITICAL_POWER_PARTY_OF_CANADA: Color.BLACK,
            PartyName.PIRATE_PARTY_OF_CANADA: Color.BLACK,
            PartyName.PROGRESSIVE: Color.GREEN,
            PartyName.PROGRESSIVE_CANADIAN_PARTY: Color.BLACK,
            PartyName.PROGRESSIVE_CONSERVATIVE_PARTY: Color.BLUE,
            PartyName.PROGRESSIVE_WORKERS_MOVEMENT: Color.BLACK,
            PartyName.PROHIBITIONIST: Color.BLACK,
            PartyName.PROTECTIONIST: Color.BLACK,
            PartyName.PROTESTANT_PROTECTIVE_ASSOCIATION: Color.BLACK,
            PartyName.RADICAL_CHRÉTIEN: Color.BLACK,
            PartyName.RALLIEMENT_DES_CRÉDITISTES: Color.BLACK,
            PartyName.RECONSTRUCTION_PARTY: Color.BLACK,
            PartyName.REFORM: Color.BLACK,
            PartyName.REFORM_PARTY_OF_CANADA: Color.GREEN,
            PartyName.REPUBLICAN: Color.BLACK,
            PartyName.REPUBLICAN_PARTY: Color.BLACK,
            PartyName.RHINOCEROS_PARTY: Color.BLACK,
            PartyName.RHINOCEROS_PARTY_OF_CANADA: Color.BLACK,
            PartyName.SENIORS_PARTY_OF_CANADA: Color.BLACK,
            PartyName.SOCIAL_CREDIT_PARTY_OF_CANADA: Color.GREEN,
            PartyName.SOCIAL_CREDIT_NATIONAL_UNITY: Color.BLACK,
            PartyName.SOCIALIST: Color.BLACK,
            PartyName.SOCIALIST_LABOUR: Color.BLACK,
            PartyName.STOP_CLIMATE_CHANGE_PARTY: Color.BLACK,
            PartyName.STRENGTH_IN_DEMOCRACY: Color.BLACK,
            PartyName.TECHNOCRAT: Color.BLACK,
            PartyName.THE_BRIDGE_PARTY_OF_CANADA: Color.BLACK,
            PartyName.TRADES_UNION: Color.BLACK,
            PartyName.UNION_POPULAIRE: Color.BLACK,
            PartyName.UNION_OF_ELECTORS: Color.BLACK,
            PartyName.UNIONIST: Color.BLUE,
            PartyName.UNIONIST_LIBERAL: Color.ORANGE,
            PartyName.UNITED_FARMERS: Color.BLACK,
            PartyName.UNITED_FARMERS_OF_ALBERTA: Color.BLACK,
            PartyName.UNITED_FARMERS_OF_ONTARIO: Color.BLACK,
            PartyName.UNITED_FARMERS_OF_ONTARIO_LABOUR: Color.BLACK,
            PartyName.UNITED_FARMERS_LABOUR: Color.BLACK,
            PartyName.UNITED_PARTY_OF_CANADA: Color.BLACK,
            PartyName.UNITED_PROGRESSIVE: Color.BLACK,
            PartyName.UNITED_REFORM: Color.BLACK,
            PartyName.UNITED_REFORM_MOVEMENT: Color.BLACK,
            PartyName.UNITY: Color.BLACK,
            PartyName.UNKNOWN: Color.BLACK,
            PartyName.VETERANS_COALITION_PARTY_OF_CANADA: Color.BLACK,
            PartyName.VETERANS_PARTY: Color.BLACK,
            PartyName.WESTERN_BLOCK_PARTY: Color.BLACK,
            PartyName.WORK_LESS_PARTY: Color.BLACK,
            PartyName.NEORHINO: Color.BLACK,
        }[self]


class Color(enum.Enum):
    BLACK = 1
    GREY = 2
    WHITE = 3

    RED = 4
    ORANGE = 5
    YELLOW = 6
    GREEN = 7
    CYAN = 8
    BLUE = 9
    PINK = 10
    PURPLE = 11


class Record(abc.ABC):
    # TODO: Make this recursive and cleaner.
    def to_json(self):
        ret = {}
        for k, v in vars(self).items():
            if isinstance(v, enum.Enum):
                ret[k] = v.name
            elif isinstance(v, Record):
                ret[k] = v.id()
            elif isinstance(v, datetime.date):
                ret[k] = {"year": v.year, "month": v.month, "day": v.day}
            elif isinstance(v, dict):
                for k2, v2 in v.items():
                    if isinstance(v2, list):
                        if len(v2) > 0 and isinstance(v2[0], Record):
                            v[k2] = [v3.id() for v3 in v2]
                    elif isinstance(v2, Record):
                        v[k2] = v2.id()
                ret[k] = v
            elif isinstance(v, list):
                if len(v) > 0 and isinstance(v[0], Record):
                    ret[k] = [v2.id() for v2 in v]
                else:
                    ret[k] = v
            else:
                ret[k] = v

        return ret

    def __hash__(self):
        return hash(self.id())

    def __eq__(self, other):
        return self.id() == other.id()


class Party(Record):
    def __init__(self, name: str):
        self.name = PartyName.from_name(name)
        self.color = self.name.color
        self.has_won_election = False

    def id(self):
        return hash_string(str(self.name.value))




class Geometry(Record):
    def __init__(self, name: str, id_num: int, shape: Polygon):
        self.name = name
        self.id_num = id_num
        self.shape = shape

    @property
    def area(self):
        return int(self.shape.area / 1e6)

    def intersects(self, other):
        return self.shape.intersects(other)

    @staticmethod
    def process_svg(svg):
        for attr_key in ["fill", "stroke", "stroke-width", "opacity"]:
            svg.attrib.pop(attr_key, None)

        if "d" not in svg.attrib:
            return

        new_d = []
        for split1 in svg.attrib["d"].split(" "):
            new_split1 = []
            for split2 in split1.split(","):
                try:
                    float(split2)
                except ValueError:
                    new_split1.append(split2)
                    continue
                new_split1.append(f"{float(split2):.0f}")
            new_d.append(",".join(new_split1))
        svg.attrib["d"] = " ".join(new_d)

    def to_svg(self, tolerance) -> str:
        simple_geometry = self.shape.simplify(tolerance, preserve_topology=False)
        svg = simple_geometry.svg()
        xml_svg = xml.etree.ElementTree.fromstring(svg)
        self.process_svg(xml_svg)
        for child in xml_svg:
            self.process_svg(child)

        return xml.etree.ElementTree.tostring(xml_svg).decode("utf-8")

    def id(self):
        return str(self.id_num)

    def to_json(self):
        return {
            "name": self.name,
            "area": self.area,
        }


class Riding(Record):
    def __init__(
        self,
        name: str,
        province: Province,
        start_date: datetime.date,
        end_date: datetime.date,
        geometry_by_year: typing.Dict[int, Geometry],
        summary: str | None,
        summary_url: str | None,
    ):
        self.name = name
        self.province = province
        self.start_date = start_date
        self.end_date = end_date
        self.geometry_by_year = geometry_by_year
        self.summary = summary
        self.summary_url = summary_url

    def id(self):
        return hash_string(
            self.name + str(self.province) + str(self.start_date) + str(self.end_date)
        )


class DetailView(Record):
    def __init__(
        self,
        name: DetailViewName,
        ridings_by_year: typing.Dict[int, Riding],
        x: int,
        y: int,
        width: int,
        height: int,
    ):
        self.name = name
        self.ridings_by_year = ridings_by_year
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def id(self):
        return self.name.name


class Candidate(Record):
    def __init__(
        self, first_name: str, last_name: str, gender: Gender, index: int = -1
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.runs = []
        self.record = {}
        self.index = index

    def id(self):
        return hash_string(
            self.first_name + self.last_name + str(self.gender) + str(self.index)
        )


class GovernmentType(enum.Enum):
    MINORITY = enum.auto()
    MAJORITY = enum.auto()

    @staticmethod
    def from_string(s: str):
        return {
            "Minority": GovernmentType.MINORITY,
            "Majority": GovernmentType.MINORITY,
        }[s]



class Parliament(Record):
    def __init__(
            self,
            number: int,
            start_date: datetime.date,
            end_date: datetime.date,
            gov_parties: typing.List[Party],
            oppo_parties: typing.List[Party],
            prime_ministers: typing.List[Candidate],
            oppo_leaders: typing.List[Candidate],
            government_type: GovernmentType,
            sessions: int,
            throne_speeches: int,
            budgets: int,
            senate_nominations: int,
        ):
        self.number = number
        self.start_date = start_date
        self.end_date = end_date
        self.gov_parties = gov_parties
        self.oppo_parties = oppo_parties
        self.prime_ministers = prime_ministers
        self.oppo_leaders = oppo_leaders
        self.government_type = government_type
        self.sessions = sessions
        self.throne_speeches = throne_speeches
        self.budgets = budgets
        self.senate_nominations = senate_nominations

    def id(self):
        return str(self.number)


class Election(Record):
    def __init__(
        self,
        date: datetime.date,
        type: ElectionType,
        parliament: int,
        riding: Riding | None = None,
        summary: typing.List[str] | None = None
    ):
        self.date = date
        self.type = type
        self.parliament = parliament
        self.runs = []
        self.riding = riding
        self.summary = summary

    def id(self):
        riding_str = self.riding.id() if self.riding is not None else ""
        return hash_string(
            str(self.date) + str(self.type) + str(self.parliament) + riding_str
        )


class Run(Record):
    def __init__(
        self,
        election: Election,
        riding: Riding,
        candidate: Candidate,
        party: Party,
        result: ElectionResult,
        votes: int,
        occupation: str,
    ):
        self.election = election
        self.riding = riding
        self.candidate = candidate
        self.party = party
        self.result = result
        self.votes = votes
        self.occupation = occupation

    def id(self):
        return hash_string(
            self.election.id()
            + self.riding.id()
            + self.candidate.id()
            + self.party.id()
            + str(self.result)
            + str(self.votes)
            + str(self.occupation)
        )
