"""
Глобальні фікстури для pytest.
Містить загальні моки (імітації) для обходу залежності від графіки та аудіо Pygame під час тестування.
"""

import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_registry():
    """
    Створює фейковий registry, доступний для всіх тестів.
    Імітує екран, звуки та спрайти, щоб не залежати від pygame.
    """
    registry = MagicMock()

    # Мокуємо surface (екран)
    mock_surface = MagicMock()
    mock_surface.get_width.return_value = 800
    mock_surface.get_height.return_value = 600

    # Мокуємо спрайти та звуки
    mock_sprites = MagicMock()
    mock_sound = MagicMock()

    # Налаштовуємо registry.get(), щоб він повертав наші моки
    def get_side_effect(key):
        items = {
            'surface': mock_surface,
            'sprites': mock_sprites,
            'rsprites': mock_sprites,
            'soundHandler': mock_sound,
            'round': 1
        }
        return items.get(key, MagicMock())

    registry.get.side_effect = get_side_effect
    return registry