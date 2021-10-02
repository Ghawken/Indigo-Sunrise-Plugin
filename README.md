# Indigo SunRise Device Plugin

A plugin device to more easily create Sunrise type alarm clocks/devices

Essentially only runs when device is turned on, and then once finished nothing running

### Why?

Well I found it very hard to time schedules/timers with brightness and then run other devices.  
Have multiple action groups some increasing brightness of single device by 5% every 20 seconds, another action group run this.
Still very hard to know when it will get to full brightness to escalate.
This plugin allows perfectly timed light brightness, and then more lights/other lights and then action group.

My usage will be to:

Increase brightness of RGB lights to 100% - doing this over 10 minutes slowly
Then increase brightness of bedside lamp from 0 -20%
and then:
Turn Sonos radio on 

Hopefully by then already woken by the rising light levels.


## Install

Create a new Sunrise Device

### Select


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

