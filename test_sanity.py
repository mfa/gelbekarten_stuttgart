import pytest

from main import gen_datetime_obj, load_previous_data, merge, parse


@pytest.fixture
def example_contents():
    # preserving relevant content and whitespacing
    return """<!DOCTYPE html><html lang="de" class="h-100"><head></head><body class="d-flex flex-column h-100"><main role="main" class="flex-shrink-0 mb-3">
    <div class="container"> <h3>Die 40 letzten Meldungen </h3> <div id="currentincidentsmap" class="mt-3 mb-4 card"></div>
    <div id="currentincidents" hidden="hidden">
            <ul>
                                                                                                                                                                                                                                                        <li                                     location=M&#x00E4;hdachstra&#x00DF;e&#x20;20
     latitude=48.822148851204
     longitude=9.1156669035262
    >Straßenbeleuchtung</li>
                                                                                                                                                                                                                                                            <li                                     location=Erligheimer&#x20;Stra&#x00DF;e&#x20;8
     latitude=48.832369698078
     longitude=9.1866819544789
    >Sonstiges</li>
                                                                                                                                                                                                                                                                                             </ul>
        </div>
    </div>
</main>
</body>
</html>
"""


def test_parse(example_contents):
    incidents = list(parse(example_contents))
    assert incidents[0] == {
        "category": "Straßenbeleuchtung",
        "lat": "48.822148851204",
        "location": "Mähdachstraße 20",
        "lon": "9.1156669035262",
    }


def test_merge_current_previous(example_contents):
    incidents = list(parse(example_contents))
    previous_incidents = list(load_previous_data())
    new_incidents = merge(previous_incidents[:40], incidents)
    assert len(list(new_incidents)) == 2


def test_merge_all_duplicate(example_contents):
    incidents = list(parse(example_contents))
    previous_incidents = incidents
    new_incidents = merge(previous_incidents[:40], incidents)
    assert len(list(new_incidents)) == 0


def test_gen_datetime_obj():
    import datetime

    datetime_obj = gen_datetime_obj(datetime.datetime(2020, 12, 28, 9, 0, 0, 1234))
    assert datetime_obj == {
        "first_seen_at_timestamp": "2020-12-28T09:00:00",
        "first_seen_date": "2020-12-28",
        "first_seen_hour": 9,
        "first_seen_weekday": 1,
    }
