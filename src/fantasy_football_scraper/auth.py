"""
This module handles the authentication for the ESPN API.
"""

# It's recommended to use environment variables or a config file for sensitive data.
# For this example, we'll keep them here but acknowledge this is not best practice.
COOKIES = {
    "kona_v3_teamcontrol_ffl": '{"leagueId":997575,"seasonId":2025,"teamId":4}',
    "kona_v3_environment_season_ffl": '{"leagueId":997575,"seasonId":null}',
    "SWID": "{A27D5FAC-0651-48E7-BE8C-DDE9A16BA2A5}",
    "espnAuth": '{"swid":"{A27D5FAC-0651-48E7-BE8C-DDE9A16BA2A5}"}',
    "espn_s2": "AEB%2FhuZCQ36VYF3eV6yA5g85%2FNhBk7I2m%2BlZHOrUoEORCW%2FT22GeI1fpo%2Bt8aBcSzGg7Ao0EqQZkC9uFXNNsWcwdRzo4MUSSVewK6iT6FpDXbUJgu%2Fd2DEoyQfRt8M3M9ZMebtZy8AnkgwJG%2Bd9XvTSjGh2BVO4Y6leqG8bh4FLBl2J9Pd2cucIKiyMa0U1cRcC%2ByL2twZ%2B8jhio3QK6AlOkWHXLX%2Fq9BclJF%2BSMUAyAzICQQvjp9obNXaoDrkF2%2FgfnJRanJvkUgZk6BBBXhmx2radX3Acf1RKoS%2B5WwBeK9A%3D%3D"
}

HEADERS = {
    'x-fantasy-filter': '{"players":{"filterStatus":{"value":["FREEAGENT","WAIVERS","ONTEAM"]},"sortDraftRanks":{"sortPriority":1,"sortAsc":true,"value":"STANDARD"},"limit":2000}}'
}
