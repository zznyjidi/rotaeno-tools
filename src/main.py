import csv
import json
from typing import TypeAlias

from parser import parser, rating

JSON: TypeAlias = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None

Levels = ['I', 'II', 'III', 'IV', 'IV_Alpha']

with open('rotaeno-save.json', 'r') as save_file:
    save: JSON = json.load(save_file)

scores = parser.extract_scores(parser.api_responds_to_data(save))

def float_or_zero(x: str) -> float:
    try:
        return float(x)
    except ValueError:
        return 0.0

with open('constant.csv', 'r', encoding='utf-8') as constant_file:
    reader = csv.reader(constant_file)
    constant = {row[0]: (row[1], dict(zip(Levels, list(map(float_or_zero ,row[2:]))))) for row in reader}


offsets = {
    song: {
        level: rating.cap_failed(result[0] + constant[song][1][level], info['IsCleared'])
        for level, info in score['levels'].items() 
        if (result := rating.score_to_rating_offset(info['Score']))[1] and level in Levels
    }
    for song, score in scores.items()
    }

for song, score in offsets.items():
    if score:
        print(f'{song:35} {score}')
