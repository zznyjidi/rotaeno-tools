
def api_responds_to_data(responds) -> dict:
    return responds['results'][0]['cloudSave']['data']['data']

def extract_scores(data: dict) -> dict:
    return data['songs']['songs']
