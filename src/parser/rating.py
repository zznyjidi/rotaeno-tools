
def score_to_rating_offset(score: int) -> tuple[float, bool]:
    match score:
        case s if s < 500_000:
            return 0, False
        case 1_010_000:
            return 3.6, True
        case s if s >= 1_008_000:
            base_offset = 3.4
            base_score = 1_008_000
            score_interval = 10_000
        case s if s >= 1_004_000:
            base_offset = 2.4
            base_score = 1_004_000
            score_interval = 4_000
        case s if s >= 1_000_000:
            base_offset = 2
            base_score = 1_000_000
            score_interval = 10_000
        case s if s >= 980_000:
            base_offset = 1
            base_score = 980_000
            score_interval = 20_000
        case s if s >= 950_000:
            base_offset = 0
            base_score = 950_000
            score_interval = 30_000
        case s if s >= 900_000:
            base_offset = -1
            base_score = 900_000
            score_interval = 50_000
        case s if s >= 500_000:
            base_offset = -5
            base_score = 500_000
            score_interval = 100_000
        case _:
            return 0, False
    
    return base_offset + ((score - base_score) / score_interval), True

def cap_failed(chart_rating: float, passed: bool) -> float:
    return chart_rating if passed else min(chart_rating, 6.0)

def chart_rating_to_player_rating(sorted_chart_ratings: list) -> float:
    b10 = sorted_chart_ratings[0:10]
    b11_20 = sorted_chart_ratings[10:20]
    b21_40 = sorted_chart_ratings[20:40]
    return (sum(b10)/10) * 0.6 + (sum(b11_20)/10) * 0.2 + (sum(b21_40)/20) * 0.2
