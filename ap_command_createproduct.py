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
import ap_product

PYVERSION =  sys.version_info[0]

#==============================================================================
toolTip = \
'''
Create a product(assembly)
within an empty file
'''

class ap_createProduct_command():

    def GetResources(self):
        return {'Pixmap'  : ap_lib.pathOfModule()+'/icons/ap_Asm.svg',
                'Accel' : "Shift+A", # a default shortcut (optional)
                'MenuText': "Create a product(assembly) within an empty file",
                'ToolTip' : toolTip
                }

    def Activated(self):
        print(u"ap_createProduct activated")
        doc = FreeCAD.activeDocument()
        selection = [s for s in FreeCADGui.Selection.getSelectionEx() if s.Document == doc ]
        if len(selection) > 0:
            selOb = selection[0]
            if hasattr(selOb,'type') and selOb.type == 'ap_product':
                component = doc.addObject("Part::FeaturePython",'Product')
                ap_product.ap_product(component)
                if FreeCAD.GuiUp:
                    ap_product.vp_ap_product(component.ViewObject)
                selOb.addObject(component)
                component.purgeTouched()
        else:
            print("adding a component failed!")

    def IsActive(self):
        doc = FreeCAD.activeDocument()
        if doc == None: return False
        if len(doc.Objects) > 0: return False # doc is not empty
        return True



FreeCADGui.addCommand('ap_createProduct_command',ap_createProduct_command())
#==============================================================================

