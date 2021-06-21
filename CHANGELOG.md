# Changelog

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
- runZero now compares w/ float instead of messily cutting string
- readDial now returns clean float instead of string
- Refactored positional & keyword arguments & their references of runMoves, runZero, runOneMove to support dual motor & to be polymorphic
- Changed references to X & Y to be agnostic (i.e 1 & 2 instead of X & Y) | This is so that order of motors is not hard coded & a separate function isn't required
- Further abstracted runMoves function by taking out individual move & refactoring into new runOneMove function
- Refactored zeroing to have pi feed steps directly to clearCore
- Changed all references in changelog of unit tests to function tests
- readDial flushes i/o before taking a reading
- readLaser flushes i/o before taking a reading
- Automated serialInterTest.py function test
- serialInterTest.py & ccSide.ino function test refactored to support pi pass clearcore # of steps
- Refactored serialInterTest & ccSide to be synchronous for most actions
    - ccSide commHandSake no longer waits for newData before it sends request
- Fixed changing exposure, turns out has to be negative integer < 0 && >= -11
- Refactored dotTest.py function test to be more pythonic & remove reoccuring clutter
- serialDeviceTest.py function test now completely uses serialInter module
- laser rangefinder functions in serialInter module now refactored for new laser rangefinder

### Removed
- TkInter.py, redundant now that pyGUI module is ready
- data_file.json, data_file1.json & data_file2.json. Outdated clutter
- piSide.py, redundant now that serialInter module serialInterTest.py & ccSide.ino function test is ready
- readSerialInput.ino, redundant now that serialInter module serialInterTest.py & ccSide.ino function test is ready
- sendInput.py, redundant now that serialInterTest.py function test is ready
- Outdated code in serialDeviceTest.py function test

### Added
- UI jogging & zero working
- Added motorFunc calcAvailableSPM function to handle generating motion profile
- Added MM to Steps functionality to mathFunc calcDist
- Middling UI
- Motion parameter UI
- pyGUI module for handling UI
- ccSideY function test for 2nd clearCore
- Non-micrometer support for runZero
- Removed references of laser rangefinder except in serialInter module
- Added second clearCore to serialInterTest function test
- serialDeviceTest new framework for testing laser reading
- Added new argument for laser functions to support continuous or one time reading
- runZero function from serialInterTest function test now a function under motorFunc module
- runMoves function from serialInterTest function test now a function under motorFunc module
- initializeLaser function in serialInter module, handles sending start msg / addr to laser rangefinder
- New reliable laser rangefinder
- swing test / imsub test & data collection (imgsub values & thresholding imsub) added to dotTest.py function test
- imgData dir
- matPlot best fit graphs
- imgData laser leveller mounted camera 24v PSU img data set
- imgData laser leveller mounted camera img data set
- imgData regular tripod mounted camera img data set
- imgData wall mounted camera img data set
- takeImg.py Lightrod imsub & photo taking test function
- compareImg write to csv imsub values between two given images
- dotTest.py function test includes bestFitPoly 
- bestFitPoly for mathFunc module to find best fit given x list y list & degree


## [1.1.0-alpha] - 2021-05-13
### Changed
- Reworked pixelWiseScan to use numpy nonzero func instead of iteratively accessing threshold array
- Reworked piSerial serialInter.py
- piSerial now functional module
### Removed
- Luminosity test
- opencv2test.py
- imageDiff.py
- imageProcess redundant files 
### Added
- compareContour function for comparison of two image's contour center dots, AKA "check camera wobble / is lightrod still" 
- dotTest.py function test for imageProcess module
- cameraFunc.py for handling image processing functions
- Added average.py for pixelwise alternative to opencv contouring
- mathFunc.py for handling math related functions
- serialObject class in piSerial serialInter module to handle each device as it's own object
- New piSerial motor module to handle motor related data & functions
- New serial test case using piSerial module serialInterTest.py
## [1.0.0-alpha] - 2021-04-29
### Changed
- Refactored average.py & fixed tons of spaghetti + redundancy
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


[Unreleased]: https://github.com/CandidDisk/GantryBot/compare/main...v1.1.0-alpha
[Test]: https://github.com/CandidDisk/GantryBot/compare/main...test
[0.1.0-alpha]: https://github.com/CandidDisk/GantryBot/compare/0.1.0...main
[1.0.0-alpha]: https://github.com/CandidDisk/GantryBot/compare/1.0.0-alpha...main
[1.1.0-alpha]: https://github.com/CandidDisk/GantryBot/compare/1.1.0-alpha...main