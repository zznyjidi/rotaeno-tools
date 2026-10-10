import csv
import json
from typing import TypeAlias

from parser import parser, rating

JSON: TypeAlias = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None

Levels = ['I', 'II', 'III', 'IV', 'IV_Alpha']


def calculate_song_ratings(scores: dict, constant: dict[str, tuple[str, dict[str, float]]]) -> dict[str, dict[str, float]]:
    return {
        song: {
            level: rating.cap_failed(result[0] + constant[song][1][level], info['IsCleared'])
            for level, info in score['levels'].items()
            if (result := rating.score_to_rating_offset(info['Score']))[1] and level in Levels
        }
        for song, score in scores.items()
    }


def split_and_filter_song_ratings(song_ratings: dict[str, dict[str, float]], deprecated: list[str]) -> list[tuple[str, float, str]]:
    entries = []
    for song, score in song_ratings.items():
        if song in deprecated:
            continue
        if ('IV' in score) or ('IV_Alpha' in score):
            IVs = {
                'IV_Alpha': score.get('IV_Alpha', 0.0),
                'IV': score.get('IV', 0.0)
            }
            entry = max(IVs, key=IVs.get)
            entries.append((song, score[entry], entry))
        entries.extend(
            (song, value, entry)
            for entry, value in score.items()
            if entry not in ['IV', 'IV_Alpha']
        )
    return entries


def float_or_zero(x: str) -> float:
    try:
        return float(x)
    except ValueError:
        return 0.0


if __name__ == '__main__':
    with open('rotaeno-save.json', 'r') as save_file:
        save: JSON = json.load(save_file)

    with open('constant.csv', 'r', encoding='utf-8') as constant_file:
        reader = csv.reader(constant_file)
        constant = {
            row[0]: (row[1], dict(zip(Levels, list(map(float_or_zero, row[2:]))))) 
            for row in reader
        }

    with open('deprecated.csv', 'r', encoding='utf-8') as deprecated_file:
        reader = csv.reader(deprecated_file)
        deprecated = [row[0] for row in reader]

    scores = parser.extract_scores(parser.api_responds_to_data(save))

    song_ratings = calculate_song_ratings(scores, constant)
    song_rating_entries = split_and_filter_song_ratings(song_ratings, deprecated)

    song_rating_entries.sort(key=lambda x: x[1], reverse=True)

    player_rating = rating.chart_rating_to_player_rating([x[1] for x in song_rating_entries])
    print(f'Rating: {player_rating}')

    for index, (song, song_rating, level) in enumerate(song_rating_entries):
        if index in [10, 20, 40]:
            print('----------')
        print(f'{song:35} {constant[song][1][level]:4.1f} {level:10} {song_rating:10.05f}/{constant[song][1][level] + 3.6:<4.1f}  {scores[song]['levels'][level]['Score']:8}   {constant[song][0]:35}')
