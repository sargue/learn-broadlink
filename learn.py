import sys

import broadlink
import json
import time
import base64

from broadlink.exceptions import ReadError, StorageError

TIMEOUT = 30


# noinspection PyUnresolvedReferences
def learn_command():
    device.enter_learning()
    start = time.time()
    while time.time() - start < TIMEOUT:
        time.sleep(0.5)
        try:
            return base64.b64encode(device.check_data()).decode('ascii')
        except (ReadError, StorageError):
            continue
    else:
        print("No data received...")
        return ''


def input_list(prompt_name, property_name):
    input_string = input(f'Enter {prompt_name} separated by commas, or leave empty to auto-detect: ')
    if len(input_string) == 0:
        return list(data[property_name])
    else:
        return input_string.split(',')


def learn_commands(operation_mode, fan_mode, swing_mode, temp_range):
    if operation_mode not in commands:
        commands[operation_mode] = {}
    if fan_mode not in commands[operation_mode]:
        commands[operation_mode][fan_mode] = {}
    if swing_mode not in commands[operation_mode][fan_mode]:
        commands[operation_mode][fan_mode][swing_mode] = {}
    else:
        if auto_resume_mode or \
           input(f'It seems you already have the definition for "{operation_mode}", "{fan_mode}" fan and '
                 f'"{swing_mode}" swing mode. Do you want to skip to the next step? (y/[n]) ') == 'y':
            return

    response = input(f'Prepare remote for learning, starting at {temp_range[0]}º. '
                     f'Enter "s" if this mode has no temperature selection (e.g. fan mode). Continue? ([y]/n/s) ')
    if response == 'n':
        exit()
    if response == 's':
        print(f'Waiting for command')
        base64command = learn_command()
        for temp in temp_range:
            commands[operation_mode][fan_mode][swing_mode][str(temp)] = base64command
    else:
        for temp in temp_range:
            print(f'Waiting for command for temperature {temp}')
            base64command = learn_command()
            commands[operation_mode][fan_mode][swing_mode][str(temp)] = base64command


def main():
    if auto_resume_mode:
        operation_modes = list(data['operationModes'])
        fan_modes = list(data['fanModes'])
        swing_modes = list(data['swingModes'])
    else:
        operation_modes = input_list('operation modes', 'operationModes')
        print(f'Will learn this operation modes: {operation_modes}')
        fan_modes = input_list('fan modes', 'fanModes')
        print(f'Will learn this fan modes: {fan_modes}')
        swing_modes = input_list('swing modes', 'swingModes')
        print(f'Will learn this swing modes: {swing_modes}')

    min_temperature = data['minTemperature']
    max_temperature = data['maxTemperature']
    temp_range = list(range(min_temperature, max_temperature + 1))

    for operation_mode in operation_modes:
        for fan_mode in fan_modes:
            for swing_mode in swing_modes:
                print(
                    f'Learning for mode {operation_mode}, fan {fan_mode}, swing {swing_mode}')
                learn_commands(operation_mode, fan_mode, swing_mode, temp_range)
                temp_range = list(reversed(temp_range))


if len(sys.argv) < 2:
    device_ip = input('Please enter the IP address of your Broadlink device: ')
else:
    device_ip = sys.argv[1]

device = broadlink.hello(device_ip)
print(device)
device.auth()

with open('smartir.json') as f:
    data = json.load(f)

commands = data['commands']
try:
    auto_resume_mode = input('Do you want to resume where you left? (y/n) ') == 'y' if data['commands'] != {} else False
    main()

    print('Waiting for the OFF command...')
    commands['off'] = learn_command()

finally:
    with open('smartir.json', 'w') as f:
        json.dump(data, f, indent=4)
