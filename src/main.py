import json
from typing import TypeAlias

from parser import parser, rating

JSON: TypeAlias = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None


with open('rotaeno-save.json', 'r') as save_file:
    save: JSON = json.load(save_file)

scores = parser.extract_scores(parser.api_responds_to_data(save))

#print(scores)

offsets = {
    song: {
        level: (result[0], info['IsCleared'])
        for level, info in score['levels'].items() 
        if (result := rating.score_to_rating_offset(info['Score']))[1]
    }
    for song, score in scores.items()
    }

for song, score in offsets.items():
    if score:
        print(f'{song:35} {score}')
