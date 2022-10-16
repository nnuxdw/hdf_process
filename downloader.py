# Set the URL string to point to a specific data URL. Some generic examples are:
#   https://servername/data/path/file
#   https://servername/opendap/path/file[.format[?subset]]
#   https://servername/daac-bin/OTF/HTTP_services.cgi?KEYWORD=value[&KEYWORD=value]
URL = 'your_URL_string_goes_here'

# Set the FILENAME string to the data file name, the LABEL keyword value, or any customized name.
FILENAME = 'your_filename_string_goes_here'

import requests

result = requests.get(URL)
try:
    result.raise_for_status()
    f = open(FILENAME, 'wb')
    f.write(result.content)
    f.close()
    print('contents of URL written to ' + FILENAME)
except:
    print('requests.get() returned an error code ' + str(result.status_code))