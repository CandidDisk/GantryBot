# Changelog

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
- Updated README.md description
- Modified math for X\Y point configuration. Thx William
- Renamed /pi to /piGantry *Done for posterity 
- Moved TkInterUI.py into /piGantry/piSerial
- Moved serialInter.py into /piGantry/piSerial
### Removed
- Removed temp.py 
- Removed non-functional workflows
- Removed /piUi
### Added
- Added Zapier issue to google sheet export
- Created serialInter.py to compartmentalise serial communication
- Created muMos directory
- Setup piSerial as module

## [0.1.0] - 2021-03-04
### Added
- Fixed versioning to semantic
- README.md
- CHANGELOG.md
- Required arduino libraries.
    - AccelStepper-1.61.0 | PrintEx-1.2.0 | SerialMenu-master | SpeedyStepper-1.0.0
- Dual axis locomotion w/ arduinoManual.ino
- TKinter python UI for raspberry pi.

## Compare [Test] w/ Unreleased


[Unreleased]: https://github.com/CandidDisk/GantryBot/compare/v0.1.0...main
[Test]: https://github.com/CandidDisk/GantryBot/compare/main...test
[0.1.0]: https://github.com/CandidDisk/GantryBot/compare/0.1.0...main