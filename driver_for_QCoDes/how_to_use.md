# How to use the driver
## Agilent_4142B
At first, let's import the instrument driver:<br>
from qcodes.instrument_drivers.agilent.Agilent_4142B import Agilent_4142B<br><br>

Creating a parameter <br>
vol = Agilent_4142B('vol','GPIB::XX') #XX is GPIB address<br><br>

If connected, the message is shown as below;<br>
Connected to: HEWLETT PACKARD 4142B (serial:0, firmware:4.30) in 0.18s<br><br>

Setting parameters<br>
vol.ch1.set_voltage(XX)<br>
vol.ch2.set_voltage(XX)<br>
Please choice the channel as ch**, and set voltage values XX in ().<br><br>