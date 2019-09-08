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
def ap_product_deleteContent(_self,doc):
    '''
    ap_product featurepython extending function deleteContent
    '''
    if len(_self.Group) > 0:
        deleteList = []
        deleteList.extend(_self.Group)
        _self.Group = []
        for ob in deleteList:
            doc.removeObject(ob.Name) # delete all components of the assembly'

#==============================================================================
class ap_product(object):
    def __init__(self, obInstance):
        obInstance.addExtension('App::GeoFeatureGroupExtensionPython', self)
        obInstance.deleteContent = ap_product_deleteContent # add a function to this featurepython class
        ap_product.setProperties(self,obInstance)
        obInstance.Proxy = self
        self.type = "ap_product"

    def setProperties(self,obj):
        propList = obj.PropertiesList
        #if not "ap_type" in propList:
        #    obj.addProperty("App::PropertyString", "ap_type")
        #    obj.ap_type = "ap_product"
        self.type = "ap_product"

    def onDocumentRestored(self,obj):
        ap_product.setProperties(self,obj)
        
    def execute(self, obj):
        pass
    
    def onChanged(self, obj, prop):
        pass
            
#==============================================================================
class vp_ap_product(object):
    def __init__(self,vobj):
        vobj.addExtension('Gui::ViewProviderGeoFeatureGroupExtensionPython', self)
        vobj.Proxy = self

    def attach(self, vobj):
        self.ViewObject = vobj
        self.Object = vobj.Object
        
        # restore lost functions to featurePython object during reload
        if not hasattr(self.Object,'deleteContent'):
            self.Object.deleteContent = ap_product_deleteContent

    def onDelete(self, viewObject, subelements): # subelements is a tuple of strings
        if FreeCAD.activeDocument() != viewObject.Object.Document:
            return False # only delete objects in the active Document anytime !!
        obj = viewObject.Object
        doc = obj.Document
        obj.deleteContent(doc) # Clean up this group complete with all content
        return True

    def getIcon(self):
        return ":/icons/ap_Asm.svg"

    def __getstate__(self):
        return None

    def __setstate__(self,state):
        return None

#==============================================================================
