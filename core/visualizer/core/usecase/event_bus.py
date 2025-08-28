from typing import Callable, List, Dict, Any


class EventBus:

    __slots__ = ["__subscribers"]

    def __init__(self) -> None:
        self.__subscribers: Dict[str, List[Callable[[Any], None]]] = {}

    def subscribe(self, event: str, callback: Callable[[Any], None]) -> None:
        self.__subscribers.setdefault(event, []).append(callback)

    def emit(self, event: str, data: Any) -> None:
        for callback in self.__subscribers.get(event, []):
            callback(data)

    def unsubscribe(self, event: str, callback: Callable[[Any], None]) -> None:
        if event in self.__subscribers:
            self.__subscribers[event] = [fn for fn in self.__subscribers[event] if fn != callback]