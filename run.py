import argparse
import pygame

from duckhunt.core import settings
from duckhunt.utils.registry import init_screen_params
from duckhunt.core import states
from duckhunt.entities import duck
from duckhunt.app import Game

if __name__ == "__main__":
    TITLE = "Duck Hunt"

    # Init pygame params
    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.init()
    pygame.display.set_caption(TITLE)
    pygame.mouse.set_visible(False)

    parser = argparse.ArgumentParser(description="Duck Hunt Game")
    parser.add_argument('--width', type=int, default=800, help='Screen width')
    parser.add_argument('--height', type=int, default=500, help='Screen height')
    parser.add_argument('--volume', type=float, default=1.0, help='Master volume')
    parser.add_argument('--difficulty', type=int, default=1, help='Difficulty level')
    parser.add_argument('--fps', type=int, default=60, help='Frames Per Second (default: 60)')

    args = parser.parse_args()

    # Global inits
    init_screen_params(args.width, args.height)
    states.init()
    duck.init()

    settings.GLOBAL_VOLUME = max(0.0, min(1.0, args.volume))
    settings.FRAMES_PER_SEC = args.fps

    speed_boost = (args.difficulty - 1) * 2
    settings.DUCK_SPEED_MIN += speed_boost
    settings.DUCK_SPEED_MAX += speed_boost

    theGame = Game(args.width, args.height)
    theGame.execute()