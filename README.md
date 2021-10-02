Indigo SunRise Device Plugin

A plugin device to more easily create Sunrise type alarm clocks/devices

Essentially only runs when device is turned on, and then once finished nothing running

Install

Create a new Sunrise Device

Select


Percent: Percentage to keep increasing brightness to
Seconds:  Over what period of time in seconds will this happen
Dimmer Devices: List - can select multiple, of dimmers to slowly increase brightness based on above
Action Group: Optional/Can be left blank:  To Run once maximum Percent reached

&
Next set of devices

NB:
Percentage should always be higher than previous set

Usage:

First set
Percent: 50
Seconds: 600
DimmerDevices: Three lamps selected
ActionGroup: Blank

When run will increase the brightness of the three select dimmerdevices, slowly to 50% maximum value over 600 seconds of time.
When makes it to 50% will then move on with next step

2nd Set of Devices:
Percent 80
Seconds 100
DimmerDevices: Main room light selected
Action Group: Blank

3rd Set of Device:
Percent 100
Seconds 100
DimmerDevices: None select
ActionGroup: Play Sonos radio active group

Hopefully following along, 2nd set will start brightness of main room from 50% --> 80% increasing over 100 seconds.
Then will go from 80% -100% over 100 seconds, there are no dimmerDevices selected so will not change any brightness.
But once 100% reached will execute actionGroup and turn on Radio.

