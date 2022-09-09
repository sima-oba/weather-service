from dataclasses import is_dataclass, asdict


def export_feature_collection(data: list, geometry_key: str) -> dict:
    features = []
    feature_collection = {
        'type': 'FeatureCollection',
        'features': features
    }

    for index, feat in enumerate(data):
        if is_dataclass(feat):
            feat = asdict(feat)

        geometry = feat.pop(geometry_key, None)
        properties = {key: value for key, value in feat.items()}
        features.append({
            'id': index,
            'type': 'Feature',
            'properties': properties,
            'geometry': geometry,
        })

    return feature_collection
