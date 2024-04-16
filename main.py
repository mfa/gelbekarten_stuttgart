import csv
import datetime

from bs4 import BeautifulSoup


def parse(contents):
    soup = BeautifulSoup(contents, "lxml")
    for incident in soup.find("div", id="currentincidents").find_all("li"):
        yield {
            "category": incident.text,
            "location": incident.attrs.get("location"),
            "lat": incident.attrs.get("latitude"),
            "lon": incident.attrs.get("longitude"),
        }


def load_previous_data(filename="data/gelbe_karten_stuttgart.csv"):
    with open(filename) as f:
        yield from csv.DictReader(f)


def merge(previous_incidents, incidents):
    _previous_incidents = [
        # remove datetime fields
        {k: v for k, v in item.items() if k in incidents[0].keys()}
        for item in previous_incidents
    ]
    for incident in incidents:
        if incident not in _previous_incidents:
            yield incident


def gen_datetime_obj(freeze=None):
    dt = freeze or datetime.datetime.utcnow()
    return {
        "first_seen_at_timestamp": dt.isoformat().split(".")[0],
        "first_seen_date": dt.date().isoformat(),
        "first_seen_weekday": dt.date().isoweekday(),
        "first_seen_hour": dt.hour,
    }


def write_data(previous_incidents, new_incidents, datetime_obj):
    with open("data/gelbe_karten_stuttgart.csv", "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=previous_incidents[0].keys())
        writer.writeheader()
        for incident in previous_incidents:
            writer.writerow(incident)
        for incident in new_incidents:
            incident.update(datetime_obj)
            writer.writerow(incident)
    print(f"{len(list(new_incidents))} incidents added.")


def main():
    datetime_obj = gen_datetime_obj()

    previous_incidents = list(load_previous_data())
    with open("incidents.html") as fp:
        new_incidents = merge(previous_incidents[-40:], list(parse(fp.read())))

    write_data(previous_incidents, new_incidents, datetime_obj)


if __name__ == "__main__":
    main()
