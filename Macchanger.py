import subprocess
import optparse
import re


# creating options and check the necessary options entered or not
def get_options():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest='interface', help='select the interface')
    parser.add_option('-m', '--mac', dest='mac', help='select the mac address')
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("Interface is not specified! --help for more info")
    elif not options.mac:
        parser.error("Mac address is not specified! --help for more info")
    else:
        return options


# Running necessary shell commands to change the mac address
def mac_change(interface, mac):
    subprocess.call(['sudo', 'ifconfig', interface, 'down'])
    subprocess.call(['sudo', 'ifconfig', interface, 'hw', 'ether', mac])
    subprocess.call(['sudo', 'ifconfig', interface, 'up'])


# matching the mac address patterns and return the mac address
def get_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    filter_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if filter_result:
        return filter_result.group(0)
    else:
        print("MAC address is not found")


# Get options
options = get_options()

# call get_mac function
mac_filter_result = get_mac(options.interface)

# call mac_change function
mac_change(options.interface, options.mac)

# printing successful or error message
if mac_filter_result == options.mac:
    print("Your current MAC address is changed to:"+options.mac)
else:
    print("Some problems may occur")