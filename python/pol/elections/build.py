import datetime
import json
import xml

import geopandas
import openpyxl
from pol.elections.structures import *
from pol.paths import ARTIFACT_DIR, CACHE_DIR, SOURCES_DIR, WEB_ARTIFACT_DIR

PARTY_COLORS = {
    "Liberal Party of Canada": Color.RED,
    "Anti-Confederate": Color.ORANGE,
    "New Democratic Party": Color.ORANGE,
    "Conservative (1867-1942)": Color.BLUE,
    "Conservative Party of Canada": Color.BLUE,
    "Green Party of Canada": Color.GREEN,
    "Liberal-Conservative": Color.PURPLE,
    "Bloc Québécois": Color.YELLOW,
    "Independent": Color.GREY,
}

# Keys are the geo dataset's "fedid" field.
# Comments are the name in the geo dataset
# "name" tag is the name in the EC dataset.
# "province" tag is the province in the EC dataset.

# Most of these corrections are due to either poor data quality
# in the geo dataset or changes in riding names over time.
GEO_ID_TO_EC_RIDINGS = {
    186712011: {  # Kings (N.S.)
        "name": "Kings",
        "province": "Nova Scotia",
    },
    186712017: {  # Victoria (N.S.)
        "name": "Victoria",
        "province": "Nova Scotia",
    },
    186713002: {  # Carleton (N.B.)
        "name": "Carleton",
        "province": "New Brunswick",
    },
    186713004: {  # City and County of St. John
        "name": "St. John (City and County of)",
        "province": "New Brunswick",
    },
    186713005: {  # City of St. John
        "name": "St. John (City of )",
        "province": "New Brunswick",
    },
    186713007: {  # Kent (N.B.)
        "name": "Kent",
        "province": "New Brunswick",
    },
    186713008: {  # Kings (N.B.)
        "name": "King's",
        "province": "New Brunswick",
    },
    186713010: {  # Queens
        "name": "Queens",
        "province": "Nova Scotia",
    },
    186713013: {  # Victoria (N.B.)
        "name": "Victoria",
        "province": "New Brunswick",
    },
    186712014: {  # Queens
        "name": "Queen's",
        "province": "New Brunswick",
    },
    186724021: {  # Jacques-Cartier
        "name": "Jacques Cartier",
        "province": "Quebec",
    },
    186724037: {  # Montreal Est
        "name": "Montreal East",
        "province": "Quebec",
    },
    186724038: {  # Montreal Ouest
        "name": "Montreal West",
        "province": "Quebec",
    },
    186724041: {  # Ottawa
        "name": "Ottawa (City of)",
        "province": "Ontario",
    },
    186724044: {  # Québec (Comté)
        "name": "Quebec County",
        "province": "Quebec",
    },
    186724045: {  # Québec-Est
        "name": "Quebec East",
        "province": "Quebec",
    },
    186724046: {  # Québec-Ouest
        "name": "Quebec West",
        "province": "Quebec",
    },
    186724047: {  # Québec-Centre
        "name": "Quebec-Centre",
        "province": "Quebec",
    },
    186724052: {  # Saint-Maurice
        "name": "Saint Maurice",
        "province": "Quebec",
    },
    186724054: {  # Sherbrooke
        "name": "Sherbrooke (Town of)",
        "province": "Quebec",
    },
    186724056: {  # Saint-Hyacinthe
        "name": "St. Hyacinthe",
        "province": "Quebec",
    },
    186724057: {  # Saint-Jean
        "name": "St. John's",
        "province": "Quebec",
    },
    186724061: {  # Trois-Rivières
        "name": "Three Rivers",
        "province": "Quebec",
    },
    186724062: {  # Deux-Montagnes
        "name": "Two Mountains",
        "province": "Quebec",
    },
    186735010: {  # Carleton (Ont.)
        "name": "Carleton",
        "province": "Ontario",
    },
    186735031: {  # Kent (Ont.)
        "name": "Kent",
        "province": "Ontario",
    },
    186735052: {  # Ottawa (is the ID a mistake? Has the Ontario prefix)
        "name": "Ottawa (County of)",
        "province": "Quebec",
    },
    186759001: {  # Cariboo
        "name": "Cariboo District",
        "province": "British Columbia",
    },
    186759002: {  # New Westminster
        "name": "New Westminster District",
        "province": "British Columbia",
    },
    186759003: {  # Vancouver
        "name": "Vancouver Island",
        "province": "British Columbia",
    },
    186759004: [  # Victoria (B.C.)
        {
            "name": "Victoria",
            "province": "British Columbia",
        },
        {
            "name": "Victoria District",
            "province": "British Columbia",
        },
    ],
    186759005: {  # Yale
        "name": "Yale District",
        "province": "British Columbia",
    },
    ####################
    ### 1872 RIDINGS ###
    ####################
    187211002: { # Prince
        "name": "Prince County",
        "province": "Prince Edward Island",
    },
    187211003: { # Queens  TODO
        "name": "Queen's County",
        "province": "Prince Edward Island",
    },
    187259004: {  # Victoria (B.C.)
        "name": "Victoria",
        "province": "British Columbia",
    },
    ####################
    ### 1882 RIDINGS ###
    ####################

    ####################
    ### 1892 RIDINGS ###
    ####################
    189211005: {  # West Queens
        "name": "West Queen's",
        "province": "Prince Edward Island",
    },
    189212015: { # Shelburne and Queens
        "name": "Shelburne and Queen's",
        "province": "Nova Scotia",
    },
    189224051: { # Sainte-Anne
        "name": "St. Anne",
        "province": "Quebec",
    },
    189224052: { # Saint-Antoine
        "name": "St. Antoine",
        "province": "Quebec",
    },
    189224054: { # Saint-Jacques
        "name": "St. James",
        "province": "Quebec",
    },
    189224055: { # Saint-Jean--Iberville
        "name": "St. Johns--Iberville",
        "province": "Quebec",
    },
    189224056: { # Saint-Laurent
        "name": "St. Lawrence",
        "province": "Quebec",
    },
    189224057: { # Sainte-Marie
        "name": "St. Mary",
        "province": "Quebec",
    },
    189224061: { # Trois-Rivières et Saint-Maurice
        "name": "Three Rivers and St. Maurice",
        "province": "Quebec",
    },
    189213011: { # Sunbury--Queens
        "name": "Sunbury--Queen's",
        "province": "New Brunswick",
    },
    ####################
    ### 1903 RIDINGS ###
    ####################
    190311003: { # Queens
        "name": "Queen's",
        "province": "Prince Edward Island",
    },
    190312013: { # Victoria and Cape Breton North
        "name": "North Cape Breton and Victoria",
        "province": "Nova Scotia",
    },
    190335075: {  # Victoria (Ont.)
        "name": "Victoria",
        "province": "Ontario",
    },
    ####################
    ### 1905 RIDINGS ###
    ####################
    190548007: {  # Victoria (Alta.)
        "name": "Victoria",
        "province": "Alberta",
    },
    ####################
    ### 1914 RIDINGS ###
    ####################
    191413007: { # Saint John--Albert
        "name": "St. John--Albert",
        "province": "New Brunswick",
    },
    191424029: { # Laval--Deux-Montagnes
        "name": "Laval--Two Mountains",
        "province": "Quebec",
    },
    191424043: { # Québec-Sud
        "name": "Quebec South",
        "province": "Quebec",
    },
    191424050: { # Sainte-Anne
        "name": "St. Ann",
        "province": "Quebec",
    },
    191424052: { # Saint-Denis
        "name": "St. Denis",
        "province": "Quebec",
    },
    191424053: { # Saint-Hyacinthe--Rouville
        "name": "St. Hyacinthe--Rouville",
        "province": "Quebec",
    },
    191424056: { # Saint-Laurent--Saint-Georges
        "name": "St. Lawrence--St. George",
        "province": "Quebec",
    },
    191424063: {  # Westmount--Saint-Henri
        "name": "Westmount--St. Henri",
        "province": "Quebec",
    },
    191435043: { # Northumberland (Ont.)
        "name": "Northumberland",
        "province": "Ontario",
    },
    191459007: {  # New Westminster
        "name": "Westminster District",
        "province": "British Columbia",
    },
    ####################
    ### 1924 RIDINGS ###
    ####################
    192424027: { # Lac-Saint-Jean
        "name": "Lake St. John",
        "province": "Quebec",
    },
    192424053: { # Saint-Henri
        "name": "St. Henri",
        "province": "Quebec",
    },
    193324060: { # Saint-Denis
        "name": "St. Denis",
        "province": "Quebec",
    },
    192424062: { # Trois-Rivières--Saint-Maurice
        "name": "Three Rivers--St. Maurice",
        "province": "Quebec",
    },
    192459013: {  # Victoria (B.C.)
        "name": "Victoria",
        "province": "British Columbia",
    },
    ####################
    ### 1933 RIDINGS ###
    ####################
    193324022: { # Lac-Saint-Jean--Roberval
        "name": "Lake St-John--Roberval",
        "province": "Quebec",
    },
    193324028: { # Montmagny--L'Islet
        "name": "Montmagny--l'Islet",
        "province": "Quebec",
    },
    193324034: { # Québec-Ouest-et-Sud
        "name": "Quebec West and South",
        "province": "Quebec",
    },
    193324039: { # Saint-Hyacinthe--Bagot
        "name": "St. Hyacinthe--Bagot",
        "province": "Quebec",
    },
    193324040: { # Saint-Jean--Iberville--Napierville
        "name": "St. Johns--Iberville--Napierville",
        "province": "Quebec",
    },
    193324041: { # Saint-Maurice--Laflèche
        "name": "St-Maurice--Laflèche",
        "province": "Quebec",
    },
    193324047: { # Trois-Rivières
        "name": "Three Rivers",
        "province": "Quebec",
    },
    193324059: { # Saint-Antoine--Westmount
        "name": "St. Antoine--Westmount",
        "province": "Quebec",
    },
    193324061: { # Saint-Henri
        "name": "St. Henry",
        "province": "Quebec",
    },
    ####################
    ### 1947 RIDINGS ###
    ####################
    194724035: { # Québec-Ouest
        "name": "Quebec West",
        "province": "Quebec",
    },
    194724064: { # Outremont--Saint-Jean
        "name": "Outremont--St-Jean",
        "province": "Quebec",
    },
    194724066: { # Sainte-Anne
        "name": "St. Ann",
        "province": "Quebec",
    },
    194724067: { # Saint-Antoine--Westmount
        "name": "St. Antoine--Westmount",
        "province": "Quebec",
    },
    194724068: { # Saint-Denis
        "name": "St-Denis",
        "province": "Quebec",
    },
    194724069: { # Saint-Henri
        "name": "St-Henri",
        "province": "Quebec",
    },
    194724070: { # Saint-Jacques
        "name": "St. James",
        "province": "Quebec",
    },
    194724071: { # Saint-Laurent--Saint-Georges
        "name": "St. Lawrence--St. George",
        "province": "Quebec",
    },
    194724072: { # Sainte-Marie
        "name": "St. Mary",
        "province": "Quebec",
    },
    194724073: { # Verdun--LaSalle
        "name": "Verdun--La Salle",
        "province": "Quebec",
    },
    ####################
    ### 1952 RIDINGS ###
    ####################
    195213004: { # Northumberland (N.B.)
        "name": "Northumberland--Miramichi",
        "province": "New Brunswick",
    },
    195224050: { # Témiscouata
        "name": "Rivière-du-Loup--Témiscouata",
        "province": "Quebec",
    },
    195224068: { # Sainte-Anne
        "name": "St. Ann",
        "province": "Quebec",
    },
    195224073: { # Saint-Laurent--Saint-Georges
        "name": "St. Lawrence--St. George",
        "province": "Quebec",
    },
    195259011: { # Nanaimo
        "name": "Nanaimo--Cowichan--The Islands",
        "province": "British Columbia",
    },
    195259013: { # Okanagan--Boundary
        "name": "Okanagan Boundary",
        "province": "British Columbia",
    },
    195259019: { # Vancouver--Kingsway
        "name": "Vancouver Kingsway",
        "province": "British Columbia",
    },
    195261001: { # Mackenzie River
        "name": "Northwest Territories",
        "province": "Northwest Territories",
    },
    ####################
    ### 1966 RIDINGS ###
    ####################
    196624009: { # Bourassa  TODO
        "name": "Montreal--Bourassa",
        "province": "Quebec",
    },
    196624029: { # Lafontaine
        "name": "Lafontaine--Rosemont",
        "province": "Quebec",
    },
    196624033: { # Lasalle
        "name": "Lasalle--Émard--Côte Saint-Paul",
        "province": "Quebec",
    },
    196624040: { # Maisonneuve  TODO
        "name": "Maisonneuve--Rosemont",
        "province": "Quebec",
    },
    196624068: { # Témiscouata
        "name": "Rivière-du-Loup--Témiscouata",
        "province": "Quebec",
    },
    196624070: { # Trois-Rivières
        "name": "Trois-Rivières Métropolitain",
        "province": "Quebec",
    },
    196635031: { # Lakeshore
        "name": "Toronto--Lakeshore",
        "province": "Ontario",
    },
    196635033: { # Lanark And Renfrew
        "name": "Lanark--Renfrew--Carleton",
        "province": "Ontario",
    },
    196635038: { # Middlesex
        "name": "Middlesex--London--Lambton",
        "province": "Ontario",
    },
    196635045: { # Oshawa--Whitby
        "name": "Oshawa",
        "province": "Ontario",
    },
    196635048: { # Ottawa East
        "name": "Ottawa--Vanier",
        "province": "Ontario",
    },
    196635053: { # Peel--Dufferin--Simcoe
        "name": "Peel--Dufferin",
        "province": "Ontario",
    },
    196635054: { # Peel South
        "name": "Mississauga",
        "province": "Ontario",
    },
    196635055: { # Perth
        "name": "Perth--Wilmot",
        "province": "Ontario",
    },
    196635059: { # Renfrew North
        "name": "Renfrew North--Nipissing East",
        "province": "Ontario",
    },
    196635061: { # Sarnia
        "name": "Sarnia--Lambton",
        "province": "Ontario",
    },
    196635076: {  # Waterloo
        "name": "Waterloo--Cambridge",
        "province": "Ontario",
    },
    196635079: {  # Wellington--Grey
        "name": "Wellington--Grey--Dufferin--Waterloo",
        "province": "Ontario",
    },
    196659017: { # Surrey
        "name": "Surrey--White Rock",
        "province": "British Columbia",
    },
    ####################
    ### 1976 RIDINGS ###
    ####################
    197624024: { # Sainte-Marie  TODO
        "name": "Montreal--Sainte Marie",
        "province": "Quebec",
    },
    197624041: { # Hochelaga--Maisonneuve  TODO
        "name": "Maisonneuve",
        "province": "Quebec",
    },
    197624044: { # Mercier  TODO
        "name": "Montreal--Mercier",
        "province": "Quebec",
    },
    197624045: { # Laval
        "name": "Mille-Iles",
        "province": "Quebec",
    },
    197624047: { # Montmorency
        "name": "Montmorency--Orléans",
        "province": "Quebec",
    },
    197624049: { # Notre-Dame-De-Grâce
        "name": "Notre-Dame-de-Grâce--Lachine East",
        "province": "Quebec",
    },
    197624056: { # Richmond
        "name": "Richmond--Wolfe",
        "province": "Quebec",
    },
    197624057: { # Rimouski
        "name": "Rimouski--Témiscouata",
        "province": "Quebec",
    },
    197624061: { # Saint-Hyacinthe
        "name": "Saint-Hyacinthe--Bagot",
        "province": "Quebec",
    },
    197624064: { # Saint-Léonard--Anjou
        "name": "Saint-Léonard",
        "province": "Quebec",
    },
    197624066: { # Saint-Michel
        "name": "Saint-Michel--Ahuntsic",
        "province": "Quebec",
    },
    197624074: { # Verdun
        "name": "Verdun--Saint-Paul",
        "province": "Quebec",
    },
    197635044: { # London--Middlesex
        "name": "Middlesex East",
        "province": "Ontario",
    },
    197635063: { # Prince Edward--Hastings
        "name": "Prince Edward",
        "province": "Ontario",
    },
    197635068: { # Sarnia
        "name": "Sarnia--Lambton",
        "province": "Ontario",
    },
    197659007: { # Prince George--Bulkley Valley  TODO
        "name": "Prince George--Bulkley Valley",
        "province": "British Columbia",
    },
    197659019: { # Prince George--Bulkley Valley  TODO
        "name": "Prince George--Peace River",
        "province": "British Columbia",
    },
    ####################
    ### 1987 RIDINGS ###
    ####################
    198710006: { # St. John's East (Est)
        "name": "St. John's East",
        "province": "Newfoundland and Labrador",
    },
    198710007: { # St. John's West (Ouest)
        "name": "St. John's West",
        "province": "Newfoundland and Labrador",
    },
    198724021: { # Laval-Est (East)
        "name": "Laval East",
        "province": "Quebec",
    },
    198724031: { # QuÃÂ©bec
        "name": "Québec",
        "province": "Quebec",
    },
    198724033: { # LaSalle-Ãâ°mard
        "name": "LaSalle--Émard",
        "province": "Quebec",
    },
    198724036: { # Laval-Ouest (West)
        "name": "Laval West",
        "province": "Quebec",
    },
    198724037: { # Laval-Centre (Center)
        "name": "Laval Centre",
        "province": "Quebec",
    },
    198724047: { # Mont-Royal (Mount Royal)
        "name": "Mount Royal",
        "province": "Quebec",
    },
    198724048: { # Notre-Dame-de-GrÃÂ¢ce
        "name": "Notre-Dame-de-Grâce",
        "province": "Quebec",
    },
    198724065: { # Saint-Laurent--Cartierville
        "name": "Saint-Laurent",
        "province": "Quebec",
    },
    198724066: { # Saint-LÃÂ©onard
        "name": "Saint-Léonard",
        "province": "Quebec",
    },
    198735046: { # Markham-Whitchurch-Stouffville
        "name": "Markham",
        "province": "Ontario",
    },
    198735047: { # Mississauga East (Est)
        "name": "Mississauga East",
        "province": "Ontario",
    },
    198735049: { # Mississauga West (Ouest)
        "name": "Mississauga West",
        "province": "Ontario",
    },
    198735059: { # Ottawa South (Sud)
        "name": "Ottawa South",
        "province": "Ontario",
    },
    198735068: { # Renfrew-Nipissing-Pembroke
        "name": "Renfrew",
        "province": "Ontario",
    },
    198735085: { # Timiskaming
        "name": "Timiskaming--French River",
        "province": "Ontario",
    },
    198735093: [  # Windsor-St. Clair (Sainte-Claire)
        {
            "name": "Windsor--St. Clair",
            "province": "Ontario",
        },
        {
            "name": "Windsor--Lake St. Clair",
            "province": "Ontario",
        },
    ],
    198746008: { # Selkirk-Red River
        "name": "Selkirk",
        "province": "Manitoba",
    },
    198746012: {  # Winnipeg South (Sud)
        "name": "Winnipeg South",
        "province": "Manitoba",
    },
    198746013: {  # Winnipeg South Centre (Sud-Centre)
        "name": "Winnipeg South Centre",
        "province": "Manitoba",
    },
    198747004: { # Prince Albert (Prince-Albert)-Churchill River
        "name": "Prince Albert--Churchill River",
        "province": "Saskatchewan",
    },
    198748022: { # St. Albert (St-Albert)
        "name": "St. Albert",
        "province": "Alberta",
    },
    198759013: { # Nanaimo (NanaÃ¯Â¿Â½mo)-Cowichan
        "name": "Nanaimo--Cowichan",
        "province": "British Columbia",
    },
    198759026: { # Surrey North (Nord)
        "name": "Surrey North",
        "province": "British Columbia",
    },
    198759027: { # Surrey-White Rock-South Langley
        "name": "Surrey--White Rock",
        "province": "British Columbia",
    },
    ####################
    ### 1996 RIDINGS ###
    ####################
    199612007: { # Pictou0AntigonishfGuysborough
        "name": "Pictou--Antigonish--Guysborough",
        "province": "Nova Scotia",
    },
    199612008: { # Sackville
        "name": "Sackville--Eastern Shore",
        "province": "Nova Scotia",
    },
    199612010: { # Sydney0Victoria
        "name": "Sydney--Victoria",
        "province": "Nova Scotia",
    },
    199612011: {  # West Nova/Ouest Nova
        "name": "West Nova",
        "province": "Nova Scotia",
    },
    199613006: { # Madawaska
        "name": "Madawaska--Restigouche",
        "province": "New Brunswick",
    },
    199613008: { # Moncton0RiverviewuDieppe
        "name": "Moncton--Riverview--Dieppe",
        "province": "New Brunswick",
    },
    199613010: { # Tobique0Mactaquac
        "name": "Tobique--Mactaquac",
        "province": "New Brunswick",
    },
    199624029: [ # Notre-Dame-de-GrrcedLachine
        {
            "name": "Notre-Dame-de-Grâce--Lachine",
            "province": "Quebec",
        },
        {
            "name": "Lachine--Notre-Dame-de-Grâce",
            "province": "Quebec",
        }
    ],
    199624038: { # L9vis-et-Chutes-de-la-Chaudi-re
        "name": "Lévis-et-Chutes-de-la-Chaudière",
        "province": "Quebec",
    },
    199624047: { # Papineau6Saint-Denis
        "name": "Papineau--Saint-Denis",
        "province": "Quebec",
    },
    199635043: { # London0Fanshawe
        "name": "London--Fanshawe",
        "province": "Ontario",
    },
    199635050: { # Nepean0Carleton
        "name": "Nepean--Carleton",
        "province": "Ontario",
    },
    199624052: { # Qu9bec-Est/Quebec East
        "name": "Québec East",
        "province": "Quebec",
    },
    199624055: { # Richmond4Arthabaska
        "name": "Richmond--Arthabaska",
        "province": "Quebec",
    },
    199624056: [ # Rimouski5Mitis
        {
            "name": "Rimouski--Mitis",
            "province": "Quebec",
        },
        {
            "name": "Rimouski",
            "province": "Quebec",
        }
    ],
    199624059: [ # T9miscamingue
        {
            "name": "Rouyn-Noranda--Témiscamingue",
            "province": "Quebec",
        },
        {
            "name": "Témiscamingue",
            "province": "Quebec",
        }
    ],
    199624060: [ # Rivi2re-des-Mille-ales
        {
            "name": "Rivière-des-Mille-Îles",
            "province": "Quebec",
        },
        {
            "name": "Saint-Eustache--Sainte-Thérèse",
            "province": "Quebec",
        }
    ],
    199624066: { # Saint-L6onard
        "name": "Saint-Léonard--Saint-Michel",
        "province": "Quebec",
    },
    199635042: { # London North Centre/London-Centre-Nord
        "name": "London--Adelaide",
        "province": "Ontario",
    },
    199635066: { # Perth5Middlesex
        "name": "Perth--Middlesex",
        "province": "Ontario",
    },
    199635068: { # Pickering  TODO
        "name": "Pickering--Ajax--Uxbridge",
        "province": "Ontario",
    },
    199624070: { # Terrebonne
        "name": "Terrebonne--Blainville",
        "province": "Quebec",
    },
    199624072: { # Vaudreuil
        "name": "Vaudreuil--Soulanges",
        "province": "Quebec",
    },
    199624073: { # Verch4res
        "name": "Verchères--Les Patriotes",
        "province": "Quebec",
    },
    199624074: { # Verdun0Saint-Henri
        "name": "Verdun--Saint-Henri",
        "province": "Quebec",
    },
    199624075: {  # Westmount
        "name": "Westmount--Ville-Marie",
        "province": "Quebec",
    },
    199635039: { # Lambton3KenttMiddlesex
        "name": "Lambton--Kent--Middlesex",
        "province": "Ontario",
    },
    199635078: { # Simcoe0Grey
        "name": "Simcoe--Grey",
        "province": "Ontario",
    },
    199635087: { # Thunder BaynSuperior North/Thunder BayOSuperior-Nord
        "name": "Thunder Bay--Superior North",
        "province": "Ontario",
    },
    199635088: { # TimiskamingnCochrane
        "name": "Timiskaming--Cochrane",
        "province": "Ontario",
    },
    199635089: { # Timmins8James Bay/TimminshBaie James
        "name": "Timmins--James Bay",
        "province": "Ontario",
    },
    199635090: { # Toronto CentreBRosedale /Toronto-CentreSRosedale
        "name": "Toronto Centre--Rosedale",
        "province": "Ontario",
    },
    199635092: [ # Vaughan9KingiAurora
        {
            "name": "Vaughan--King--Aurora",
            "province": "Ontario",
        },
        {
            "name": "Vaughan--Aurora",
            "province": "Ontario",
        },
    ],
    199635094: {  # Waterloo3Wellington
        "name": "Waterloo--Wellington",
        "province": "Ontario",
    },
    199635095: {  # Wentworth
        "name": "Wentworth--Burlington",
        "province": "Ontario",
    },
    199635096: {  # Whitby0Ajax
        "name": "Whitby--Ajax",
        "province": "Ontario",
    },
    199635098: {  # Windsor9St. Clair
        "name": "Windsor--St. Clair",
        "province": "Ontario",
    },
    199646008: { # Selkirk0Interlake
        "name": "Selkirk--Interlake",
        "province": "Manitoba",
    },
    199646005: { # Portage0Lisgar
        "name": "Portage--Lisgar",
        "province": "Manitoba",
    },
    199646009: {  # Winnipeg North Centre/Winnipeg-Centre-Nord
        "name": "Winnipeg North Centre",
        "province": "Manitoba",
    },
    199646010: {  # Winnipeg Centre/Winnipeg-Centre
        "name": "Winnipeg Centre",
        "province": "Manitoba",
    },
    199646013: [  # Winnipeg North St. Paul/Winnipeg-Nord-St. Paul
        {
            "name": "Winnipeg--St. Paul",
            "province": "Manitoba",
        },
        {
            "name": "Winnipeg North--St. Paul",
            "province": "Manitoba",
        },
    ],
    199646014: {  # Winnipeg3Transcona
        "name": "Winnipeg--Transcona",
        "province": "Manitoba",
    },
    199647007: [  # Regina0Qu'Appelle
        {
            "name": "Qu'Appelle",
            "province": "Saskatchewan",
        },
        {
            "name": "Regina--Qu'Appelle",
            "province": "Saskatchewan",
        },
    ],
    199647008: [ # Regina0LumsdenlLake Centre
        {
            "name": "Regina--Lumsden--Lake Centre",
            "province": "Saskatchewan",
        },
        {
            "name": "Regina--Arm River",
            "province": "Saskatchewan",
        }
    ],
    199659010: [ # Langley0Abbotsford
        {
            "name": "Langley--Abbotsford",
            "province": "British Columbia",
        },
        {
            "name": "Langley--Matsqui",
            "province": "British Columbia",
        }
    ],
    199659011: { # Nanaimo1Alberni
        "name": "Nanaimo--Alberni",
        "province": "British Columbia",
    },
    199659013: { # New WestminsternCoquitlamgBurnaby
        "name": "New Westminster--Coquitlam--Burnaby",
        "province": "British Columbia",
    },
    199659014: [ # Okanagan3Shuswap
        {
            "name": "Okanagan--Shuswap",
            "province": "British Columbia",
        },
        {
            "name": "North Okanagan--Shuswap",
            "province": "British Columbia",
        }
    ],
    199659016: { # Okanagan5Coquihalla
        "name": "Okanagan--Coquihalla",
        "province": "British Columbia",
    },
    199659017: { # Port MoodyoCoquitlamiPort Coquitlam
        "name": "Port Moody--Coquitlam--Port Coquitlam",
        "province": "British Columbia",
    },
    199659021: { # Saanich2Gulf Islands
        "name": "Saanich--Gulf Islands",
        "province": "British Columbia",
    },
    199659023: { # South Surrey White RockeLangley
        "name": "South Surrey--White Rock--Langley",
        "province": "British Columbia",
    },
    199659024: { # Surrey Central/Surrey-Centre
        "name": "Surrey Central",
        "province": "British Columbia",
    },
    199659028: { # Vancouver Island North/rle de Vancouver-Nord
        "name": "Vancouver Island North",
        "province": "British Columbia",
    },
    199659031: { # Vancouver SouthaBurnaby/Vancouver-SudeBurnaby
        "name": "Vancouver South--Burnaby",
        "province": "British Columbia",
    },
    199659033:  # Kootenay2BoundaryuOkanagan
    {
        "name": "West Kootenay--Okanagan",
        "province": "British Columbia",
    },
    199659034: {  # West VancouveraSunshine Coast
        "name": "West Vancouver--Sunshine Coast",
        "province": "British Columbia",
    },
    ####################
    ### 1999 RIDINGS ###
    ####################
    199912008: { # Sackville
        "name": "Sackville--Musquodoboit Valley--Eastern Shore",
        "province": "Nova Scotia",
    },
    199924040: { # Lotbini3re
        "name": "Lotbinière--L'Érable",
        "province": "Quebec",
    },
    199924056: { # Rimouski5Mitis
        "name": "Rimouski-Neigette-et-La Mitis",
        "province": "Quebec",
    },
    199924058: { # Rosemont
        "name": "Rosemont--Petite-Patrie",
        "province": "Quebec",
    },
    199924074: { # Verdun0Saint-Henri
        "name": "Verdun--Saint-Henri--Saint-Paul--Pointe Saint-Charles",
        "province": "Quebec",
    },
    199935008: { # Broadview
        "name": "Toronto--Danforth",
        "province": "Ontario",
    },
    199935025: { # Carleton4Gloucester
        "name": "Ottawa--Orléans",
        "province": "Ontario",
    },
    199635062: { # Ottawa WesteNepean/Ottawa-OuesteNepean
        "name": "Ottawa West--Nepean",
        "province": "Ontario",
    },
    199935083: { # Stormont2DundasmCharlottenburgh
        "name": "Stormont--Dundas--Charlottenburgh",
        "province": "Ontario",
    },
    199647009: { # Saskatoon
        "name": "Saskatoon--Rosetown",
        "province": "Saskatchewan",
    },
    199647010: { # Saskatoon
        "name": "Saskatoon--Rosetown--Biggar",
        "province": "Saskatchewan",
    },
    199947012: { # Wanuskewin
        "name": "Saskatoon--Wanuskewin",
        "province": "Saskatchewan",
    },
    #######################################################
    ### 2003 RIDINGS: No names given in the geo dataset ###
    #######################################################
    # ID <-> Name correlation was done with https://www12.statcan.gc.ca/census-recensement/2011/geo/pdf/CANMAP_E_NEW2003.pdf
    # Newfoundland and Labrador
    200310001: {"name": "Avalon", "province": "Newfoundland and Labrador"},
    200310002: [
        {"name": "Bonavista--Exploits", "province": "Newfoundland and Labrador"},
        {
            "name": "Bonavista--Gander--Grand Falls--Windsor",
            "province": "Newfoundland and Labrador",
        },
    ],
    200310003: {
        "name": "Humber--St. Barbe--Baie Verte",
        "province": "Newfoundland and Labrador",
    },
    200310004: {"name": "Labrador", "province": "Newfoundland and Labrador"},
    200310005: {
        "name": "Random--Burin--St. George's",
        "province": "Newfoundland and Labrador",
    },
    200310006: [
        {"name": "St. John's North", "province": "Newfoundland and Labrador"},
        {"name": "St. John's East", "province": "Newfoundland and Labrador"},
    ],
    200310007: [
        {"province": "Newfoundland and Labrador", "name": "St. John's South"},
        {
            "name": "St. John's South--Mount Pearl",
            "province": "Newfoundland and Labrador",
        },
    ],
    # Prince Edward Island
    200311001: {"name": "Cardigan", "province": "Prince Edward Island"},
    200311002: {"name": "Charlottetown", "province": "Prince Edward Island"},
    200311003: {"name": "Egmont", "province": "Prince Edward Island"},
    200311004: {"name": "Malpeque", "province": "Prince Edward Island"},
    # Nova Scotia
    200312001: {"name": "Cape Breton--Canso", "province": "Nova Scotia"},
    200312002: {"name": "Central Nova", "province": "Nova Scotia"},
    200312003: {"name": "Dartmouth--Cole Harbour", "province": "Nova Scotia"},
    200312004: {"name": "Halifax", "province": "Nova Scotia"},
    200312005: {"name": "Halifax West", "province": "Nova Scotia"},
    200312006: {"name": "Kings--Hants", "province": "Nova Scotia"},
    200312007: [
        {"name": "North Nova", "province": "Nova Scotia"},
        {
            "name": "Cumberland--Colchester--Musquodoboit Valley",
            "province": "Nova Scotia",
        },
    ],
    200312008: {"name": "Sackville--Eastern Shore", "province": "Nova Scotia"},
    200312009: {"name": "South Shore--St. Margaret's", "province": "Nova Scotia"},
    200312010: {"name": "Sydney--Victoria", "province": "Nova Scotia"},
    200312011: {"name": "West Nova", "province": "Nova Scotia"},
    # New Brunswick
    200313001: {"name": "Acadie--Bathurst", "province": "New Brunswick"},
    200313002: {"name": "Beauséjour", "province": "New Brunswick"},
    200313003: {"name": "Fredericton", "province": "New Brunswick"},
    200313004: [
        {"name": "Fundy", "province": "New Brunswick"},
        {"name": "Fundy Royal", "province": "New Brunswick"},
    ],
    200313005: {"name": "Madawaska--Restigouche", "province": "New Brunswick"},
    200313006: {"name": "Miramichi", "province": "New Brunswick"},
    200313007: {"name": "Moncton--Riverview--Dieppe", "province": "New Brunswick"},
    200313008: [
        {"name": "St. Croix--Belleisle", "province": "New Brunswick"},
        {"name": "New Brunswick Southwest", "province": "New Brunswick"},
    ],
    200313009: {"name": "Saint John", "province": "New Brunswick"},
    200313010: {"name": "Tobique--Mactaquac", "province": "New Brunswick"},
    # Quebec
    200324001: {"name": "Abitibi--Témiscamingue", "province": "Quebec"},
    200324002: {"name": "Ahuntsic", "province": "Quebec"},
    200324003: {"name": "Alfred-Pellan", "province": "Quebec"},
    200324004: [
        {"name": "Argenteuil--Mirabel", "province": "Quebec"},
        {"name": "Argenteuil--Papineau--Mirabel", "province": "Quebec"},
    ],
    200324005: {"name": "Beauce", "province": "Quebec"},
    200324006: {"name": "Beauharnois--Salaberry", "province": "Quebec"},
    200324007: [
        {"name": "Beauport", "province": "Quebec"},
        {"name": "Beauport--Limoilou", "province": "Quebec"},
    ],
    200324008: {"name": "Berthier--Maskinongé", "province": "Quebec"},
    200324009: {"name": "Bourassa", "province": "Quebec"},
    200324010: {"name": "Brome--Missisquoi", "province": "Quebec"},
    200324011: {"name": "Brossard--La Prairie", "province": "Quebec"},
    200324012: {"name": "Chambly--Borduas", "province": "Quebec"},
    200324013: [
        {"name": "Charlesbourg", "province": "Quebec"},
        {"name": "Charlesbourg--Haute-Saint-Charles", "province": "Quebec"},
    ],
    200324014: [
        {"name": "Montmorency--Charlevoix--Haute-Côte-Nord", "province": "Quebec"},
        {"name": "Charlevoix--Montmorency", "province": "Quebec"},
    ],
    200324015: {"name": "Châteauguay--Saint-Constant", "province": "Quebec"},
    200324016: {"name": "Chicoutimi--Le Fjord", "province": "Quebec"},
    200324017: {"name": "Compton--Stanstead", "province": "Quebec"},
    200324018: {"name": "Drummond", "province": "Quebec"},
    200324019: {"name": "Gaspésie--Îles-de-la-Madeleine", "province": "Quebec"},
    200324020: {"name": "Gatineau", "province": "Quebec"},
    200324021: {"name": "Hochelaga", "province": "Quebec"},
    200324022: {"name": "Honoré-Mercier", "province": "Quebec"},
    200324023: {"name": "Hull--Aylmer", "province": "Quebec"},
    200324024: {"name": "Jeanne-Le Ber", "province": "Quebec"},
    200324025: {"name": "Joliette", "province": "Quebec"},
    200324026: {"name": "Jonquière--Alma", "province": "Quebec"},
    200324027: {"name": "Lac-Saint-Louis", "province": "Quebec"},
    200324028: {"name": "La Pointe-de-l'Île", "province": "Quebec"},
    200324029: {"name": "LaSalle--Émard", "province": "Quebec"},
    200324030: {"name": "Laurentides--Labelle", "province": "Quebec"},
    200324031: [
        {"name": "Laurier", "province": "Quebec"},
        {"name": "Laurier--Sainte-Marie", "province": "Quebec"},
    ],
    200324032: {"name": "Laval", "province": "Quebec"},
    200324033: {"name": "Laval--Les Îles", "province": "Quebec"},
    200324034: {"name": "Lévis--Bellechasse", "province": "Quebec"},
    200324035: [
        {"name": "Longueuil", "province": "Quebec"},
        {"name": "Longueuil--Pierre-Boucher", "province": "Quebec"},
    ],
    200324036: {"name": "Lotbinière--Chutes-de-la-Chaudière", "province": "Quebec"},
    200324037: {"name": "Louis-Hébert", "province": "Quebec"},
    200324038: {"name": "Louis-Saint-Laurent", "province": "Quebec"},
    200324039: {"name": "Manicouagan", "province": "Quebec"},
    200324040: {"name": "Marc-Aurèle-Fortin", "province": "Quebec"},
    200324041: [
        {"name": "Matapédia--Matane", "province": "Quebec"},
        {"name": "Haute-Gaspésie--La Mitis--Matane--Matapédia", "province": "Quebec"},
    ],
    200324042: {"name": "Mégantic--L'Érable", "province": "Quebec"},
    200324043: {"name": "Montcalm", "province": "Quebec"},
    200324044: {"name": "Mount Royal", "province": "Quebec"},
    200324045: {"name": "Notre-Dame-de-Grâce--Lachine", "province": "Quebec"},
    200324046: [
        {"name": "Abitibi--Baie-James--Nunavik--Eeyou", "province": "Quebec"},
        {"name": "Nunavik--Eeyou", "province": "Quebec"},
    ],
    200324047: {"name": "Outremont", "province": "Quebec"},
    200324048: {"name": "Papineau", "province": "Quebec"},
    200324049: {"name": "Pierrefonds--Dollard", "province": "Quebec"},
    200324050: {"name": "Pontiac", "province": "Quebec"},
    200324051: [
        {"name": "Portneuf", "province": "Quebec"},
        {"name": "Portneuf--Jacques-Cartier", "province": "Quebec"},
    ],
    200324052: {"name": "Québec", "province": "Quebec"},
    200324053: {"name": "Repentigny", "province": "Quebec"},
    200324054: [
        {"name": "Bas-Richelieu--Nicolet--Bécancour", "province": "Quebec"},
        {"name": "Richelieu", "province": "Quebec"},
    ],
    200324055: {"name": "Richmond--Arthabaska", "province": "Quebec"},
    200324056: [
        {"name": "Rimouski--Témiscouata", "province": "Quebec"},
        {"name": "Rimouski-Neigette--Témiscouata--Les Basques", "province": "Quebec"},
    ],
    200324057: {"name": "Rivière-des-Mille-Îles", "province": "Quebec"},
    200324058: [
        {
            "name": "Montmagny--L’Islet--Kamouraska--Rivière-du-Loup",
            "province": "Quebec",
        },
        {"name": "Rivière-du-Loup--Montmagny", "province": "Quebec"},
    ],
    200324059: {"name": "Rivière-du-Nord", "province": "Quebec"},
    200324060: [
        {"name": "Roberval", "province": "Quebec"},
        {"name": "Roberval--Lac-Saint-Jean", "province": "Quebec"},
    ],
    200324061: {"name": "Rosemont--La Petite-Patrie", "province": "Quebec"},
    200324062: {"name": "Saint-Bruno--Saint-Hubert", "province": "Quebec"},
    200324063: {"name": "Saint-Hyacinthe--Bagot", "province": "Quebec"},
    200324064: {"name": "Saint-Jean", "province": "Quebec"},
    200324065: {"name": "Saint-Lambert", "province": "Quebec"},
    200324066: {"name": "Saint-Laurent--Cartierville", "province": "Quebec"},
    200324067: {"name": "Saint-Léonard--Saint-Michel", "province": "Quebec"},
    200324068: {"name": "Saint-Maurice--Champlain", "province": "Quebec"},
    200324069: {"name": "Shefford", "province": "Quebec"},
    200324070: {"name": "Sherbrooke", "province": "Quebec"},
    200324071: {"name": "Terrebonne--Blainville", "province": "Quebec"},
    200324072: {"name": "Trois-Rivières", "province": "Quebec"},
    200324073: {"name": "Vaudreuil--Soulanges", "province": "Quebec"},
    200324074: {"name": "Verchères--Les Patriotes", "province": "Quebec"},
    200324075: {"name": "Westmount--Ville-Marie", "province": "Quebec"},
    # Ontario
    200335001: {"name": "Ajax--Pickering", "province": "Ontario"},
    200335002: {"name": "Algoma--Manitoulin--Kapuskasing", "province": "Ontario"},
    200335003: {
        "name": "Ancaster--Dundas--Flamborough--Westdale",
        "province": "Ontario",
    },
    200335004: {"name": "Barrie", "province": "Ontario"},
    200335005: {"name": "Beaches--East York", "province": "Ontario"},
    200335006: {"name": "Bramalea--Gore--Malton", "province": "Ontario"},
    200335007: {"name": "Brampton--Springdale", "province": "Ontario"},
    200335008: {"name": "Brampton West", "province": "Ontario"},
    200335009: {"name": "Brant", "province": "Ontario"},
    200335010: {"name": "Burlington", "province": "Ontario"},
    200335011: {"name": "Cambridge", "province": "Ontario"},
    200335012: [
        {"name": "Carleton--Lanark", "province": "Ontario"},
        {"name": "Carleton--Mississippi Mills", "province": "Ontario"},
    ],
    200335013: {"name": "Chatham-Kent--Essex", "province": "Ontario"},
    200335014: [
        {"name": "Clarington--Scugog--Uxbridge", "province": "Ontario"},
        {"name": "Durham", "province": "Ontario"},
    ],
    200335015: {"name": "Davenport", "province": "Ontario"},
    200335016: {"name": "Don Valley East", "province": "Ontario"},
    200335017: {"name": "Don Valley West", "province": "Ontario"},
    200335018: {"name": "Dufferin--Caledon", "province": "Ontario"},
    200335019: {"name": "Eglinton--Lawrence", "province": "Ontario"},
    200335020: {"name": "Elgin--Middlesex--London", "province": "Ontario"},
    200335021: {"name": "Essex", "province": "Ontario"},
    200335022: {"name": "Etobicoke Centre", "province": "Ontario"},
    200335023: {"name": "Etobicoke--Lakeshore", "province": "Ontario"},
    200335024: {"name": "Etobicoke North", "province": "Ontario"},
    200335025: {"name": "Glengarry--Prescott--Russell", "province": "Ontario"},
    200335026: [
        {"name": "Grey--Bruce--Owen Sound", "province": "Ontario"},
        {"name": "Bruce--Grey--Owen Sound", "province": "Ontario"},
    ],
    200335027: {"name": "Guelph", "province": "Ontario"},
    200335028: {"name": "Haldimand--Norfolk", "province": "Ontario"},
    200335029: {"name": "Haliburton--Kawartha Lakes--Brock", "province": "Ontario"},
    200335030: {"name": "Halton", "province": "Ontario"},
    200335031: {"name": "Hamilton Centre", "province": "Ontario"},
    200335032: {"name": "Hamilton East--Stoney Creek", "province": "Ontario"},
    200335033: {"name": "Hamilton Mountain", "province": "Ontario"},
    200335034: {"name": "Huron--Bruce", "province": "Ontario"},
    200335035: {"name": "Kenora", "province": "Ontario"},
    200335036: {"name": "Kingston and the Islands", "province": "Ontario"},
    200335037: {"name": "Kitchener Centre", "province": "Ontario"},
    200335038: [
        # Renamed from "Kitchener--Conestoga" to "Kitchener--Wilmot--Wellesley--Woolwich" then back again.
        {"name": "Kitchener--Wilmot--Wellesley--Woolwich", "province": "Ontario"},
        {"name": "Kitchener--Conestoga", "province": "Ontario"},
    ],
    200335039: {"name": "Kitchener--Waterloo", "province": "Ontario"},
    200335040: {
        "name": "Lanark--Frontenac--Lennox and Addington",
        "province": "Ontario",
    },
    200335041: {"name": "Leeds--Grenville", "province": "Ontario"},
    200335042: {"name": "London--Fanshawe", "province": "Ontario"},
    200335043: {"name": "London North Centre", "province": "Ontario"},
    200335044: {"name": "London West", "province": "Ontario"},
    200335045: {"name": "Markham--Unionville", "province": "Ontario"},
    200335046: [
        {"name": "Middlesex--Kent--Lambton", "province": "Ontario"},
        {"name": "Lambton--Kent--Middlesex", "province": "Ontario"},
    ],
    200335047: {"name": "Mississauga--Brampton South", "province": "Ontario"},
    200335048: {"name": "Mississauga East--Cooksville", "province": "Ontario"},
    200335049: {"name": "Mississauga--Erindale", "province": "Ontario"},
    200335050: {"name": "Mississauga South", "province": "Ontario"},
    200335051: {"name": "Mississauga--Streetsville", "province": "Ontario"},
    200335052: {"name": "Nepean--Carleton", "province": "Ontario"},
    200335053: {"name": "Newmarket--Aurora", "province": "Ontario"},
    200335054: {"name": "Niagara Falls", "province": "Ontario"},
    200335055: {"name": "Niagara West--Glanbrook", "province": "Ontario"},
    200335056: {"name": "Nickel Belt", "province": "Ontario"},
    200335057: {"name": "Nipissing--Timiskaming", "province": "Ontario"},
    200335058: {"name": "Northumberland--Quinte West", "province": "Ontario"},
    200335059: {"name": "Oak Ridges--Markham", "province": "Ontario"},
    200335060: {"name": "Oakville", "province": "Ontario"},
    200335061: {"name": "Oshawa", "province": "Ontario"},
    200335062: {"name": "Ottawa Centre", "province": "Ontario"},
    200335063: {"name": "Ottawa--Orléans", "province": "Ontario"},
    200335064: {"name": "Ottawa South", "province": "Ontario"},
    200335065: {"name": "Ottawa--Vanier", "province": "Ontario"},
    200335066: {"name": "Ottawa West--Nepean", "province": "Ontario"},
    200335067: {"name": "Oxford", "province": "Ontario"},
    200335068: {"name": "Parkdale--High Park", "province": "Ontario"},
    200335069: {"name": "Parry Sound--Muskoka", "province": "Ontario"},
    200335070: {"name": "Perth--Wellington", "province": "Ontario"},
    200335071: {"name": "Peterborough", "province": "Ontario"},
    200335072: {"name": "Pickering--Scarborough East", "province": "Ontario"},
    200335073: {"name": "Prince Edward--Hastings", "province": "Ontario"},
    200335074: {"name": "Renfrew--Nipissing--Pembroke", "province": "Ontario"},
    200335075: {"name": "Richmond Hill", "province": "Ontario"},
    200335076: {"name": "St. Catharines", "province": "Ontario"},
    200335077: {"name": "St. Paul's", "province": "Ontario"},
    200335078: {"name": "Sarnia--Lambton", "province": "Ontario"},
    200335079: {"name": "Sault Ste. Marie", "province": "Ontario"},
    200335080: {"name": "Scarborough--Agincourt", "province": "Ontario"},
    200335081: {"name": "Scarborough Centre", "province": "Ontario"},
    200335082: {"name": "Scarborough--Guildwood", "province": "Ontario"},
    200335083: {"name": "Scarborough--Rouge River", "province": "Ontario"},
    200335084: {"name": "Scarborough Southwest", "province": "Ontario"},
    200335085: {"name": "Simcoe--Grey", "province": "Ontario"},
    200335086: {"name": "Simcoe North", "province": "Ontario"},
    200335087: {"name": "Stormont--Dundas--South Glengarry", "province": "Ontario"},
    200335088: {"name": "Sudbury", "province": "Ontario"},
    200335089: {"name": "Thornhill", "province": "Ontario"},
    200335090: {"name": "Thunder Bay--Rainy River", "province": "Ontario"},
    200335091: {"name": "Thunder Bay--Superior North", "province": "Ontario"},
    200335092: {"name": "Timmins--James Bay", "province": "Ontario"},
    200335093: {"name": "Toronto Centre", "province": "Ontario"},
    200335094: {"name": "Toronto--Danforth", "province": "Ontario"},
    200335095: {"name": "Trinity--Spadina", "province": "Ontario"},
    200335096: {"name": "Vaughan", "province": "Ontario"},
    200335097: {"name": "Welland", "province": "Ontario"},
    200335098: {"name": "Wellington--Halton Hills", "province": "Ontario"},
    200335099: {"name": "Whitby--Oshawa", "province": "Ontario"},
    200335100: {"name": "Willowdale", "province": "Ontario"},
    200335101: {"name": "Windsor--Tecumseh", "province": "Ontario"},
    200335102: {"name": "Windsor West", "province": "Ontario"},
    200335103: {"name": "York Centre", "province": "Ontario"},
    200335104: {"name": "York--Simcoe", "province": "Ontario"},
    200335105: {"name": "York South--Weston", "province": "Ontario"},
    200335106: {"name": "York West", "province": "Ontario"},
    # Manitoba
    200346001: {"name": "Brandon--Souris", "province": "Manitoba"},
    200346002: [
        {"name": "Charleswood--St. James", "province": "Manitoba"},
        {"name": "Charleswood--St. James--Assiniboia", "province": "Manitoba"},
    ],
    200346003: {"name": "Churchill", "province": "Manitoba"},
    200346004: [
        {"name": "Dauphin--Swan River", "province": "Manitoba"},
        {"name": "Dauphin--Swan River--Marquette", "province": "Manitoba"},
    ],
    200346005: {"name": "Elmwood--Transcona", "province": "Manitoba"},
    200346006: {"name": "Kildonan--St. Paul", "province": "Manitoba"},
    200346007: {"name": "Portage--Lisgar", "province": "Manitoba"},
    200346008: {"name": "Provencher", "province": "Manitoba"},
    200346009: {"name": "Saint Boniface", "province": "Manitoba"},
    200346010: {"name": "Selkirk--Interlake", "province": "Manitoba"},
    200346011: {"name": "Winnipeg Centre", "province": "Manitoba"},
    200346012: {"name": "Winnipeg North", "province": "Manitoba"},
    200346013: {"name": "Winnipeg South", "province": "Manitoba"},
    200346014: {"name": "Winnipeg South Centre", "province": "Manitoba"},
    # Saskatchewan
    200347001: {"name": "Battlefords--Lloydminster", "province": "Saskatchewan"},
    200347002: {"name": "Blackstrap", "province": "Saskatchewan"},
    200347003: [
        {"name": "Churchill River", "province": "Saskatchewan"},
        {"name": "Desnethé--Missinippi--Churchill River", "province": "Saskatchewan"},
    ],
    200347004: {"name": "Cypress Hills--Grasslands", "province": "Saskatchewan"},
    200347005: {"name": "Palliser", "province": "Saskatchewan"},
    200347006: {"name": "Prince Albert", "province": "Saskatchewan"},
    200347007: {"name": "Regina--Lumsden--Lake Centre", "province": "Saskatchewan"},
    200347008: {"name": "Regina--Qu'Appelle", "province": "Saskatchewan"},
    200347009: {"name": "Saskatoon--Humboldt", "province": "Saskatchewan"},
    200347010: {"name": "Saskatoon--Rosetown--Biggar", "province": "Saskatchewan"},
    200347011: {"name": "Saskatoon--Wanuskewin", "province": "Saskatchewan"},
    200347012: {"name": "Souris--Moose Mountain", "province": "Saskatchewan"},
    200347013: {"name": "Wascana", "province": "Saskatchewan"},
    200347014: {"name": "Yorkton--Melville", "province": "Saskatchewan"},
    # Alberta
    200348001: [
        {"name": "Athabasca", "province": "Alberta"},
        {"name": "Fort McMurray--Athabasca", "province": "Alberta"},
    ],
    200348002: {"name": "Calgary East", "province": "Alberta"},
    200348003: [
        {"name": "Calgary North Centre", "province": "Alberta"},
        {"name": "Calgary Centre-North", "province": "Alberta"},
    ],
    200348004: {"name": "Calgary Northeast", "province": "Alberta"},
    200348005: {"name": "Calgary--Nose Hill", "province": "Alberta"},
    200348006: [
        {"name": "Calgary South Centre", "province": "Alberta"},
        {"name": "Calgary Centre", "province": "Alberta"},
    ],
    200348007: {"name": "Calgary Southeast", "province": "Alberta"},
    200348008: {"name": "Calgary Southwest", "province": "Alberta"},
    200348009: {"name": "Calgary West", "province": "Alberta"},
    200348010: {"name": "Crowfoot", "province": "Alberta"},
    200348011: [
        {"name": "Edmonton--Mill Woods--Beaumont", "province": "Alberta"},
        {"name": "Edmonton--Beaumont", "province": "Alberta"},
    ],
    200348012: {"name": "Edmonton Centre", "province": "Alberta"},
    200348013: {"name": "Edmonton East", "province": "Alberta"},
    200348014: {"name": "Edmonton--Leduc", "province": "Alberta"},
    200348015: {"name": "Edmonton--St. Albert", "province": "Alberta"},
    200348016: {"name": "Edmonton--Sherwood Park", "province": "Alberta"},
    200348017: {"name": "Edmonton--Spruce Grove", "province": "Alberta"},
    200348018: {"name": "Edmonton--Strathcona", "province": "Alberta"},
    200348019: {"name": "Lethbridge", "province": "Alberta"},
    200348020: {"name": "Macleod", "province": "Alberta"},
    200348021: {"name": "Medicine Hat", "province": "Alberta"},
    200348022: {"name": "Peace River", "province": "Alberta"},
    200348023: {"name": "Red Deer", "province": "Alberta"},
    200348024: {"name": "Vegreville--Wainwright", "province": "Alberta"},
    200348025: [
        # Renamed from "Westlock--St. Paul" to "Battle River" then back again.
        {"name": "Battle River", "province": "Alberta"},
        {"name": "Westlock--St. Paul", "province": "Alberta"},
    ],
    200348026: {"name": "Wetaskiwin", "province": "Alberta"},
    200348027: {"name": "Wild Rose", "province": "Alberta"},
    200348028: {"name": "Yellowhead", "province": "Alberta"},
    # British Columbia
    200359001: {"name": "Abbotsford", "province": "British Columbia"},
    200359002: {"name": "Burnaby--Douglas", "province": "British Columbia"},
    200359003: {"name": "Burnaby--New Westminster", "province": "British Columbia"},
    200359004: {"name": "Cariboo--Prince George", "province": "British Columbia"},
    200359005: {"name": "Chilliwack--Fraser Canyon", "province": "British Columbia"},
    200359006: {"name": "Delta--Richmond East", "province": "British Columbia"},
    200359007: [
        {"name": "Dewdney--Alouette", "province": "British Columbia"},
        {"name": "Pitt Meadows--Maple Ridge--Mission", "province": "British Columbia"},
    ],
    200359008: {"name": "Esquimalt--Juan de Fuca", "province": "British Columbia"},
    200359009: {"name": "Fleetwood--Port Kells", "province": "British Columbia"},
    200359010: [
        {"name": "Kamloops--Thompson", "province": "British Columbia"},
        {"name": "Kamloops--Thompson--Cariboo", "province": "British Columbia"},
    ],
    200359011: [
        {"name": "Kelowna", "province": "British Columbia"},
        {"name": "Kelowna--Lake Country", "province": "British Columbia"},
    ],
    200359012: {"name": "Kootenay--Columbia", "province": "British Columbia"},
    200359013: {"name": "Langley", "province": "British Columbia"},
    200359014: {"name": "Nanaimo--Alberni", "province": "British Columbia"},
    200359015: {"name": "Nanaimo--Cowichan", "province": "British Columbia"},
    200359016: {"name": "Newton--North Delta", "province": "British Columbia"},
    200359017: {"name": "New Westminster--Coquitlam", "province": "British Columbia"},
    200359018: {"name": "Okanagan--Shuswap", "province": "British Columbia"},
    200359018: [
        {"name": "North Okanagan--Shuswap", "province": "British Columbia"},
        {"name": "Okanagan--Shuswap", "province": "British Columbia"},
    ],
    200359019: {"name": "North Vancouver", "province": "British Columbia"},
    200359020: {"name": "Okanagan--Coquihalla", "province": "British Columbia"},
    200359021: {
        "name": "Port Moody--Westwood--Port Coquitlam",
        "province": "British Columbia",
    },
    200359022: {"name": "Prince George--Peace River", "province": "British Columbia"},
    200359023: {"name": "Richmond", "province": "British Columbia"},
    200359024: {"name": "Saanich--Gulf Islands", "province": "British Columbia"},
    200359025: {"name": "Skeena--Bulkley Valley", "province": "British Columbia"},
    200359026: [
        {"name": "Southern Interior", "province": "British Columbia"},
        {"name": "British Colombia Southern Interior", "province": "British Columbia"},
    ],
    200359027: {
        "name": "South Surrey--White Rock--Cloverdale",
        "province": "British Columbia",
    },
    200359028: {"name": "Surrey North", "province": "British Columbia"},
    200359029: {"name": "Vancouver Centre", "province": "British Columbia"},
    200359030: {"name": "Vancouver East", "province": "British Columbia"},
    200359031: {"name": "Vancouver Island North", "province": "British Columbia"},
    200359032: {"name": "Vancouver Kingsway", "province": "British Columbia"},
    200359033: {"name": "Vancouver Quadra", "province": "British Columbia"},
    200359034: {"name": "Vancouver South", "province": "British Columbia"},
    200359035: {"name": "Victoria", "province": "British Columbia"},
    200359036: [
        {"name": "West Vancouver--Sunshine Coast", "province": "British Columbia"},
        {
            "name": "West Vancouver--Sunshine Coast--Sea to Sky Country",
            "province": "British Columbia",
        },
    ],
    # Territories
    200360001: {"name": "Yukon", "province": "Yukon"},
    200361001: {"name": "Northwest Territories", "province": "Northwest Territories"},
    200362001: {"name": "Nunavut", "province": "Nunavut"},
    ####################
    ### 2013 RIDINGS ###
    ####################
    201324013: { # Th�r�se-De Blainville
        "name": "Thérèse-De Blainville",
        "province": "Quebec",
    },
    201324014: { # Pierre-Boucher--Les Patriotes--Verch�res
        "name": "Pierre-Boucher--Les Patriotes--Verchères",
        "province": "Quebec",
    },
    201324018: { # Rimouski-Neigette--T�miscouata--Les Basques
        "name": "Rimouski-Neigette--Témiscouata--Les Basques",
        "province": "Quebec",
    },
    201324037: [ # LaSalle--�mard--Verdun
        {
            "name": "LaSalle--Émard--Verdun",
            "province": "Quebec",
        },
        {
            "name": "LaSalle--Verdun",
            "province": "Quebec",
        },
    ],
    201324041: [ # Longueuil--Charles-LeMoyne
        {
            "name": "Longueuil",
            "province": "Quebec",
        },
        {
            "name": "Lemoyne",
            "province": "Quebec",
        },
    ],
    201324042: { # L�vis--Lotbini�re
        "name": "Lévis--Lotbinière",
        "province": "Quebec",
    },
    201324053: { # Notre-Dame-de-Gr�ce--Westmount
        "name": "Notre-Dame-de-Grâce--Westmount",
        "province": "Quebec",
    },
    201324065: { # Marc-Aur�le-Fortin
        "name": "Marc-Aurèle-Fortin",
        "province": "Quebec",
    },
    201324071: { # Salaberry--Suro�t
        "name": "Salaberry--Suroît",
        "province": "Quebec",
    },
    201324074: { # Vaudreuil--Soulanges
        "name": "Soulanges--Vaudreuil",
        "province": "Quebec",
    },
    201324077: [  # Ville-Marie--Le Sud-Ouest--�le-des-Soeurs
        {
            "name": "Ville-Marie--Le Sud-Ouest--Île-des-Soeurs",
            "province": "Quebec",
        },
        {
            "name": "Ville-Marie",
            "province": "Quebec",
        },
    ],
    201335049: { # Lanark--Frontenac--Kingston
        "name": "Lanark--Frontenac",
        "province": "Ontario",
    },
    201335059: { # Mississauga East--Cooksville
        "name": "Mississauga--Cooksville",
        "province": "Ontario",
    },
    201335071: { # Northumberland--Peterborough South
        "name": "Northumberland--Pine Ridge",
        "province": "Ontario",
    },
    201335076: { # Orl�ans
        "name": "Orléans",
        "province": "Ontario",
    },
    201335088: { # Carleton
        "name": "Rideau--Carleton",
        "province": "Ontario",
    },
    201335090: { # Toronto--St. Paul's
        "name": "St. Paul's",
        "province": "Ontario",
    },
    201348030: { # Red Deer--Lacombe
        "name": "Red Deer--Wolf Creek",
        "province": "Alberta",
    },
    201359026: { # Esquimalt--Saanich--Sooke
        "name": "Saanich--Esquimalt--Juan de Fuca",
        "province": "British Columbia",
    },
    201359037: { # North Island--Powell River
        "name": "Vancouver Island North--Comox--Powell River",
        "province": "British Columbia",
    },
}


