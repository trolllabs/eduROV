# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning]
(https://www.python.org/dev/peps/pep-0440/).

## [Unreleased]
### Added
- Minimal, rc_car and experiment code examples
- Sphinx docs
- Keyup and keydown methods to key manager
- Possibility to change sensor update interval while the program is running
- Possibility to choose redirect type between 301 and 302
- support for http and www redirect from links

### Changed
- Moved "arm" and "stop" from POST to GET method
- KeyUp and KeyDown uses GET instead of POST
- KeyManager uses dictionary instead of list for keys to increase performance
- Refactored script.js into multiple files for clarity
- Engange eduROV now has fixed places for sensor values
- Engange eduROV has denomination on sensor values
- renamed examples_edurov folder to examples

### Removed
- Pygame implementations
- Possibility to set keys from json dict
- Duo file for pygame implementations
- Armed property in ROVSyncer, use local variable in js instead
- Echo response in webserver
- Armed response in webserver
- try except clause in GET method
- args_resolution_help as command help
- STANDARD_RESOLUTIONS

## [0.0.4] - 2018-03-20
### Added
- Tooltips for buttons on Engange eduROV index page
- Changelog created
- Arming of ROV functionality
- Custom response parameter for WebMethod class, lets the user define own
  respononses for the web request server
- Favicon to webpage
- Version check under installation, will abort and warn user if the setup is
  runned with python 2
- New roll indicator that can be toggled
- New sensor value that displays free disk space on memory card

## [0.0.3] - 2018-03-20
### Added
- New GUI in browser based on bootstrap

[Unreleased]: https://github.com/trolllabs/eduROV/compare/0.0.4...master
[0.0.4]: https://github.com/trolllabs/eduROV/compare/0.0.3...0.0.4
[0.0.3]: https://github.com/trolllabs/eduROV/compare/0.0.1rc1...0.0.3