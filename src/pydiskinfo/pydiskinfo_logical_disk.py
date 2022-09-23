"""pydiskinfo LogicalDisk class definition

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

class LogicalDisk(dict):
    """Class for logical disks/mount points"""    

    def __init__(self, system: 'System') -> None:
        self['System'] = system
        self['Partitions'] = []
        self['Description'] = ""
        self['Device I.D.'] = ""
        self['Drive Type'] = ""
        self['File System'] = ""
        self['Free Space'] = 0
        self['Maximum Component Length'] = -1
        self['Name'] = ""
        self['Path'] = ""
        self['Size'] = 0
        self['Volume Name'] = ""
        self['Volume Serial Number'] = ""

    def add_partition(self, partition: 'Partition') -> None:
        """Add a partition to this logical disk"""
        self['Partitions'].append(partition)
    
    def __str__(self) -> str:
        return "Logical Disk -- " + ", ".join(("Path: " + self['Path'], 
                                             'Volume Name: ' + self['Volume Name'],
                                             'File System: ' + self['File System'],
                                             'Free Space: ' + human_readable_units(self['Free Space'])
                                           ))


class LinuxLogicalDisk(LogicalDisk):
    def __init__(self, system: object) -> None:
        super().__init__(system)

class WindowsLogicalDisk(LogicalDisk):
    _DRIVETYPES = [ 'Unknown', 
                    'No Root Directory', 
                    'Removable Disk', 
                    'Local Disk', 
                    'Network Drive', 
                    'Compact Disk',
                    'RAM Disk'
                    ]

    def __init__(self, logical_disk: 'wmi._wmi_object', system: 'System') -> None:
        super().__init__(system)
        self._set_description(logical_disk)
        self._set_device_id_and_path_and_name(logical_disk)
        self._set_drive_type(logical_disk)
        self._set_file_system(logical_disk)
        self._set_free_space(logical_disk)
        self._set_maximum_component_length(logical_disk)
        self._set_size(logical_disk)
        self._set_volume_name(logical_disk)
        self._set_volume_serial_number(logical_disk)
    
    def _set_description(self, logical_disk: 'wmi._wmi_object') -> None:
        """Set the description"""
        try:
            self['Description'] = logical_disk.Description
            if not type(self['Description']) == str:
                self['Description'] = ""
        except AttributeError:
            self['Description'] = ""

    def _set_device_id_and_path_and_name(self, logical_disk: 'wmi._wmi_object') -> None:
        """Set the unique device ID and name. On windows this is pretty much the same as path."""
        try:
            self['Device I.D.'] = logical_disk.DeviceID
            if not type(self['Device I.D.']) == str:
                self['Device I.D.'] = ""
        except AttributeError:
            self['Device I.D.'] = ""
        self['Name'] = self['Device I.D.']
        self['Path'] = self['Device I.D.'] + "\\"

    def _set_drive_type(self, logical_disk: 'wmi._wmi_object') -> None:
        """Set the drive type."""
        try:
            drivetype = int(logical_disk.DriveType)
        except AttributeError:
            drivetype = 0
        except ValueError:
            drivetype = 0
        try:
            self['Drive Type'] = self._DRIVETYPES[drivetype]
        except IndexError:
            self['Drive Type'] = self._DRIVETYPES[0]

    def _set_file_system(self, logical_disk: 'wmi._wmi_object') -> None:
        """Set the filesystem according to the system."""
        try:
            self['File System'] = logical_disk.FileSystem
            if type(self['File System']) != str:
                self['File System'] = "unknown"
        except AttributeError:
            self['File System'] = "unknown"

    def _set_free_space(self, logical_disk: 'wmi._wmi_object') -> None:
        """Set the available space on the filesystem in bytes"""
        try:
            self['Free Space'] = int(logical_disk.FreeSpace)
        except AttributeError:
            self['Free Space'] = 0
        except ValueError:
            self['Free Space'] = 0
        except TypeError:
            self['Free Space'] = 0

    def _set_maximum_component_length(self, logical_disk: 'wmi._wmi_object') -> None:
        """Set the max path length in characters."""
        try:
            self['Maximum Component Length'] = int(logical_disk.MaximumComponentLength)
        except AttributeError:
            self['Maximum Component Length'] = 0
        except ValueError:
            self['Maximum Component Length'] = 0
        except TypeError:
            self['Maximum Component Length'] = 0

    def _set_size(self, logical_disk: 'wmi._wmi_object') -> None:
        """Set the size in bytes."""
        try:
            self['Size'] = int(logical_disk.Size)
        except AttributeError:
            self['Size'] = 0
        except ValueError:
            self['Size'] = 0
        except TypeError:
            self['Size'] = 0

    def _set_volume_name(self, logical_disk: 'wmi._wmi_object') -> None:
        """Set the volume name. Usually the Label value."""
        try:
            self['Volume Name'] = logical_disk.VolumeName
            if type(self['Volume Name']) != str:
                self['Volume Name'] = ""
        except AttributeError:
            self['Volume Name'] = ""

    def _set_volume_serial_number(self, logical_disk: 'wmi._wmi_object') -> None:
        """Set the volume serial number."""
        try:
            self['Volume Serial Number'] = logical_disk.VolumeSerialNumber
            if type(self['Volume Serial Number']) != str:
                self['Volume Serial Number'] = ""
        except AttributeError:
            self['Volume Serial Number'] = ""


