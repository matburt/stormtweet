class NOAA2Message(object):

    remove = ["SEVERE THUNDERSTORM",
              "WAS REPORTED",
              "TRAINED SPOTTER",
              "NATIONAL WEATHER SERVICE",
              "REMAINS IN EFFECT",
              "THIS STORM IS",
              "THIS STORM WAS",
              "METEOROLOGISTS",
              "CONTINUED TO INDICATE",
              "CONTINUED TO DETECT",
              "DOPPLER RADAR"]

    def convert(self, origmsg, msglimit=140):
        if len(origmsg) <= msglimit:
            return origmsg

        msg = origmsg
        for rmErs in self.remove:
            msg = re.sub(rmErs, "", msg)

        msg = re.sub(" AND ", ", ", msg)
        msg = re.sub("\\.+", " ", msg)
        msg = re.sub(" +", " ", msg)

        msg = msg[:msglimit].lower()

        print msg
