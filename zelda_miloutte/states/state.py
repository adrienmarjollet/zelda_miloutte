from abc import ABC, abstractmethod


class State(ABC):
    def __init__(self, game):
        self.game = game

    def enter(self):
        pass

    def exit(self):
        pass

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def draw(self, surface):
        pass

    def handle_event(self, event):
        pass
