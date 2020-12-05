# -*- coding: utf-8 -*-
"""
Created on Oct. 7, 2020
Last Updated on Nov. 2, 2020
This version suppurts voltage/current output and current readout.

@author: Yui, Motoya
"""
from qcodes.utils.validators import Enum, Strings
from qcodes import (Instrument, VisaInstrument,
                    ManualParameter, MultiParameter,
                    validators as vals)
from qcodes.instrument.channel import InstrumentChannel


class AgilentChannel(InstrumentChannel):

    def __init__(self, parent: Instrument, name: str, channel: str) -> None:
        """
        Args:
            parent: The Instrument instance to which the channel is
                to be attached.
            name: The 'colloquial' name of the channel
            channel: The number used by the 4142B, i.e. either
                '1' or '2'
        """

        ch = int(channel)
        if channel not in ['1', '2']: # Please add number if you use more channel
            raise ValueError('channel must be either "ch1" or "ch2"')

        super().__init__(parent, name)
        self.model = self._parent.model

        self.add_parameter('set_voltage',
                            set_cmd = "FMT1;CN{};DV{},0,{},{}".format(ch,ch,'{:.8f}',1e-6),
                            label='Set_voltage',
                            unit='V')
        
        self.add_parameter('curr',
                            get_cmd = "FMT2;CN{};MM1,{};RI{},0;AV1,0;XE".format(ch,ch,ch), #FMT2 is needed to get current value as type of float.
                            label='Current',
                            get_parser=float,
                            unit='A')

        self.add_parameter('set_current',
                            set_cmd = "FMT1;CN{};DI{},0,{}".format(ch,ch,'{:.8f}'),
                            label='Set_current',
                            unit='A')

        # self.add_parameter('volt',
        #                     get_cmd = "FMT2;CN{};MM1,{};RV{},0;AV1,0;XE".format(ch,ch,ch),
        #                     label='Voltage',
        #                     get_parser=float,
        #                     unit='V')
        self.channel = channel


class Agilent_4142B(VisaInstrument):
    """
    This is the qcodes driver for the Agilent_4142B,
    tested with HP_4142B
    """
    def __init__(self, name: str, address: str, **kwargs) -> None:
        """
        Args:
            name: Name to use internally in QCoDeS
            address: VISA ressource address
        """
        super().__init__(name, address, terminator='\r\n', **kwargs)
        idn = self.IDN.get()        
        self.model = idn['model']
        model = idn['model']

        knownmodels = ['4142B'] 
        if model not in knownmodels:
            kmstring = ('{}, '*(len(knownmodels)-1)).format(*knownmodels[:-1])
            kmstring += 'and {}.'.format(knownmodels[-1])
            raise ValueError('Unknown model. Known model are: ' + kmstring)

        # Add the channel to the instrument
        for ch in ['1','2']: # Please add number if you use more channel
            ch_name = '{}'.format(ch)
            channel = AgilentChannel(self, ch_name,ch_name)
            self.add_submodule('ch{}'.format(int(ch)), channel)

        self.connect_message()
