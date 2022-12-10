# Broadlink IR Remote Learning

This is a Python script that can be used to learn the IR commands for a Broadlink RM2/RM3/RM Pro+ device.
The script will ask you to enter the IP address of your device, and then guide you through the process of 
learning each of the commands for your air conditioner or other IR-controlled device.

Its purpose is to automate the creation of a new JSON file for the 
[smartir Home Assistant integration](https://github.com/smartHomeHub/SmartIR), specifically for
[climate devices](https://github.com/smartHomeHub/SmartIR/blob/master/docs/CLIMATE.md).

## Requirements

- A Broadlink RM device
- Python 3
- The `broadlink` Python package

## Setup

First you will need to install the required packages. It is recommended to use a Python virtual environment.
Then just run `pip install -r requirements.txt`.

You will need the IP address of your Broadlink device. You can get that from your DHCP server or by
using the `broadlink_discovery` command from the 
[`python_broadlink` library](https://github.com/mjg59/python-broadlink/tree/master/cli).

## Configuration

Create a `smartir.json` file using the `template.json` as a template. Adjust the temperature range, 
manufacturer, model and operating, fan and swing modes.

## Usage

To use the script, run it from the command line and pass the IP address of your Broadlink device as the 
first argument. For example:

``
python learn.py 192.168.0.100
``

The script will then guide you through the process of learning each of the commands for your device. It will 
ask you to prepare the remote for learning, and then wait for you to press the appropriate button on the 
remote. Once it receives the command, it will store it and move on to the next command.

## Output

As the script learns the commands for your device it will keep updating the `smartir.json` file. You
can then use this file for the `smartir` integration.

## References

* [`python_broadlink` library](https://github.com/mjg59/python-broadlink/)
* [Home Assistant Broadlink integration](https://www.home-assistant.io/integrations/broadlink/)
* [smartir Home Assistant integration](https://github.com/smartHomeHub/SmartIR)
