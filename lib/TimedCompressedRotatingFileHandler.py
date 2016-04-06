import logging
import logging.handlers
import zipfile
import codecs
import sys
import os
import time
import glob


class TimedCompressedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    """
    Extended version of TimedRotatingFileHandler that compress logs on rollover.
    """
    def doRollover(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        dfn = self.baseFilename + "_" + time.strftime(self.suffix, timeTuple)
        if os.path.exists(dfn):
            os.remove(dfn)
        # Issue 18940: A file may not have been created if delay is True.
        if os.path.exists(self.baseFilename):
            os.rename(self.baseFilename, dfn)
            # Added compression. 
            file = zipfile.ZipFile(dfn + ".gz", "w")
            file.write(dfn, os.path.basename(dfn), zipfile.ZIP_DEFLATED)
            file.close()
            os.remove(dfn)
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        if not self.delay:
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        #If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:           # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt
        
#   def doRollover(self):
#        """
#        do a rollover; in this case, a date/time stamp is appended to the filename
#        when the rollover happens.  However, you want the file to be named for the
#        start of the interval, not the current time.  If there is a backup count,
#        then we have to get a list of matching filenames, sort them and remove
#        the one with the oldest suffix.
#        """
#
#        self.stream.close()
#        # get the time that this sequence started at and make it a TimeTuple
#        t = self.rolloverAt - self.interval
#        timeTuple = time.localtime(t)
#        dfn = self.baseFilename + "." + time.strftime(self.suffix, timeTuple)
#        if os.path.exists(dfn):
#            os.remove(dfn)
#        os.rename(self.baseFilename, dfn)
#        if self.backupCount > 0:
#            # find the oldest log file and delete it
#            s = glob.glob(self.baseFilename + ".20*")
#            if len(s) > self.backupCount:
#                s.sort()
#                os.remove(s[0])
#        #print "%s -> %s" % (self.baseFilename, dfn)
#        if self.encoding:
#            self.stream = codecs.open(self.baseFilename, 'w', self.encoding)
#        else:
#            self.stream = open(self.baseFilename, 'w')
#        self.rolloverAt = self.rolloverAt + self.interval
#        if os.path.exists(dfn + ".zip"):
#            os.remove(dfn + ".zip")
#        file = zipfile.ZipFile(dfn + ".zip", "w")
#        file.write(dfn, os.path.basename(dfn), zipfile.ZIP_DEFLATED)
#        file.close()
#        os.remove(dfn)