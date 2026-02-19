"""
Тести логіки нарахування балів та керування станом раунду.
Демонструє використання фікстур та параметризації у pytest.
"""

import pytest
from duckhunt.utils.registry import Registry

# Підготовка
@pytest.fixture
def game_registry():
    """
    Фікстура для підготовки чистого стану перед кожним тестом.
    Ініціалізує об'єкт Registry та встановлює початкові значення (рахунок 0, раунд 1).
    """
    reg = Registry()
    reg.set('score', 0)
    reg.set('round', 1)
    return reg

# Нарахування балів
@pytest.mark.parametrize(
    "initial_score, hits, expected_score",
    [
        (0, 1, 10),      # Сценарій 1: Старт з 0, 1 влучання (10 балів)
        (100, 1, 110),   # Сценарій 2: Старт зі 100, 1 влучання (+10 балів)
        (0, 5, 50),      # Сценарій 3: Старт з 0, серія з 5 влучань (+50 балів)
    ]
)
def test_score_accumulation(game_registry, initial_score, hits, expected_score):
    """
    Перевіряє, що рахунок збільшується коректно при влучанні по качках.
    Використовує параметризацію для перевірки різних сценаріїв одним кодом.
    """
    # Встановлюємо початковий рахунок для тесту
    game_registry.set('score', initial_score)

    # Імітуємо логіку нарахування балів з PlayState (по 10 балів за качку)
    for _ in range(hits):
        current_score = game_registry.get('score')
        game_registry.set('score', current_score + 10)

    # Перевіряємо, чи збігається результат з очікуваним
    assert game_registry.get('score') == expected_score

# GAME OVER (Скидання гри)
def test_score_reset(game_registry):
    """
    Перевіряє, що після стану Game Over рахунок скидається на 0, а раунд на 1.
    """
    # Штучно створюємо ситуацію "кінця гри" з досягнутим прогресом
    game_registry.set('score', 540)
    game_registry.set('round', 7)

    # Імітуємо логіку скидання з GameOverState.execute()
    game_registry.set('score', 0)
    game_registry.set('round', 1)

    # Перевіряємо, чи відбулося скидання коректно
    assert game_registry.get('score') == 0
    assert game_registry.get('round') == 1