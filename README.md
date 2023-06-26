[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

# Bucharest Hot Water Sensor
A simple Home Assistant integration that let's you select one or more Bucharest Thermal Points and exposes a binary sensor for each, telling you if the point is currently providing hot water or not(true means you have hot water). 

It does this by polling the [CMTEB website](https://www.cmteb.ro/functionare_sistem_termoficare.php) and searching if there is any information related to your thermal point or not.

## How to use

- Add this repository to HACS as a Custom repository by following the [HACS Documentation](https://hacs.xyz/docs/faq/custom_repositories)
- Go to HACS -> Integrations -> Search for "Bucharest Hot Water Sensor" and add it to HA
- Reboot Home Assistant
- Go to Settings -> Devices&Services -> Click the "ADD INTEGRATION" button and search for "Bucharest Hot Water Sensor"
- Give the entry a user friendly name via the Address name field(e.g. Home)
- Enter the Thermal Point that provides hot water to the specified address(you could consult the [CMTEB map](https://www.cmteb.ro/harta_stare_sistem_termoficare_bucuresti.php) to find the point)
- NOTE: Currently the name is case sensitive. So enter the Thermal Point name exacly as it is written on the website.