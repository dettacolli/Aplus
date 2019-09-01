#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2019 kbwbe                                              *
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

import FreeCADGui,FreeCAD
from PySide import QtGui, QtCore
import os, copy, time, sys, platform
import ap_lib
import ap_component

PYVERSION =  sys.version_info[0]

#==============================================================================
toolTip = \
'''
Add a part from an external file
to the assembly
'''

class ap_importPart_command():

    def GetResources(self):
        return {'Pixmap'  : ap_lib.pathOfModule()+'/icons/ap_ImportPart.svg',
                'Accel' : "Shift+A", # a default shortcut (optional)
                'MenuText': "Add a part from an external file",
                'ToolTip' : toolTip
                }

    def Activated(self):
        print(u"importPartCommand activated")
        doc = FreeCAD.activeDocument()
        newObj = doc.addObject("Part::FeaturePython",'Component')
        ap_component.ap_component(newObj)
        if FreeCAD.GuiUp:
            ap_component.vp_ap_component(newObj.ViewObject)
        newObj.purgeTouched()

    def IsActive(self):
        doc = FreeCAD.activeDocument()
        if doc == None: return False
        countProducts = 0
        for ob in doc.Objects:
            if ob.Name.startswith('Product'):
                countProducts += 1
        if countProducts == 1: 
            return True
        else:
            return False

    def GuiViewFit(self):
        FreeCADGui.SendMsgToActiveView("ViewFit")


FreeCADGui.addCommand('ap_importPart_command',ap_importPart_command())
#==============================================================================

