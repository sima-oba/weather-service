from dataclasses import dataclass

from .entity import Entity


@dataclass
class City(Entity):
    geoid: int
    name: str
    state: str


CITIES = [
    {
        'geoid': '2901403',
        'name': 'Angical',
        'state': 'BA'
    },
    {
        'geoid': '2902500',
        'name': 'Baianópolis',
        'state': 'BA'
    },
    {
        'geoid': '2903201',
        'name': 'Barreiras',
        'state': 'BA'
    },
    {
        'geoid': '2904407',
        'name': 'Brejolândia',
        'state': 'BA'
    },
    {
        'geoid': '2906105',
        'name': 'Canápolis',
        'state': 'BA'
    },
    {
        'geoid': '2907400',
        'name': 'Catolândia',
        'state': 'BA'
    },
    {
        'geoid': '2908101',
        'name': 'Cocos',
        'state': 'BA'
    },
    {
        'geoid': '2909109',
        'name': 'Coribe',
        'state': 'BA'
    },
    {
        'geoid': '2909307',
        'name': 'Correntina',
        'state': 'BA'
    },
    {
        'geoid': '2909406',
        'name': 'Cotegipe',
        'state': 'BA'
    },
    {
        'geoid': '2909703',
        'name': 'Cristópolis',
        'state': 'BA'
    },
    {
        'geoid': '2911105',
        'name': 'Formosa do Rio Preto',
        'state': 'BA'
    },
    {
        'geoid': '2917359',
        'name': 'Jaborandi',
        'state': 'BA'
    },
    {
        'geoid': '2919553',
        'name': 'Luís Eduardo Magalhães',
        'state': 'BA'
    },
    {
        'geoid': '2920452',
        'name': 'Mansidão',
        'state': 'BA'
    },
    {
        'geoid': '2926202',
        'name': 'Riachão das Neves',
        'state': 'BA'
    },
    {
        'geoid': '2928109',
        'name': 'Santa Maria da Vitória',
        'state': 'BA'
    },
    {
        'geoid': '2928208',
        'name': 'Santana',
        'state': 'BA'
    },
    {
        'geoid': '2928406',
        'name': 'Santa Rita de Cássia',
        'state': 'BA'
    },
    {
        'geoid': '2928901',
        'name': 'São Desidério',
        'state': 'BA'
    },
    {
        'geoid': '2929057',
        'name': 'São Félix do Coribe',
        'state': 'BA'
    },
    {
        'geoid': '2930303',
        'name': 'Serra Dourada',
        'state': 'BA'
    },
    {
        'geoid': '2930907',
        'name': 'Tabocas do Brejo Velho',
        'state': 'BA'
    },
    {
        'geoid': '2933455',
        'name': 'Wanderley',
        'state': 'BA'
    }
]
