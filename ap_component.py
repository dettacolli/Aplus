#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2019 kbwbe                                              *
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


# This is the definition of an ap_product object ( what is an assembly )

import FreeCAD
import FreeCADGui

#==============================================================================
class ap_component(object):
    def __init__(self, obInstance):
        obInstance.addExtension('App::LinkExtensionPython', self)
        
        ap_component.setProperties(self,obInstance)
        self.type = "ap_component"

    def setProperties(self,obj):
        propList = obj.PropertiesList
        #if not "a2p_Version" in propList:
        #    obj.addProperty("App::PropertyString", "a2p_Version", "importPart")
        #    obj.a2p_Version = A2P_VERSION
        self.type = "ap_component"

    def onDocumentRestored(self,obj):
        ap_component.setProperties(self,obj)
        self.type = "ap_component"
        
    def execute(self, obj):
        pass
    
    def onChanged(self, obj, prop):
        pass
            
#==============================================================================
class vp_ap_component(object):
    def __init__(self,vobj):
        #vobj.addExtension('Gui::ViewProviderGeoFeatureGroupExtensionPython', self)
        #vobj.addExtension('Gui::ViewProviderLinkExtensionPython', self)
        #vobj.addExtension('Gui::ViewProviderLinkPython', self)
        vobj.Proxy = self

    def attach(self, vobj):
        self.ViewObject = vobj
        self.Object = vobj.Object
        
        # restore lost functions to featurePython object during reload
        #if not hasattr(self.Object,'deleteContent'):
        #    pass
        #    self.Object.deleteContent = ap_product_deleteContent

    def onDelete(self, viewObject, subelements): # subelements is a tuple of strings
        if FreeCAD.activeDocument() != viewObject.Object.Document:
            return False # only delete objects in the active Document anytime !!
        return True

    def getIcon(self):
        return ":/icons/ap_Obj.svg"

    def __getstate__(self):
        return None

    def __setstate__(self,state):
        return None

#==============================================================================
