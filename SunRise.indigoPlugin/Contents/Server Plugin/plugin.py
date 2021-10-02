#! /usr/bin/env python2.6
# -*- coding: utf-8 -*-

"""
Author: GlennNZ

"""
import sys
import datetime
import time as t
import urllib2
import os
import shutil
import logging
import threading
import time

try:
    import indigo
except:
    pass


class Plugin(indigo.PluginBase):
    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)

        pfmt = logging.Formatter('%(asctime)s.%(msecs)03d\t[%(levelname)8s] %(name)20s.%(funcName)-25s%(msg)s',
                                 datefmt='%Y-%m-%d %H:%M:%S')
        self.plugin_file_handler.setFormatter(pfmt)

        try:
            self.logLevel = int(self.pluginPrefs[u"logLevel"])
        except:
            self.logLevel = logging.INFO

        self.indigo_log_handler.setLevel(self.logLevel)
        self.logger.threaddebug(u"logLevel = " + str(self.logLevel))

        self.logger.debug(u"Initializing plugin.")
        self.pluginIsInitializing = True
        self.pluginIsShuttingDown = False
        self.prefsUpdated = False
        self.logger.info(u"")
        self.logger.info(u"{0:=^130}".format(" Initializing New Plugin Session "))
        self.logger.info(u"{0:<30} {1}".format("Plugin name:", pluginDisplayName))
        self.logger.info(u"{0:<30} {1}".format("Plugin version:", pluginVersion))
        self.logger.info(u"{0:<30} {1}".format("Plugin ID:", pluginId))
        self.logger.info(u"{0:<30} {1}".format("Indigo version:", indigo.server.version))
        self.logger.info(u"{0:<30} {1}".format("Python version:", sys.version.replace('\n', '')))
        self.logger.info(u"{0:<30} {1}".format("Python Directory:", sys.prefix.replace('\n', '')))
        self.logger.info(u"{0:=^130}".format(""))

        self.deviceThreads = []
        self.deviceList = []

    def actionControlDevice(self, action, device):

        if action.deviceAction == indigo.kDeviceAction.TurnOn:
            self.logger.debug(u"Request to turn On Sunrise device noted")
            self.set_turnOn(action, device)

        elif action.deviceAction == indigo.kDeviceAction.TurnOff:
            self.logger.debug("Request to turn off sunrise device noted")
            self.set_turnOff(action,device)

        elif action.deviceAction == indigo.kDeviceAction.Toggle:
            self.logger.debug("Request to toggle sunrise device noted")

        elif action.deviceAction == indigo.kDeviceAction.SetBrightness:
            self.logger.debug("Request to setBrightness device")

    def set_turnOn(self,action,device):
        self.logger.debug(u"set Turn On Starting....")

        ## need to thread here otherwise won't respond
        stoppedThread = self.stopSceneThread(device)

        if stoppedThread:
            self.logger.debug(u"Thread was running... Restarting..")
            time.sleep(5)

        device.updateStateOnServer('status', value="Running")
        device.updateStateOnServer('onOffState', value=True, uiValue='Running')

        devicesceneThread = SunriseDeviceThread(device, self.logger, action)
        self.deviceThreads.append(devicesceneThread)
        self.logger.info("Starting SunRise Device: "+unicode(device.name))

    def stopSceneThread(self, device):
        indigoDevice = indigo.devices[device.id]
        deviceSceneThread = None
        stoppedThread = False
        for gThread in self.deviceThreads:
            if gThread.indigoDevice.name == indigoDevice.name:
                deviceSceneThread = gThread

        if deviceSceneThread is not None:
            self.debugLog("...stopSceneThread Stopping scene thread: " + indigoDevice.name)
            deviceSceneThread.stopDevConcurrentThread()
            self.deviceThreads.remove(deviceSceneThread)
            deviceSceneThread = None
            stoppedThread = True
            # any remaining scene workItems will be skipped if an activeScene Thread isn't found for the device

        self.debugLog("...stopSceneThread Total remaining scene threads - " + str(len(self.deviceThreads)))
        return stoppedThread

    def set_turnOff(self,action,device):
        self.logger.debug(u"Set Turn Off Starting....l")
        device.updateStateOnServer('status',value="Turning off")
        device.updateStateOnServer('onOffState', value=False, uiValue='Off')
        for gThread in self.deviceThreads:
            if gThread.indigoDevice.name == device.name:
                gThread.stopDevConcurrentThread()
                self.deviceThreads.remove(gThread)
                indigo.server.log("Stopping device thread: " + device.name)



    def closedPrefsConfigUi(self, valuesDict, userCancelled):
        if not userCancelled:
            try:
                self.logLevel = int(valuesDict[u"logLevel"])
            except:
                self.logLevel = logging.INFO
            self.indigo_log_handler.setLevel(self.logLevel)
            self.logger.debug(u"logLevel = " + str(self.logLevel))


        return True

    # Start 'em up.
    def deviceStartComm(self, dev):

        self.debugLog(u"deviceStartComm() method called.")
        dev.stateListOrDisplayStateIdChanged()

        try:
            self.deviceList.append(dev.id)
        except Exception as ex:
            self.errorLog("Exception hit in deviceStartComm - " + str(ex))

    # Shut 'em down.
    def deviceStopComm(self, device):

        self.debugLog(u"deviceStopComm() method called.")
        indigo.server.log(u"Stopping device: " + device.name)
        for gThread in self.deviceThreads:
            if gThread.indigoDevice.name == device.name:
                gThread.stopDevConcurrentThread()
                self.deviceThreads.remove(gThread)
                indigo.server.log("Stopping device thread: " + device.name)

        if device.id in self.deviceList:
            self.deviceList.remove(device.id)
            indigo.server.log("Stopping device: " + device.name)



    def shutdown(self):

         self.debugLog(u"shutdown() method called.")

    def startup(self):

        self.debugLog(u"Starting Plugin. startup() method called.")

        # See if there is a plugin update and whether the user wants to be notified.
        try:
            self.sleep(1)
        except Exception as error:
            self.errorLog(u"Update checker error: {0}".format(error))

    def validatePrefsConfigUi(self, valuesDict):

        self.logger.debug(u"validatePrefsConfigUi called")
        errorDict = indigo.Dict()

        if len(errorDict) > 0:
            return (False, valuesDict, errorDict)

        return (True, valuesDict)



    def setStatestonil(self, dev):

         self.debugLog(u'setStates to nil run')


    def refreshDataAction(self, valuesDict):
        """
        The refreshDataAction() method refreshes data for all devices based on
        a plugin menu call.
        """

        self.debugLog(u"refreshDataAction() method called.")
        self.refreshData()
        return True

    def refreshData(self):
        """
        The refreshData() method controls the updating of all plugin
        devices.
        """

        self.debugLog(u"refreshData() method called.")

        try:
            # Check to see if there have been any devices created.
            if indigo.devices.itervalues(filter="self"):

                self.debugLog(u"Updating data...")

                for dev in indigo.devices.itervalues(filter="self"):
                    self.refreshDataForDev(dev)

            else:
                indigo.server.log(u"No Enphase Client devices have been created.")

            return True

        except Exception as error:
            self.errorLog(u"Error refreshing devices. Please check settings.")
            self.errorLog(unicode(error.message))
            return False

    def refreshDataForDev(self, dev):

        if dev.configured:

            self.debugLog(u"Found configured device: {0}".format(dev.name))

            if dev.enabled:

                self.debugLog(u"   {0} is enabled.".format(dev.name))
                timeDifference = int(t.time() - t.mktime(dev.lastChanged.timetuple()))

            else:

                 self.debugLog(u"    Disabled: {0}".format(dev.name))



    def refreshDataForDevAction(self, valuesDict):
        """
        The refreshDataForDevAction() method refreshes data for a selected device based on
        a plugin menu call.
        """

        self.debugLog(u"refreshDataForDevAction() method called.")

        dev = indigo.devices[valuesDict.deviceId]

        self.refreshDataForDev(dev)
        return True

