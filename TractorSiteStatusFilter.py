from TrStatusFilter import TrStatusFilter

import re
from datetime import datetime

# See /opt/pixar/Tractor-2.4/lib/python2.7/site-packages/tractor/apps/blade/TractorSiteStatusFilter.py for example

## ------------------------------------------------------------- ##
class TractorSiteStatusFilter (TrStatusFilter):
    def __init__ (self):
        self.super = super(type(self), self)  # magic proxy object
        self.super.__init__()
        
        self.logger.info("initializing site status filters")

        # Stop Tractor prorgess from being matched and eaten, but don't mess up the match groups
        self.cmdLogFilterRE = re.compile(
                r'(?!x)x(\d*)'
                 '|[0-9:.]{11} \S+ +PROG +\| +(\d*)'
                 '|TR_PROGRESS +(\d*)'
                 '|ALF_PROGRESS +(\d*)'
                 '|(\d*)% done'
                 '|Frame +\d* +\((\d*) +of +(\d*)\)'
                 '|TR_EXIT_STATUS +(-?\d*)'
                 '|ALF_EXIT_STATUS +(-?\d*)'
                 '|TR_EXPAND_CHUNK +"(.+)" ?(\S+)?'
            )

        # Record the start time to show timestamps
        self.t0 = datetime.now()


    def FilterSubprocessOutputLine (self, cmd, textline):
        (flag, payload) = self.super.FilterSubprocessOutputLine( cmd, textline )

        # If it is just log text, add a tiemstamp
        if flag == self.super.TR_LOG_TEXT_EMIT:
            payload = "[T+{}]: {}".format(self.delta_to_hms(datetime.now() - self.t0), payload)
        
        return (flag, payload)

    ## --------------- helper to convert timedelta to h:mm:ss ------------------ ##
    @classmethod
    def delta_to_hms(cls, td):
        hours, remainder = divmod(td.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        return "{:.0f}:{:02.0f}:{:02.4f}".format(hours, minutes, seconds)

## ------------------------------------------------------------- ##
