"""pydiskinfo Partition class definition

Copyright (c) 2022 Lars Henrik Ericson

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from human_readable_units import human_readable_units


class Partition(dict):
    """Contains information about partitions. This includes logical disk, 
    or 'volume' information. The same volume may span several disks, and the 
    filesystem of the partition, will in those cases be the filesystem of the 
    spanned volume. The partition may in that case not include a functional 
    filesystem on its own, though its contents will be part of one.
    """

    def __init__(self, physical_disk: 'PhysicalDisk') -> None:
        self['Physical Disk'] = physical_disk
        self['Logical Disks'] = []
        self['Blocksize'] = -1
        self['Bootable'] = False
        self['Boot Partition'] = False
        self['Description'] = ""
        self['Path'] = ""
        self['Device I.D.'] = ""
        self['Disk Number'] = -1
        self['Partition Number'] = -1
        self['Number of Blocks'] = -1
        self['Primary Partition'] = False
        self['Size'] = 0
        self['Starting Offset'] = -1
        self['Type'] = ""

    def add_logical_disk(self, logical_disk: 'LogicalDisk') -> None:
        """Set the logical disk connected to this partition."""
        new_logical_disk = True
        for each_logical_disk in self['Logical Disks']:
            if each_logical_disk['Device I.D.'] == logical_disk['Device I.D.']:
                new_logical_disk = False
        if new_logical_disk:
            self['Logical Disks'].append(logical_disk)

    def __str__(self) -> str:
        """overloading the __str__ method"""
        partition = 'Partition -- ' + ", ".join(('ID: ' + self['Device I.D.'], 
                                               'Type: ' + self['Type'], 
                                               'Size: ' + human_readable_units(self['Size']), 
                                               'Offset: '+ str(self['Starting Offset'])
                                               ))
        logical_disks = ["\n".join(["  " + line for line in str(logical_disk).split("\n")]) for logical_disk in self['Logical Disks']] 
        return "\n".join((partition, *logical_disks))


class LinuxPartition(Partition):
    def __init__(self, disk: 'PhysicalDisk') -> None:
        super().__init__(disk)

class WindowsPartition(Partition):
    def __init__(self, partition: 'wmi._wmi_object', disk: 'PhysicalDisk') -> None:
        super().__init__(disk)
        self._set_blocksize(partition)
        self._set_bootable(partition)
        self._set_boot_partition(partition)
        self._set_description(partition)
        self._set_device_id(partition)
        self._set_disk_number(partition)
        self._set_partition_number(partition)
        self._set_number_of_blocks(partition)
        self._set_primary_partition(partition)
        self._set_size(partition)
        self._set_starting_offset(partition)
        self._set_type(partition)

    def _set_blocksize(self, partition: 'wmi._wmi_object') -> None:
        """Set blocksize or -1 if it fails."""
        try:
            self['BlockSize'] = int(partition.BlockSize)
        except AttributeError:
            self['BlockSize'] = -1
        except ValueError:
            self['BlockSize'] = -1

    def _set_bootable(self, partition: 'wmi._wmi_object') -> None:
        """Set bootable or false if it fails."""
        try:
            self['Bootable'] = partition.Bootable
        except AttributeError:
            self['Bootable'] = False

    def _set_boot_partition(self, partition: 'wmi._wmi_object') -> None:
        """Set if system boot partition, or False if it fails."""
        try:
            self['Boot Partition'] = partition.BootPartition
        except AttributeError:
            self['Boot Partition'] = False

    def _set_description(self, partition: 'wmi._wmi_object') -> None:
        """set a description provided by the system."""
        try:
            self['Description'] = partition.Description
        except AttributeError:
            self['Description'] = ""

    def _set_device_id(self, partition: 'wmi._wmi_object') -> None:
        """set the device id provided by the system."""
        try:
            self['Device I.D.'] = partition.DeviceID
        except AttributeError:
            self['Device I.D.'] = ""

    def _set_disk_number(self, partition: 'wmi._wmi_object') -> None:
        """Set the disk index number as the system sees it."""
        try:
            self['Disk Number'] = int(partition.DiskIndex)
        except AttributeError:
            self['Disk Number'] = -1
        except ValueError:
            self['Disk Number'] = -1

    def _set_partition_number(self, partition: 'wmi._wmi_object') -> None:
        """Set the partition index on the disk, according to the system."""
        try:
            self['Partition Number'] = int(partition.Index)
        except AttributeError:
            self['Partition Number'] = -1
        except ValueError:
            self['Partition Number'] = -1

    def _set_number_of_blocks(self, partition: 'wmi._wmi_object') -> None:
        """Set number of blocks."""
        try:
            self._number_of_blocks = int(partition.NumberOfBlocks)
        except AttributeError:
            self._number_of_blocks = -1
        except ValueError:
            self._number_of_blocks = -1

    def _set_primary_partition(self, partition: 'wmi._wmi_object') -> None:
        """Set if the partition is a primary partition"""
        try:
            self['Primary Partition'] = int(partition.PrimaryPartition)
        except AttributeError:
            self['Primary Partition'] = False

    def _set_size(self, partition: 'wmi._wmi_object') -> None:
        """Set partition size in bytes."""
        try:
            self['Size'] = int(partition.Size)
        except AttributeError:
            self['Size'] = 0
        except ValueError:
            self['Size'] = 0

    def _set_starting_offset(self, partition: 'wmi._wmi_object') -> None:
        """Set partition starting offset in bytes."""
        try:
            self['Starting Offset'] = int(partition.StartingOffset)
        except AttributeError:
            self['Starting Offset'] = -1
        except ValueError:
            self['Starting Offset'] = -1

    def _set_type(self, partition: 'wmi._wmi_object') -> None:
        """Set partition type."""
        try:
            self['Type'] = partition.Type
        except AttributeError:
            self['Type'] = ""


