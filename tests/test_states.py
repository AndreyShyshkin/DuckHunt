"""
Тести для машини станів (State Machine) гри.
Перевіряє логіку переходу між станами (зокрема, умови перемоги та поразки).
"""

import pytest
from unittest.mock import MagicMock
from duckhunt.core import states
from duckhunt.core.states import RoundEndState
from duckhunt.utils.registry import Registry


@pytest.fixture
def mock_env():
    """Створює Registry та мокає (імітує) звуковий обробник."""
    reg = Registry()
    mock_sound = MagicMock()
    reg.set('soundHandler', mock_sound)
    states.registry = reg
    return reg, mock_sound


def test_round_end_game_over(mock_env):
    """Перевіряє логіку програшу (>= 4 промахи)."""
    _, mock_sound = mock_env
    hit_ducks = [False, False, False, False, True, True, True, True, True, True]

    state = RoundEndState(hit_ducks)

    assert state.isGameOver is True
    mock_sound.enqueue.assert_called_once_with('gameover')


def test_round_end_next_round(mock_env):
    """Перевіряє логіку переходу до наступного раунду (< 4 промахів)."""
    _, mock_sound = mock_env
    hit_ducks = [True] * 10  # 10 влучань, 0 промахів

    state = RoundEndState(hit_ducks)

    assert state.isGameOver is False
    mock_sound.enqueue.assert_called_once_with('nextround')
