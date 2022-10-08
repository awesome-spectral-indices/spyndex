import json

import requests

# Request Awesome List of Spectral Indices
awesomeSpectralIndices = requests.get(
    "https://raw.githubusercontent.com/awesome-spectral-indices/awesome-spectral-indices/main/output/spectral-indices-dict.json"
).json()
# Save the dict as json file
with open("./spyndex/data/spectral-indices-dict.json", "w") as fp:
    json.dump(awesomeSpectralIndices, fp, indent=4, sort_keys=True)

# Request Constants
constants = requests.get(
    "https://raw.githubusercontent.com/awesome-spectral-indices/awesome-spectral-indices/main/output/constants.json"
).json()
# Save the dict as json file
with open("./spyndex/data/constants.json", "w") as fp:
    json.dump(constants, fp, indent=4, sort_keys=True)

# Request Bands
bands = requests.get(
    "https://raw.githubusercontent.com/awesome-spectral-indices/awesome-spectral-indices/main/output/bands.json"
).json()
# Save the dict as json file
with open("./spyndex/data/bands.json", "w") as fp:
    json.dump(bands, fp, indent=4, sort_keys=True)
