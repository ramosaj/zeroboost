import pytest
from unnamed_backend.src.replay_aggregator import ReplayAggregator
import numbers
import datetime
from freezegun import freeze_time


def test_init(): 
    replay = ReplayAggregator('steam','1234')
    assert(replay.platform) == 'steam'
    assert(replay.player_id) == '1234'


@pytest.mark.vcr
def test_parse_replay(): 
    replay = ReplayAggregator('steam','76561198353975600')
    replay_obj = replay.parse_replay('4e68ba50-8933-4ece-98dd-17e77e334dae')
    assert(isinstance(replay_obj['bpm'],numbers.Number))
    assert(isinstance(replay_obj['date'],str))
    assert(isinstance(replay_obj['shooting_percentage'],numbers.Number))


@freeze_time("2023-2-1")
@pytest.mark.vcr
def test_get_replays():
    replay = ReplayAggregator('steam','76561198353975600')
    aggregated_replay = replay.get_replays(count=5,n_months=2)
    assert(len(aggregated_replay['bpm']) > 0)
    assert(len(aggregated_replay['shooting_percentage']) > 0)



    