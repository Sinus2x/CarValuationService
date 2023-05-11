import reverse_geocode


def get_city(lat, long):
    data = reverse_geocode.search([(lat, long)])
    try:
        return data[0]['city']
    except KeyError:
        return 'Unknown'