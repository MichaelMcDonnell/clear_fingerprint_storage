#!/usr/bin/python3
import os, sys, time
if not os.geteuid() == 0:
    sys.exit("Error: Not root. Please run with sudo.")

# Stop the fingerprint service
print("Stopping fprintd.service...")
process = os.popen("systemctl stop fprintd.service")
preprocessed = process.read()
process.close()

# Import libfprint
import gi
gi.require_version('FPrint', '2.0')
from gi.repository import FPrint, GLib
ctx = GLib.main_context_default()
c = FPrint.Context()

# Get the first fingerprint reader
c.enumerate()
devices = c.get_devices()
d = devices[0]
assert d.has_feature(FPrint.DeviceFeature.STORAGE_CLEAR)

# Clear the fingerprint reader storage
d.open_sync()
d.clear_storage_sync()
d.close_sync()

# Start the fingerprint service again
print("Starting fprintd.service...")
process = os.popen("systemctl start fprintd.service")
preprocessed = process.read()
process.close()