def get_cached_xlsx(xlsx_path, json_path):
    if not json_path.exists():
        rows = []
        workbook = openpyxl.load_workbook(xlsx_path)
        sheet = workbook.active

        for row in sheet.iter_rows(min_row=2, values_only=True):
            rows.append(row)

        if not json_path.parent.exists():
            json_path.parent.mkdir(parents=True, exist_ok=True)

        with open(json_path, "w") as f:
            json.dump(rows, f, indent=4)

    with open(json_path) as f:
        return json.load(f)


def build():
    ARTIFACT_DIR.mkdir(exist_ok=True)

    geometry_dir = SOURCES_DIR / "geometry/fedshapes_cbf_20221003"
    riding_years = sorted([int(f.stem[6:10]) for f in geometry_dir.glob("*.shp")])
    ridings = {year: [] for year in riding_years}

    debug_geo_ridings = []
    for year in riding_years:
        print(year)
        gdf = geopandas.read_file(
            SOURCES_DIR / f"geometry/fedshapes_cbf_20221003/CBF_RO{year}_CSRS.shp",
            engine="pyogrio",
        )

        for _, row in gdf.iterrows():
            if year in [1867, 1872]:
                _, _, name, id, _, notes, geometry = row.tolist()
            elif year in [1882]:
                _, _, name, id, notes, _, _, _, geometry = row.tolist()
            elif year in [1892, 1903, 1914, 1924, 1933, 1947, 1952, 1966, 1976]:
                _, _, name, id, _, geometry = row.tolist()
            elif year in [1905]:
                name, _, _, _, id, geometry = row.tolist()
            elif year in [1987]:
                _, id, _, _, name, geometry = row.tolist()
            elif year in [1996]:
                _, name, id, _, _, geometry = row.tolist()
            elif year in [1999]:
                _, name, _, id, _, geometry = row.tolist()
            elif year in [2003]:
                _, id, _, _, geometry = row.tolist()
                name = None
            elif year in [2013]:
                _, name, _, id, _, geometry = row.tolist()
            else:
                raise RuntimeError(f"Unhandled year: {year}")

            simple_geometry = geometry.simplify(1000, preserve_topology=False)
            svg = simple_geometry.svg()
            xml_svg = xml.etree.ElementTree.fromstring(svg)
            for attr_key in ["fill", "stroke", "stroke-width", "opacity"]:
                xml_svg.attrib.pop(attr_key, None)
                for child in xml_svg:
                    child.attrib.pop(attr_key, None)
            final_svg = xml.etree.ElementTree.tostring(xml_svg).decode("utf-8")

            ridings[year].append({"name": name, "id": id, "geometry": final_svg})
            debug_geo_ridings.append(
                {"name": name, "id": id, "year": year, "copy": f"{id}: {{ # {name}"}
            )

    election_and_candidate_rows = get_cached_xlsx(
        SOURCES_DIR / "electionsCandidates.xlsx", CACHE_DIR / "electionsCandidates.json"
    )
    riding_rows = get_cached_xlsx(
        SOURCES_DIR / "ridings/ParlInfoRidings1.xlsx", CACHE_DIR / f"ridings.json"
    )

    data = {
        Parliament: [],
        Election: [],
        Party: set(),
        Riding: [],
        Candidate: set(),
        Run: [],
    }

    with open(ARTIFACT_DIR / "debug_geo_ridings.json", "w") as f:
        json.dump(debug_geo_ridings, f, indent=4, ensure_ascii=False)

    print("Processing ridings")
    count = 0
    debug_2003_ec = []
    for row in riding_rows:
        name, province, region, start_date, end_date, status = row
        if start_date == "":
            start_date_obj = None
        else:
            start_year, start_month, start_day = start_date.split("-")
            start_date_obj = datetime.date(
                int(start_year), int(start_month), int(start_day)
            )

        # According to EC these ridings started on May 1st, 1871.
        # But these elections were held on March 2nd and 3rd, 1871!
        # https://en.wikipedia.org/wiki/Lisgar_(electoral_district)
        # https://en.wikipedia.org/wiki/Provencher
        if (name, start_date_obj) == ("Lisgar", datetime.date(1871, 5, 1)):
            start_date_obj = datetime.date(1871, 3, 2)
        elif (name, start_date_obj) == ("Marquette", datetime.date(1871, 5, 1)):
            start_date_obj = datetime.date(1871, 3, 2)
        elif (name, start_date_obj) == ("Selkirk", datetime.date(1871, 5, 1)):
            start_date_obj = datetime.date(1871, 3, 2)
        elif (name, start_date_obj) == ("Provencher", datetime.date(1871, 5, 1)):
            start_date_obj = datetime.date(1871, 3, 3)  # This one was a day late?

        if end_date == "":
            end_date_obj = None
        else:
            end_year, end_month, end_day = end_date.split("-")
            end_date_obj = datetime.date(int(end_year), int(end_month), int(end_day))

        if start_date_obj < datetime.date(2013, 1, 1) and (
            end_date_obj is None or end_date_obj > datetime.date(2004, 5, 22)
        ):
            debug_2003_ec.append(
                {
                    "name": name,
                    "province": province,
                    "start_date": start_date,
                    "end_date": end_date,
                }
            )

        most_recent_year = min(ridings.keys())
        for year in ridings.keys():
            if 0 <= start_date_obj.year - year < most_recent_year:
                most_recent_year = year

        geometry = None
        is_duplicate = (
            len([r for r in ridings[most_recent_year] if r["name"] == name]) > 1
        )
        for riding in ridings[most_recent_year]:
            if not is_duplicate and riding["name"] and (
                riding["name"].lower() == name.lower() or \
                riding["name"] == name.replace("--", "-") or \
                riding["name"].split("/")[0] == name
            ):
                geometry = riding["geometry"]
                break

            manual_match = GEO_ID_TO_EC_RIDINGS.get(int(riding["id"]))
            if manual_match is None:
                continue

            if not isinstance(manual_match, list):
                manual_match = [manual_match]

            for match in manual_match:
                if match["name"] == name and match["province"] == province:
                    geometry = riding["geometry"]
                    break

        if geometry is None:
            if name in ("Saskatchewan", "Saskatchewan (Provisional District)"):
                continue
            count += 1
            print(
                f"{name: <50} {province: <25} {start_date} - {end_date if end_date else 'active'}"
            )

        province_enum = Province.from_name(province)
        data[Riding].append(
            Riding(name, province_enum, geometry, start_date_obj, end_date_obj)
        )

    with open(ARTIFACT_DIR / "debug_2003_ec.json", "w") as f:
        json.dump(debug_2003_ec, f, indent=4, ensure_ascii=False)
    print(f"\n{count} unassigned ridings")
    exit()
    print("Processing runs")
    for row in election_and_candidate_rows:
        (
            picture_or_heading,
            province,
            riding,
            candidate,
            gender,
            occupation,
            party,
            result,
            votes,
        ) = row

        if picture_or_heading.startswith("Parliament: "):
            parliament = int(picture_or_heading[12:])
            data[Parliament].append(Parliament(parliament))

        elif picture_or_heading.startswith("Type of Election: "):
            election_type_str = picture_or_heading.split(": ")[1]
            election_type = {
                "By-Election": ElectionType.BYELECTION,
                "General": ElectionType.GENERAL,
            }[election_type_str]

        elif picture_or_heading.startswith("Date of Election: "):
            date = picture_or_heading[18:]
            year, month, day = date.split("-")
            date = datetime.date(int(year), int(month), int(day))
            data[Election].append(Election(date, election_type, data[Parliament][-1]))

        elif picture_or_heading == "":
            party = Party(party, PARTY_COLORS.get(party, None))
            data[Party].add(party)

            split_name = candidate.split(", ")
            last = split_name[0]
            first = "".join(split_name[1:])
            candidate = Candidate(first, last, gender, occupation)
            data[Candidate].add(candidate)

            if (date, riding) == (datetime.date(2004, 6, 28), "Laurier--Sainte-Marie"):
                # https://en.wikipedia.org/wiki/Laurier%E2%80%94Sainte-Marie
                # Laurier—Sainte-Marie was abolished in 2003, then redistributed into Laurier and Holcheaga,
                # then Laurier was renamed to Laurier—Sainte-Marie in 2004 *after* the election.
                riding = "Laurier"
            elif (date, riding) == (
                datetime.date(2004, 6, 28),
                "Rimouski-Neigette--Témiscouata--Les Basques",
            ):
                # https://en.wikipedia.org/wiki/Rimouski-Neigette%E2%80%94T%C3%A9miscouata%E2%80%94Les_Basques
                # This riding was created as Rimouski--Témiscouata in 2003 and only renamed *after* the 2004 election.
                riding = "Rimouski--Témiscouata"

            matching_ridings = [
                r
                for r in data[Riding]
                if r.name == riding
                and r.province == Province.from_name(province)
                and date >= r.start_date
                and (r.end_date is None or date < r.end_date)
            ]

            assert len(matching_ridings) == 1

            run = Run(
                data[Election][-1],
                matching_ridings[0],
                candidate,
                party,
                ElectionResult.from_string(result),
                int(votes),
            )
            data[Run].append(run)

            for election in data[Election]:
                if election.date == date:
                    election.runs.append(run.id())
                    break

        else:
            raise RuntimeError(f"Bad row: {row}")

    print("Writing JSON files")
    for cls, instances in data.items():
        obj = {}
        for instance in instances:
            obj[instance.id()] = instance.to_json()
        json_file = ARTIFACT_DIR / f"{cls.__name__.lower()}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=4, ensure_ascii=False)
