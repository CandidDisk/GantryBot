# Changelog

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
- Reworked piSerial serialInter.py
- piSerial now functional module
### Removed

### Added
- mathFunc.py for handling math related functions
- serialObject class in piSerial serialInter module to handle each device as it's own object
- New piSerial motor module to handle motor related data & functions
- New serial test case using piSerial module serialInterTest.py
## [1.0.0-alpha] - 2021-04-29
### Changed
- Updated requirements.txt to include opencv-python v4.5.1
- Updated README.md w/ ClearCore prerequisites 
- Renamed 0.1.0 tag to 0.1.0-alpha
- ClearCore zeroing test IO handshake is now proper function
- renamed MoveDistance to moveDistance to keep camel case 
- Digital dial now read by Pi using ch340 based USB To Ser chip included in digital dial cable.
- Laser rangefinder read by Pi
- Removed start bit from serial comm, only read stop bit / new line
- Using ClearCore PIC motor driver instead of Arduino Uno
- Updated README.md description
- Modified math for X\Y point configuration. Thx William
- Renamed ./pi to ./piGantry *Done for posterity 
- Moved TkInterUI.py into /piGantry/piSerial
- Moved serialInter.py into ./piGantry/piSerial
- Renamed ./muMos to imageProcess
  - Name more accurately reflects scope & function of directory 
    (Not actual muMos software, only image processing for verifying data within scope of Gantry)
- Changed changelog link in README.md from absolute to relative
- ~~Switched to using AccelStepper & Arduino Stepper~~
### Removed
- Arduino directory
- AccelStepper & Arduino Stepper
- Arduino Uno
- SpeedyStepper
- Removed temp.py 
- Removed non-functional workflows
- Removed ./piUi
- Removed ./library, redundant as arduino pre-requisites can be installed via arduino-cli 
- * Removed mermaidjs-github-svg-generator | build script not functional
- mermaidjs workflow
- mermaidjs
### Added
- Writing data of each move to json during test move
- Steps to mm conversion function
- Test move after zeroing completes in zeroing test
- Refactor of test sendInput.py to better manage scopes  
- Proper handshaking for serial I/O between CC & Pi
- opencv2test.py | Light dot recognition, counting, & grouping
- ClearCore arduino ide wrapper
- ClearCore library
- ~~arduinoZero & arduinoZero2, for first time zero~~
- ~~Secondary arduino for y axis~~
- Added Zapier issue to google sheet export
- Created serialInter.py to compartmentalise serial communication
- Created muMos directory
- Setup piSerial as module
- * MermaidJS-to-svg for flowchart in readme !!Removed!!
- compile-mermaid-markdown-action | Any commits w/ change to .mermaid files will be compiled into a .png & pull request automatically made
## [0.1.0-alpha] - 2021-03-04
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
[0.1.0-alpha]: https://github.com/CandidDisk/GantryBot/compare/0.1.0...main
[1.0.0-alpha]: https://github.com/CandidDisk/GantryBot/compare/1.0.0-alpha...main
