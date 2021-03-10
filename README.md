# GantryBot


#### Description
Gantry Bot is a dual axis, dual servomotor driven machine automating data collection w/ MuMos. It uses an arduino for servomotor locomotion and a Pi for higher level tasks and camera control / image processing.

See [changelog](CHANGELOG.md) for more info
##### *Currently requires an instance of Arduino IDE*

## Prerequisites

#### Python 3.x

#### Arduino 1.5.6 or compatible

Refer to [**ARDUINO(1) Manual Page**](https://github.com/arduino/Arduino/blob/master/build/shared/manpage.adoc)

#### Arduino IDE 1.8.13 or compatible
* [Arduino IDE downloads **All**](https://www.arduino.cc/en/software)
* [Arduino IDE guide **Linux**](https://www.arduino.cc/en/guide/linux)


## Installation

``` bash
#Clone the repo w/ 
$ git clone https://github.com/CandidDisk/GantryBot.git GantryBot
#Install required python libraries w/
$ pip install -r requirements.txt

#To be updated once installation is standardized
```

* also stick to mixed case for now plz

## Project Overview

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggVERcbiAgZ2Fucm9iW1Byb2plY3QgU3RydWN0dXJlXSAtLT4gUGlcbiAgZ2Fucm9iIC0tPiBBcmR1aW5vXG5cbiAgUGkgLS0-IEIocGlHYW50cnkpXG4gIEIgLS0-IEMoaW1hZ2VQcm9jZXNzKVxuICBCIC0tPiBEKHBpU2VyaWFsKVxuXG5cbiAgRCAtLT4gRShbc2VyaWFsSW50ZXIucHldKVxuICBEIC0tPiBGKFtUa0ludGVyVUkucHldKVxuICBGIC0tPiBFXG5cbiAgICBBcmR1aW5vIC0tPiBsb2NvKFthcmR1aW5vTW90b3IuaW5vXSlcblx0XHQiLCJtZXJtYWlkIjp7InRoZW1lIjoiZGVmYXVsdCJ9fQ)](file:///C:/Repo/GantryBot/mermaidJs/editor/Mermaid%20live%20editor.htm#/edit/eyJjb2RlIjoiZ3JhcGggVERcbiAgZ2Fucm9iW1Byb2plY3QgU3RydWN0dXJlXSAtLT4gUGlcbiAgZ2Fucm9iIC0tPiBBcmR1aW5vXG5cbiAgUGkgLS0-IEIocGlHYW50cnkpXG4gIEIgLS0-IEMoaW1hZ2VQcm9jZXNzKVxuICBCIC0tPiBEKHBpU2VyaWFsKVxuXG5cbiAgRCAtLT4gRShbc2VyaWFsSW50ZXIucHldKVxuICBEIC0tPiBGKFtUa0ludGVyVUkucHldKVxuICBGIC0tPiBFXG5cbiAgICBBcmR1aW5vIC0tPiBsb2NvKFthcmR1aW5vTW90b3IuaW5vXSlcblx0XHQiLCJtZXJtYWlkIjp7InRoZW1lIjoiZGVmYXVsdCJ9fQ)