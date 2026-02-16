import pytest
from unittest.mock import MagicMock
import DuckHunt.src.duckhunt.entities.duck as duck_module

# Маркуємо всі тести в цьому файлі як 'mechanics'
pytestmark = pytest.mark.mechanics

class TestDuck:

    def test_duck_movement(self, mock_registry):
        """Перевірити, що качка змінює координати при оновленні."""
        # Важливо: ініціалізуємо глобальні змінні модуля (FRAME_SIZE і т.д.)
        duck_module.init() 

        duck = duck_module.Duck(mock_registry)
        start_x, start_y = duck.position
        
        # Примусово задаємо швидкість, щоб качка точно рухалася
        duck.dx = 5
        duck.dy = 0
        
        # Оновлюємо стан качки
        duck.update(dt=1)
        
        new_x, new_y = duck.position
        # Перевіряємо, що вона не стоїть на місці
        assert (new_x != start_x) or (new_y != start_y)

    def test_duck_hit(self, mock_registry):
        """Перевірити, що метод isShot повертає True при влучанні."""
        duck_module.init()

        duck = duck_module.Duck(mock_registry)
        # Ставимо качку в конкретну точку
        duck.position = (100, 100)
        
        # "Стріляємо" трохи правіше і нижче від лівого верхнього кута качки
        # (розмір качки 81x75, тому 110x110 - це влучання)
        hit_pos = (110, 110)
        
        assert duck.isShot(hit_pos) is True
        assert duck.isDead is True  # Качка має померти

    def test_duck_miss(self, mock_registry):
        """Перевірити, що метод isShot повертає False при промаху."""
        duck_module.init()
        
        duck = duck_module.Duck(mock_registry)
        duck.position = (100, 100)
        
        # "Стріляємо" далеко від качки
        miss_pos = (500, 500) 
        
        assert duck.isShot(miss_pos) is False
        assert duck.isDead is False  # Качка має жит