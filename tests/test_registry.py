import pytest
from duckhunt.utils.registry import Registry

@pytest.mark.core
def test_registry_basics():
    """Перевіряє базові функції збереження та отримання даних з реєстру."""
    reg = Registry()
    reg.set('player_name', 'Oleg')

    assert reg.get('player_name') == 'Oleg'
    assert reg.get('non_existent_key') is None

@pytest.mark.skip(reason="Демонстрація маркера skip.")
def test_dummy_graphics():
    """Цей тест не буде виконуватися, але відобразиться у звіті як пропущений."""
    assert False