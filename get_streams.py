"""
Define functions to resolve LSL streams

"""


class MyException(Exception):
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)


def get_streams_2_players():
    """
    Resolve protocols from two players

    """

    from pylsl import resolve_byprop, StreamInlet
    from game_params import PL1, PL2, LSL_TIMEPROP

    # -------------------- connect to streams ------------------- #
    stream_pl1 = resolve_byprop('name', PL1, timeout=LSL_TIMEPROP)
    stream_pl2 = resolve_byprop('name', PL2, timeout=LSL_TIMEPROP)
    if not stream_pl1:
        raise MyException('STREAM {} CONNECTION ERROR'.format(PL1.upper()))

    if not stream_pl2:
        raise MyException('STREAM {} CONNECTION ERROR'.format(PL2.upper()))

    pl1_inlet = StreamInlet(stream_pl1[0])
    pl2_inlet = StreamInlet(stream_pl2[0])
    # ----------------------------------------------------------- #
    return pl1_inlet, pl2_inlet

