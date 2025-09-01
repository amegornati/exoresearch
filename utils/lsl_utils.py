"""
Lightweight helpers for LabStreamingLayer (LSL).
Works with pylsl that exposes resolve_streams().
"""
from pylsl import StreamInfo, StreamOutlet, StreamInlet, resolve_streams
import time

def make_marker_outlet(name="markers", type_="Markers", channel_format="string"):
    info = StreamInfo(name, type_, 1, 0, channel_format, "marker_stream_001")
    outlet = StreamOutlet(info)
    return outlet

def push_marker(outlet, value):
    outlet.push_sample([str(value)])

def _matches(si, prop, value):
    # Minimal property matcher for common cases
    if prop.lower() == "type":
        return (si.type() or "") == value
    if prop.lower() == "name":
        return (si.name() or "") == value
    # Fallback: try getattr() for other props if ever needed
    try:
        return getattr(si, prop)() == value
    except Exception:
        return False

def resolve_first_inlet(prop="type", value="EEG", timeout=10):
    """
    Find the first LSL stream where stream.<prop>() == value, then open an inlet.
    Example: prop="type", value="EEG"  -> first EEG stream
    """
    streams = resolve_streams(wait_time=timeout)  # returns list[StreamInfo]
    matches = [si for si in streams if _matches(si, prop, value)]
    if not matches:
        # Helpful debug print: list available streams and their names/types
        available = [(si.name(), si.type()) for si in streams]
        raise RuntimeError(f"No LSL stream found with {prop}={value}. Available: {available}")
    return StreamInlet(matches[0])

def now_ms():
    return int(time.time() * 1000)