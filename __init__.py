#-----------------------------------------------------------
# Copyright (C) 2015 Martin Dobias
#-----------------------------------------------------------
# Licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#---------------------------------------------------------------------

from PyQt5.QtWidgets import QAction, QMessageBox
from PyQt5.QtGui import QColor as QColor
#import PyQt5.QtGui.QColor

import os # This is is needed in the pyqgis console also
from qgis.core import *
import qgis.utils
from qgis.core import QgsProject
from qgis.core import (
QgsVectorLayer
)
from qgis.core import (
QgsRasterLayer,
QgsColorRampShader,
QgsSingleBandPseudoColorRenderer
)

def classFactory(iface):
    return MinimalPlugin(iface)


class MinimalPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.project = QgsProject.instance()

    def initGui(self):
        self.action = QAction('Init_data!', self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)

        self.action2=QAction('Convert to colormap!', self.iface.mainWindow())
        self.action2.triggered.connect(self.colormap)
        self.iface.addToolBarIcon(self.action2)

        self.action3=QAction('Add points!', self.iface.mainWindow())
        self.action3.triggered.connect(self.points)
        self.iface.addToolBarIcon(self.action3)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def run(self):
        self.project.read('C:/Users/william/Documents/Qgis/example.qgs')
        #project = QgsProject.instance()
        path_to_tif = os.path.join(QgsProject.instance().homePath(), "qgis_sample_data", "raster", "SR_50M_alaska_nad.TIF")
        self.rlayer = QgsRasterLayer(path_to_tif)
        if not self.rlayer.isValid():
            print("Layer failed to load!")
        QgsProject.instance().addMapLayer(self.rlayer)


        QMessageBox.information(None, 'Example:', 'Data is loaded!')

    def colormap(self):
        self.project.read('C:/Users/william/Documents/Qgis/example.qgs')
        #project = QgsProject.instance()
        path_to_tif = os.path.join(QgsProject.instance().homePath(), "qgis_sample_data", "raster", "SR_50M_alaska_nad.TIF")
        self.rlayer = QgsRasterLayer(path_to_tif)
        fcn = QgsColorRampShader()
        fcn.setColorRampType(QgsColorRampShader.Interpolated)
        lst = [ QgsColorRampShader.ColorRampItem(0, QColor(0,25,25)),
        QgsColorRampShader.ColorRampItem(255, QColor(255,255,0)) ]
        fcn.setColorRampItemList(lst)
        shader = QgsRasterShader()
        shader.setRasterShaderFunction(fcn)
        renderer = QgsSingleBandPseudoColorRenderer(self.rlayer.dataProvider(), 1, shader)
        self.rlayer.setRenderer(renderer)
        QgsProject.instance().addMapLayer(self.rlayer)
        QgsProject.instance().layerTreeRoot()
        QMessageBox.information(None, 'Example:', 'Colormap is loaded!')

    def points(self):
        path_to_ports_layer = os.path.join(QgsProject.instance().homePath(),"qgis_sample_data", "climate", "climate.shp")
        vlayer = QgsVectorLayer(path_to_ports_layer)
        if not vlayer.isValid():
            print("Layer failed to load!")
        QgsProject.instance().addMapLayer(vlayer)

