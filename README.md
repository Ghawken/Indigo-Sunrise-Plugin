# Indigo SunRise Device Plugin

![https://github.com/Ghawken/Indigo-Sunrise-Plugin/blob/master/Resources/SunRise%20Icon/Sunrise+100.png?raw=true](https://github.com/Ghawken/Indigo-Sunrise-Plugin/blob/master/Resources/SunRise%20Icon/Sunrise+100.png?raw=true)



A plugin device to more easily create Sunrise type alarm clocks/devices.

Essentially only runs when device is turned on, and then once finished nothing running.  If 'Turn Off' device will stop current sunrise from running and turn off all devices that may be involved.

### Why?

I found it very hard to time schedules/timers with slowly increasing brightness and then at a certain brightness run other events.  Why I could try to guess timing, was difficult.
Then had issues if wanted to stop the sunrise alarm as continued to slowly increase.
  
This plugin allows perfectly timed light brightness, and then more lights/other lights and then action group.

My usage will be to:

Increase brightness of RGB bedroom lights to close to 100% -  this over 10 minutes slowly
Then increase brightness of far away lamp quickly to 100% over 2 minutes
Then increase brightness of bedside lamp to 30%
and then:
run actionGroup to:
Turn Sonos radio on 

At completion of the Sunrise event all devices are left unchanged.  If you would prefer them to turn off, select a Action Group to do so after completion.

Hopefully by then already woken by the rising light levels....

Other:

Sunrise Alarm - turning on kids lights,  slowly one by one until perhaps they are awake.  
This plugin allows this easily to be a single Indigo Relay device, actionable by a turn on/turn off, or Alexa very simply.
Alexa - please turn on kids alarm etc..

## Install

Create a new Sunrise Device

### Select

Allows four sequential events currently, can increase to further.
Each group allows mulitple dimmer devices to be selected, and once the end Percent reached an optional action group to be run.


Percent: Percentage to keep increasing brightness to for this set of dimmerDevices.
Seconds:  Over what period of time in seconds will this happen
Dimmer Devices: List - can select multiple, of dimmers to slowly increase brightness based on above
Action Group: Optional/Can be left blank:  To Run once maximum Percent reached

&
Next set of devices as per above.
Up to x4 sets.

eg.
![https://github.com/Ghawken/Indigo-Sunrise-Plugin/blob/master/Resources/Images/SunRiseDevice.png?raw=true](https://github.com/Ghawken/Indigo-Sunrise-Plugin/blob/master/Resources/Images/SunRiseDevice.png?raw=true)


## Device Status

The Sunrise Device always has a number of status to keep you updated, display in Control Page

![https://github.com/Ghawken/Indigo-Sunrise-Plugin/blob/master/Resources/Images/SunRiseStatus.png?raw=true](https://github.com/Ghawken/Indigo-Sunrise-Plugin/blob/master/Resources/Images/SunRiseStatus.png?raw=true)

Total_Percent: Current running Sunrise total percent of entire event completed
Total_Percent_Whole: As above but rounded to zero decimals for Control page use
current_Percent:  The current brightness of current set of dimmer devices
devicesDimming: Names of current devices actioning
lengthofSunrise:  Total length of sunrise event in seconds  (calculated on first run)
secondsRunning:  How long the current Sunrise has been running
status: Running, Off etc.


## Example Usage:

First set, always start from 0
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


## Additional

There is very little checking of the device setup, given multitude of options.  
Would suggest test turning on and making sure behaves as you would like before completion.