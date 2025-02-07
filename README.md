Pinmux Helper for i.MX6
=======================

The pinctrl in devicetrees for i.MX processors always follows the pattern

<PAD_NAME>__<ALTERNATE_FUNCTION>     <Drive Characteristics>

While Pad Name and Alternate Function are somewhat human-readable, the drive Characteristics is usually expressed as hex value.

This script implements some very simple parsing of this and also provides a simple generator for the Drive Characteristics.

Please use the `-h` flag for a full help.

Sidenotes
---------

 - please read the iomuxc datasheet for a more precise definition of the meaning and combination of the flags parsed from the device tree. You find it in the i.MX6Q datasheet.
 - This is just a very simple tool that I hacked in some few minutes, please review its output carefully and do not blindly rely on it.
 - There is no full database of pinmux options included in this tool, it can currently only generate the drive characteristics as hex

Contribution
------------

Contributions and fixes are welcome, please register a pull request.

License
-------

This tool is licensed under the MIT license, please see [LICENSE] for the complete license text.

