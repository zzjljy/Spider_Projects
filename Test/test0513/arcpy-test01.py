#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @File : arcpy-test01.py
    @Author: LiJiaoyang
    @Date : 2020/6/11
    @Desc : 
'''

# -*- coding: UTF-8 -*-

import arcpy

import os

import ConversionUtils
# Set the input datasets

inputs = ConversionUtils.gp.GetParameterAsText(0)

# The list is split by semicolons ";"

inputs = ConversionUtils.SplitMultiInputs(inputs)

# Set the output workspace

output = ConversionUtils.gp.GetParameterAsText(1)


try:
    arcpy.env.workspace = output

    fcs = arcpy.ListFeatureClasses()
    fcs = fcs + arcpy.ListTables()

    dss = arcpy.ListDatasets()

    for File in inputs:

        for fc in fcs:

            arcpy.Append_management(File + "\\" + fc, output + "\\" + fc)

        for ds in dss:

            fcs1 = arcpy.ListFeatureClasses(feature_dataset=ds)

            for fc1 in fcs1:

                 arcpy.Append_management(File + "\\" + ds + "\\" + fc1, output + "\\" + ds + "\\" + fc1)



except arcpy.ExecuteError:
    print(arcpy.GetMessages())
