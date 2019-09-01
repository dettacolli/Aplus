# -*- coding: utf-8 -*-
#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2018 kbwbe                                              *
#*                                                                         *
#*   Portions of code based on hamish's assembly 2                         *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************

__title__ = 'Aplus assembly Workbench - InitGui file'
__author__ = 'kbwbe'

AP_VERSION = 'V0.1'



import sys
PyVersion = sys.version_info[0]
if PyVersion == 2:
    import ap_Resources2
else:
    import ap_Resources3


class AplusWorkbench (Workbench):

    def __init__(self):
        global AP_VERSION
        import ap_lib
        self.__class__.Icon = ap_lib.pathOfModule() + "/icons/ap_Workbench.svg"
        self.__class__.MenuText = 'Aplus '+AP_VERSION
        self.__class__.ToolTip  = 'An other assembly workbench for FreeCAD'


    def Initialize(self):
        import sys
        PyVersion = sys.version_info[0]
        if PyVersion == 2:
            import ap_Resources2
        else:
            import ap_Resources3
        import ap_lib
        import ap_command_createproduct
        import ap_command_importpart

        partCommands = [
            'ap_createProduct_command',
            'ap_importPart_command',
            ]

        self.appendToolbar(
               'ap_Part',
               partCommands
               )

        commandslist = list()
        commandslist.extend(partCommands)

        self.appendMenu(
            'Aplus',
            commandslist
            )

        FreeCADGui.addIconPath(':/icons')
        
        FreeCADGui.addPreferencePage(
            ap_lib.pathOfModule() +
            '/GuiAp/Resources/ui/ap_prefs.ui','Aplus'
            )


    def Activated(self):
        pass

    def Deactivated(self):
        pass

    def ContextMenu(self, recipient):
        self.appendContextMenu(
            "Aplus",
            [
              ]
            )

Gui.addWorkbench(AplusWorkbench())
