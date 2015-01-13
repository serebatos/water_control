__author__ = 'bonecrusher'
import sys
import gspread

# Google Docs account email, password, and spreadsheet name.
GDOCS_EMAIL = 'serebatos'
GDOCS_PASSWORD = 'rfgecnfgmail2'
GDOCS_SPREADSHEET_NAME = '0ApX_lPM02tkIdDdlODRkeXk2NEU3V0NqeDRDRGU0eHc'

# How long to wait (in seconds) between measurements.
FREQUENCY_SECONDS = 30


def login_open_sheet(email, password, spreadsheet):
    """Connect to Google Docs spreadsheet and return the first worksheet."""
    # try:
    c = gspread.Client(auth=(email, password))
    c.login()
    print "Logged in..."
    worksheet = c.open_by_key(spreadsheet).sheet1
    return worksheet
    # except:
    #     print 'Unable to login and get spreadsheet.  Check email, password, spreadsheet name.'
    #     sys.exit(1)

worksheet = login_open_sheet(GDOCS_EMAIL, GDOCS_PASSWORD, GDOCS_SPREADSHEET_NAME)