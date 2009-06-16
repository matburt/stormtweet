import noaaRSS
import optparse
import sys
import model
from ConfigParser import RawConfigParser

def getConfig(path):
    rc = RawConfigParser()
    if path not in rc.read(path):
        print("Invalid Configuration File")
        sys.exit(1)
    return rc

def main():
    op = optparse.OptionParser()
    op.add_option("-c", "--config", dest="config",
                  help="configuration file")
    op.add_option("-i", "--initialize", dest="initialize",
                  help="Initialize database, don't actually post entries",
                  action="store_true", default=False)
    op.add_option("-v", "--verbose", dest="verbose",
                  help="Display extra information",
                  action="store_true", default=False)
    (options, args) = op.parse_args()

    if options.config is None:
        print("Configuration file required")
        sys.exit(1)

    config = getConfig(options.config)

    model.setupModel(config.get("model", "bind"))
    if options.initialize:
        print "Initializing Database"
        model.createDataBase()
        # Make codepath just create at the moment
        # without attempting to fetch the feeds
        sys.exit(1)

    ts = noaaRSS.ThunderStorm(config.get("stormtweet", "noaafeed"),
                              config.get("stormtweet", "shelfFile"))

if __name__ == '__main__':
    main()
