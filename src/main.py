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
    constant = {row[0]: (row[1], dict(zip(Levels, list(map(float_or_zero, row[2:]))))) for row in reader}

ratings = {
    song: {
        level: rating.cap_failed(result[0] + constant[song][1][level], info['IsCleared'])
        for level, info in score['levels'].items() 
        if (result := rating.score_to_rating_offset(info['Score']))[1] and level in Levels
    }
    for song, score in scores.items()
    }

splitted_effective_rating_entry = []
for song, score in ratings.items():
    if ('IV' in score) or ('IV_Alpha' in score):
        IVs = {
            'IV_Alpha': score.get('IV_Alpha', 0.0),
            'IV': score.get('IV', 0.0)
        }
        entry = max(IVs, key=IVs.get)
        splitted_effective_rating_entry.append((song, score[entry], entry))
    splitted_effective_rating_entry.extend(
        (song, value, entry)
        for entry, value in score.items()
        if entry not in ['IV', 'IV_Alpha']
    )

splitted_effective_rating_entry.sort(key=lambda x: x[1], reverse=True)

print(f'Rating: {rating.chart_rating_to_player_rating([x[1] for x in splitted_effective_rating_entry])}')

for index, (song, song_rating, level) in enumerate(splitted_effective_rating_entry):
    if index in [10, 20, 40]:
        print('----------')
    print(f'{song:35} {constant[song][1][level]:4.1f} {level:10} {song_rating:10.05f}/{constant[song][1][level] + 3.6:<4.1f}  {scores[song]['levels'][level]['Score']:8}   {constant[song][0]:35}')
