"""
Модульні тести для ігрової сутності Gun (зброя).
Перевіряє логіку стрільби, витрати патронів та перезарядки.
"""

import pytest
from unittest.mock import MagicMock, patch
from duckhunt.entities.gun import Gun
from duckhunt.core import settings

# Маркуємо всі тести в цьому файлі як 'mechanics'
pytestmark = pytest.mark.mechanics


class TestGun:
    """Набір тестів для перевірки механіки рушниці гравця."""

    def test_gun_shoot_decrements_ammo(self, mock_registry):
        """Перевірити, що постріл зменшує кількість патронів."""
        # Патчимо pygame всередині модуля gun
        with patch('duckhunt.entities.gun.pygame') as mock_pygame:

            # Налаштовуємо мок для картинки прицілу
            mock_img = MagicMock()
            mock_img.get_size.return_value = (50, 50)
            mock_pygame.image.load.return_value = mock_img
            mock_pygame.transform.scale.return_value = mock_img

            gun = Gun(mock_registry)
            initial_rounds = gun.rounds

            # Стріляємо
            gun.shoot()

            # Перевіряємо, що патронів стало менше
            assert gun.rounds == initial_rounds - 1

    def test_gun_no_ammo(self, mock_registry):
        """Перевірити, що не можна стріляти без патронів."""

        with patch('duckhunt.entities.gun.pygame') as mock_pygame:
            mock_img = MagicMock()
            mock_img.get_size.return_value = (50, 50)
            mock_pygame.image.load.return_value = mock_img
            mock_pygame.transform.scale.return_value = mock_img

            gun = Gun(mock_registry)
            gun.rounds = 0  # Забираємо патрони

            result = gun.shoot()

            assert result is False  # Постріл не відбувся
            assert gun.rounds == 0  # Патрони не пішли в мінус

    def test_gun_reload(self, mock_registry):
        """Перевірити, що перезарядка відновлює патрони."""

        with patch('duckhunt.entities.gun.pygame') as mock_pygame:
            mock_img = MagicMock()
            mock_img.get_size.return_value = (50, 50)
            mock_pygame.image.load.return_value = mock_img
            mock_pygame.transform.scale.return_value = mock_img

            gun = Gun(mock_registry)
            gun.rounds = 0

            gun.reloadIt()

            assert gun.rounds == settings.GUN_ROUNDS
