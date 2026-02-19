import pytest
from duckhunt.utils.registry import Registry, adjwidth

@pytest.mark.core
def test_registry_basics():
    reg = Registry()
    reg.set('player_name', 'Oleg')
    assert reg.get('player_name') == 'Oleg'
    assert reg.get('non_existent_key') is None

@pytest.mark.skip(reason="Демонстрація маркера skip.")
def test_dummy_graphics():
    assert False

@pytest.mark.parametrize(
    "original_width, expected_width",
    [
        (100, 100),
        (256, 256),
        (0, 0)
    ]
)
def test_adjwidth_scaling(original_width, expected_width):
    """Перевіряє математику функції масштабування екрана."""
    result = adjwidth(original_width)
    assert result == expected_width