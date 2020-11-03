# How to use the driver
## Agilent_4142B
At first, let's import the instrument driver:
from qcodes.instrument_drivers.agilent.Agilent_4142B import Agilent_4142B

Creating a parameter 
vol = Agilent_4142B('vol','GPIB::XX') #XX is GPIB address

If connected, the message is shown as below;
Connected to: HEWLETT PACKARD 4142B (serial:0, firmware:4.30) in 0.18s

Setting parameters
vol.ch1.set_voltage(XX)
vol.ch2.set_voltage(XX)
Please choice the channel as ch**, and set voltage values XX in ().