class SunriseDeviceThread(threading.Thread):
    def __init__(self, indigoDevice, logger, actionProps):
        super(SunriseDeviceThread, self).__init__()
        self.indigoDevice = indigoDevice
        self.logger = logger
        self.stopThread = False
        self.actionProps = actionProps
        self.start()

    def run(self):
        try:

            # do the scene stuff
            self.logger.debug("group running - " + str(self.indigoDevice.name) + ", thread-id=" + str(self.name))
            self.logger.debug("Action Props:"+unicode(self.actionProps))
            self.logger.debug("Device Props:"+unicode(self.indigoDevice.pluginProps))
            # take a sleep based on the scene preferences

            dimmerDevice = []
            percentage = []
            actionGroup = []
            second = []

            x = 1
            while (x <= 4):
                dimmerDevice.append([ self.indigoDevice.pluginProps.get('dimmerDevice'+str(x), None) ] )
                percentage.append( self.indigoDevice.pluginProps.get('percent' + str(x), None) )
                actionGroup.append( self.indigoDevice.pluginProps.get('actionGroup' + str(x), None) )
                second.append( self.indigoDevice.pluginProps.get('seconds' + str(x), None) )
                x =x +1

            totaltime = int(0)
            for seconds in second:
                if seconds !="":
                    totaltime = int(seconds)+totaltime
            self.logger.debug("Total length of Sunrise device ="+unicode(totaltime)+" seconds")
            self.indigoDevice.updateStateOnServer('lengthofSunrise', value=int(totaltime))
            self.indigoDevice.updateStateOnServer('secondsRunning', value=int(0))
            try:
                self.logger.debug(unicode(dimmerDevice))

                ## Steps
                x = 0  ## this is number of data points currently == 4
                startpercentage = float(0.0)

                step = float(0.5)  ## this is out of 100...
                oldstep = 0
                oldtime = t.time()
                starttime = t.time()
                while (x <=3) and not self.stopThread:
                    if percentage[x]==None:
                        self.logger.debug("Percentage None so ending.")
                        break
                    oldpercentage = float(percentage[x])
                    individualtiming = float(float(float(second[x]) / (float(percentage[x])))) / 2  ## make 0.5..%
                    while (step <= float(percentage[x])) and not self.stopThread:
                        ## needs to take seconds to end

                        if step != oldstep:
                            self.logger.debug("Dividing Step:"+str(x)+" into parts based on time to complete = "+unicode(second[x]+" seconds:"))
                            self.logger.debug("Individual timing second / percentage, so 0.5% = " + unicode(individualtiming) + " seconds")
                            oldstep = step
                        #self.logger.debug("Current time ="+unicode(current_time))
                        if t.time() > oldtime+individualtiming:
                            self.logger.debug("Current Percentage (or step)="+unicode(step)+ " % completed")
                            oldtime = t.time()
                            for dimmerlist in dimmerDevice[x]:
                                for dimmers in dimmerlist:
                                    self.logger.debug("Setting current Dimmer: "+unicode(dimmers)+" to "+unicode(step)+" % brightness" )
                                    try:
                                        iDev = indigo.devices[int(dimmers)]
                                        indigo.dimmer.setBrightness( iDev,value=int(step) )
                                    except:
                                        self.logger.exception("Exception setting brightness for this dimmer device?")
                            step = step + 0.5
                            self.indigoDevice.updateStateOnServer('current_Percentage',value=float(step))
                            self.indigoDevice.updateStateOnServer('secondsRunning', value=int(t.time()-starttime))
                        #time.sleep(individualtiming)  ## should be == 1% percentage point.  But if huge will be issue as will hang
                        time.sleep(int(individualtiming)/2)

                    self.logger.debug("End of Step and first percentage.. Checking next. ")
                    if actionGroup[x] != "" and not self.stopThread:  ## reached end of percentage run action group
                        self.logger.debug("Running Action Group "+unicode(actionGroup[x])+" reached percent:" + unicode(step) + " %")
                        indigo.actionGroup.execute( int(actionGroup[x]) )
                    ## increment
                    x= x +1
                    ## check next percentage to make sure exists.
                    if percentage[x]=="":
                        self.logger.debug("Next Percentage None so ending.")
                        break
                    if float(percentage[x]) < oldpercentage:
                        self.logger.info("Error with setup of Sunrise Device, each percentage needs to increase in order to max of 100")
                        break
                time.sleep(0.5)

                self.logger.info("End of Sunrise Device.  Turning Off")
                self.indigoDevice.updateStateOnServer('onOffState', value=False, uiValue='Off')
                self.indigoDevice.updateStateOnServer('current_Percentage', value=int(0))
                self.indigoDevice.updateStateOnServer('secondsRunning', value=int(0))

                return
            except:  # Do my other non-socket reading stuff here
                self.logger.exception(
                    "...Scene group exception - " + str(self.indigoDevice.name) + ", thread-id=" + str(self.name))
                self.logger.debug(
                    "...Unexpected loop error: - " + str(sys.exc_info()) + ", thread-id=" + str(self.name))

        except:
            self.logger.exception(
                "...Scene exception hit, process exiting - " + str(self.indigoDevice.name) + ", thread-id=" + str(self.name))
            self.logger.debug("...Unexpected non-loop error: - " + str(sys.exc_info()) + ", thread-id=" + str(self.name))


    def stopDevConcurrentThread(self):
        self.logger.debug(
            "...stopping concurrent thread for group - " + str(self.indigoDevice.name) + ", thread-id=" + str(self.name))
        self.stopThread = True