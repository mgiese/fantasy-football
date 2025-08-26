"""
This module handles the authentication for the ESPN API.

IMPORTANT: To use this scraper for your own private league, you MUST provide
your own authentication cookies. Failure to do so will result in a 401 or 403
(Unauthorized) error from the ESPN API.

Follow these steps to get your cookie values:

1.  Log in to your ESPN Fantasy Football league page in your web browser (e.g., Chrome, Edge, Firefox).
2.  Open the browser's Developer Tools. You can usually do this by pressing F12 or right-clicking
    on the page and selecting "Inspect".
3.  Go to the "Application" tab (in Chrome/Edge) or the "Storage" tab (in Firefox).
4.  In the left-hand menu, expand the "Cookies" section and select "https://fantasy.espn.com".
5.  You will see a list of all cookies for the site. You need to find two of them:
    - `espn_s2`: Find this in the list and copy its entire "Cookie Value".
    - `SWID`: Find this in the list and copy its "Cookie Value".
6.  Paste these values into the `COOKIES` dictionary below, replacing the existing placeholder values.

The `HEADERS` dictionary contains the `x-fantasy-filter`, which tells the API to return
all players (free agents, on waivers, and on a team). You generally won't need to
change this unless you want to experiment with different filters.
"""

try:
    from .local_auth import COOKIES
except ImportError:
    # Fallback or default cookies if local_auth.py is not found
    # It's recommended to use environment variables or a config file for sensitive data.
    print("Warning: `local_auth.py` not found. Using placeholder cookies. Please create `local_auth.py` with your actual cookies.")
    COOKIES = {
        "espn_s2": "YOUR_ESPN_S2_COOKIE_HERE",
        "SWID": "YOUR_SWID_COOKIE_HERE"
    }


HEADERS = {
    'x-fantasy-filter': '{"players":{"filterStatus":{"value":["FREEAGENT","WAIVERS","ONTEAM"]},"sortDraftRanks":{"sortPriority":1,"sortAsc":true,"value":"STANDARD"},"limit":2000}}'
}
