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

import FreeCAD
import FreeCADGui
from FreeCAD import Base
import  Part
from PySide import QtGui
from PySide import QtCore
import os
import sys
import copy
import platform
import numpy

PYVERSION =  sys.version_info[0]

preferences = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Aplus")

#USE_PROJECTFILE = preferences.GetBool('useProjectFolder', False)
DEBUGPROGRAM = 1

path_ap = os.path.dirname(__file__)
path_ap_resources = os.path.join( path_ap, 'GuiAp', 'Resources', 'resources.rcc')
resourcesLoaded = QtCore.QResource.registerResource(path_ap_resources)
assert resourcesLoaded


#------------------------------------------------------------------------------
# Detect the operating system...
#------------------------------------------------------------------------------
tmp = platform.system()
tmp = tmp.upper()
tmp = tmp.split(' ')

OPERATING_SYSTEM = 'UNKNOWN'
if "WINDOWS" in tmp:
    OPERATING_SYSTEM = "WINDOWS"
elif "LINUX" in tmp:
    OPERATING_SYSTEM = "LINUX"
else:
    OPERATING_SYSTEM = "OTHER"
#------------------------------------------------------------------------------
def to_bytes(tx):
    if PYVERSION > 2:
        if isinstance(tx, str):
            value = tx.encode("utf-8")
        else:
            value = tx
    else:
        if isinstance(tx,unicode):
            value = tx.encode("utf-8")
        else:
            value = tx
    return value # Instance of bytes
#------------------------------------------------------------------------------
def to_str(tx):
    if PYVERSION > 2:
        if isinstance(tx, bytes):
            value = tx.decode("utf-8")
        else:
            value = tx
    else:
        if isinstance(tx, unicode):
            value = tx
        else:
            value = tx.decode("utf-8")
    return value # Instance of unicode string
#------------------------------------------------------------------------------
def appVersionStr():
    version = int(FreeCAD.Version()[0])
    subVersion = int(float(FreeCAD.Version()[1]))
    return "%03d.%03d" %(version,subVersion)
#------------------------------------------------------------------------------
def numpyVecToFC(nv):
    assert len(nv) == 3
    return Base.Vector(nv[0],nv[1],nv[2])
#------------------------------------------------------------------------------
def fit_plane_to_surface1( surface, n_u=3, n_v=3 ):
    uv = sum( [ [ (u,v) for u in numpy.linspace(0,1,n_u)] for v in numpy.linspace(0,1,n_v) ], [] )
    P = [ surface.value(u,v) for u,v in uv ] #positions at u,v points
    N = [ numpy.cross( *surface.tangent(u,v) ) for u,v in uv ] 
    plane_norm = sum(N) / len(N) #plane's normal, averaging done to reduce error
    plane_pos = P[0]
    error = sum([ abs( numpy.dot(p - plane_pos, plane_norm) ) for p in P ])
    return numpyVecToFC(plane_norm), numpyVecToFC(plane_pos), error
#------------------------------------------------------------------------------
def pathOfModule():
    return os.path.dirname(__file__)
#------------------------------------------------------------------------------
def Msg(tx):
    FreeCAD.Console.PrintMessage(tx)
#------------------------------------------------------------------------------
def DebugMsg(level, tx):
    if A2P_DEBUG_LEVEL >= level:
        FreeCAD.Console.PrintMessage(tx)
#------------------------------------------------------------------------------
def findUnusedObjectName(base, counterStart=1, fmt='%03i', document=None):
    if document == None:
        document = FreeCAD.ActiveDocument
    i = counterStart
    usedNames = [ obj.Name for obj in document.Objects ]

    if base[-4:-3] == '_':
        base2 = base[:-4]
    else:
        base2 = base
    base2 = base2 + '_'

    objName = '%s%s' % (base2, fmt%i)
    while objName in usedNames:
        i += 1
        objName = '%s%s' % (base2, fmt%i)
    return objName
#------------------------------------------------------------------------------
def findUnusedObjectLabel(base, counterStart=1, fmt='%03i', document=None):
    if document == None:
        document = FreeCAD.ActiveDocument
    i = counterStart
    usedLabels = [ obj.Label for obj in document.Objects ]

    if base[-4:-3] == '_':
        base2 = base[:-4]
    else:
        base2 = base
    base2 = base2 + '_'

    objLabel = '%s%s' % (base2, fmt%i)
    while objLabel in usedLabels:
        i += 1
        objLabel = '%s%s' % (base2, fmt%i)
    return objLabel
#------------------------------------------------------------------------------

