# watchdog
---
This Python script sets limits on the resources used by a list of given processes. Limited resources, limits and processes monitored are configurable in `config.yaml`. Additionally, these processes will be restarted in case they stop.\
For testing purposes, I've also written some small C programs (available in `test_procs`) which can run in the background and take up resources.
## Limitable resources
The script can limit any of the resources available in Python's `resource` module, such as CPU usage and heap size. A full list can be found in `config.yaml`.
## Notes
- `resource` is a Unix specific package, as such the script will only work on Unix based systems
- The following Python libraries are additionally required: `psutil`, `PyYAML`
- Expect bugs!
- Project built for college in collaboration with @Istr8
