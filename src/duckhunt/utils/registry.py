"""
Модуль для управління глобальними налаштуваннями екрану та реєстром ресурсів гри.
Містить функції для масштабування графіки та клас Registry.
"""

from duckhunt.core.settings import ORIG_W, ORIG_H

RENDER_W, RENDER_H = ORIG_W, ORIG_H


def init_screen_params(width, height):
    """Ініціалізує глобальні параметри ширини та висоти екрану для подальшого масштабування."""

    global RENDER_W, RENDER_H
    RENDER_W = width
    RENDER_H = height


def adjwidth(x):
    """Масштабує координату X або ширину відносно оригінального розміру екрану."""

    return (RENDER_W * x) // ORIG_W


def adjheight(y):
    """Масштабує координату Y або висоту відносно оригінального розміру екрану."""

    return (RENDER_H * y) // ORIG_H


def adjpos(x, y):
    """Масштабує координати (X, Y) у вигляді кортежу."""

    return (adjwidth(x), adjheight(y))


def adjrect(a, b, c, d):
    """Масштабує прямокутник (x, y, width, height) у вигляді кортежу."""

    return (adjwidth(a), adjheight(b), adjwidth(c), adjheight(d))


class Registry(object):
    """
    Клас-реєстр для зберігання та доступу до глобальних об'єктів гри (поверхня, обробник звуків, рахунок).
    Реалізує патерн Service Locator.
    """

    def __init__(self):
        """Ініціалізує порожній словник для зберігання даних."""

        self.registry = {}

    def set(self, key, value):
        """Зберігає об'єкт у реєстрі за вказаним ключем та повертає сам реєстр (для ланцюгових викликів)."""

        self.registry[key] = value
        return self

    def get(self, key):
        """Отримує об'єкт з реєстру за ключем. Повертає None, якщо ключ не знайдено."""
        if key in self.registry:
            return self.registry[key]
        return None
