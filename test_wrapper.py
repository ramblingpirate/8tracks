import pirateTracks


selected_mix = 1915496


def nop(*args, **kwargs):
    """It's a NOP."""

def mock(*args, **kwargs):
    """It's a mock."""
    return selected_mix

pirateTracks.ask_which = mock
pirateTracks.play_stream = nop
pirateTracks.report_performance = nop

pirateTracks.start_stream()
