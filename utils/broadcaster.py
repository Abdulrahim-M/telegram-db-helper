from collections import defaultdict
import asyncio

_listeners = defaultdict(list)

def subscribe(event_name: str, callback):
    """Register a function to listen for an event."""
    _listeners[event_name].append(callback)

async def broadcast(event_name: str, *args, **kwargs):
    print("Broadcast triggered")
    """Trigger all listeners for an event."""
    if event_name not in _listeners:
        print("Event name not in list. canceled broadcasting")
        return
    for cb in _listeners[event_name]:
        # Support both async and sync listeners
        if asyncio.iscoroutinefunction(cb):
            print("Broadcasted async")
            await cb(*args, **kwargs)
        else:
            print("Broadcasted")
            cb(*args, **kwargs)