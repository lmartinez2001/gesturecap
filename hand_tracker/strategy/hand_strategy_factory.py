from .hand_strategies import HandStrategy, LeftHandStrategy, RightHandStrategy


class HandStrategyFactory:
    @staticmethod
    def create_strategy(hand: str, config) -> HandStrategy:
        if hand == 'Right':
            return RightHandStrategy(config)
        elif hand == 'Left':
            return LeftHandStrategy(config)
        else:
            raise ValueError(f"Unknown hand: {hand}")
