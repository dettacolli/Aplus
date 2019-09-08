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
def activateImportFile(workingDoc,workingComponent,fileName):
    importDocIsOpen = False
    requestedFile = os.path.split(fileName)[1]
    for d in FreeCAD.listDocuments().values():
        recentFile = os.path.split(d.FileName)[1]
        print(recentFile)
        if requestedFile == recentFile:
            importDoc = d # file is already open...
            importDocIsOpen = True
            break
    
    if not importDocIsOpen:
        FreeCAD.open(fileName)
    else:
        name = importDoc.Name
        # Search and activate the corresponding document window..
        mw=FreeCADGui.getMainWindow()
        mdi=mw.findChild(QtGui.QMdiArea)
        sub=mdi.subWindowList()
        for s in sub:
            mdi.setActiveSubWindow(s)
            if FreeCAD.activeDocument().Name == name: break
            
    FreeCADGui.Selection.clearSelection()
#==============================================================================
toolTip = \
'''
Add a part from an external file
to the assembly
'''

class ap_importPart_command(QtGui.QDialog):

    def __init__(self):
        super(ap_importPart_command,self).__init__()

    def GetResources(self):
        return {'Pixmap'  : ap_lib.pathOfModule()+'/icons/ap_ImportPart.svg',
                'Accel' : "Shift+A", # a default shortcut (optional)
                'MenuText': "Add a part from an external file",
                'ToolTip' : toolTip
                }

    def Activated(self):
        doc = FreeCAD.activeDocument()
        selection = [s for s in FreeCADGui.Selection.getSelectionEx() if s.Document == doc ]
        if len(selection) > 0:
            selOb = selection[0].Object
            try:
                if selOb.Proxy.type == 'ap_product':
                    dialog = QtGui.QFileDialog(
                        QtGui.QApplication.activeWindow(),
                        "Select FreeCAD document to import part from"
                        )
                    # set option "DontUseNativeDialog"=True, as native Filedialog shows
                    # misbehavior on Unbuntu 18.04 LTS. It works case sensitively, what is not wanted...
                    dialog.setOption(QtGui.QFileDialog.DontUseNativeDialog, True)        
                    dialog.setNameFilter("Supported Formats (*.FCStd *.stp *.step);;All files (*.*)")
                    if dialog.exec_():
                        if PYVERSION < 3:
                            filename = unicode(dialog.selectedFiles()[0])
                        else:
                            filename = str(dialog.selectedFiles()[0])
                    else:
                        return
                    component = doc.addObject("Part::FeaturePython",'Component')
                    ap_component.ap_component(component)
                    if FreeCAD.GuiUp:
                        ap_component.vp_ap_component(component.ViewObject)
                    selOb.addObject(component)
                    selOb.purgeTouched()
                    component.SourceFile = filename
                    self.workingDoc = doc
                    self.workingComponent = component
                    self.fileName = filename
                    self.addLinkToComponent()
                    self.drawUI()
                    self.show()
                    component.purgeTouched()
                    return
            except:
                pass
        QtGui.QMessageBox.information(
            QtGui.QApplication.activeWindow(),
           u"Message",
           u'''First create and select a product object'''
           )
    
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

    def addLinkToComponent(self):
        activateImportFile(self.workingDoc, self.workingComponent, self.fileName) #non member func for later reuse
        
    def switchBackDocument(self):
        name = self.workingDoc.Name
        # Search and activate the corresponding document window..
        mw=FreeCADGui.getMainWindow()
        mdi=mw.findChild(QtGui.QMdiArea)
        sub=mdi.subWindowList()
        for s in sub:
            mdi.setActiveSubWindow(s)
            if FreeCAD.activeDocument().Name == name: break
        
    def onCancel(self):
        self.switchBackDocument()
        self.close()
    
    def onOK(self):
        doc = FreeCAD.activeDocument()
        selection = [s for s in FreeCADGui.Selection.getSelectionEx() if s.Document == doc ]
        self.switchBackDocument()
        link = self.workingComponent.newObject("App::Link","LinkObj")
        link.LinkedObject = selection[0].Object
        link.recompute()
        self.close()
        
    def drawUI(self):
        self.setModal(False)
        self.setWindowFlags( QtCore.Qt.WindowStaysOnTopHint )
        self.setWindowTitle('Insert a Link')
        self.setMinimumSize(400, 150)
        self.resize(400,150)
        
        # label
        self.labelMain = QtGui.QLabel(self)
        self.labelMain.setText("Select exactly one object to be linked\nand hit the OK-Button")
        self.labelMain.move(10,20)
        #self.Layout.addWidget(self.labelMain)
        
        # Cancel button
        self.CancelBtn = QtGui.QPushButton('Cancel', self)
        self.CancelBtn.setAutoDefault(False)
        self.CancelBtn.move(10, 100)

        # create Link button
        self.okBtn = QtGui.QPushButton('OK', self)
        self.okBtn.move(285, 100)
        self.okBtn.setDefault(True)
        
        self.CancelBtn.clicked.connect(self.onCancel)
        self.okBtn.clicked.connect(self.onOK)
        
        
        


FreeCADGui.addCommand('ap_importPart_command',ap_importPart_command())
#==============================================================================

