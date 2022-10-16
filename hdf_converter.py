# -*- coding:utf-8 -*-
import os, sys
import gdal
import osr
import numpy as np
import drawer


def batchConvertHDF2Tif(inRootPath, outRootPath):
    for root, dirs, files in os.walk(inRootPath, topdown=False):
        # 遍历路径
        for dir in dirs:
            dirPath = os.path.join(root, dir)
            print("Processing dir: " + dirPath)
            file_list = os.listdir(dirPath)
            for file in file_list:
                if file.endswith('.he5'):
                    print('Processing file: ' + file)
                    src_ds = gdal.Open(os.path.join(dirPath, file))
                    sub_ds = src_ds.GetSubDatasets()
                    print('The number of sub-datasets is : {}'.format(len(sub_ds)))
                    for sd in sub_ds:
                        print('Name: {0}\nDescription:{1}\n'.format(*sd))
                    o3_ds = gdal.Open(sub_ds[0][0]).ReadAsArray()
                    data = o3_ds[:]
                    data[data > 2e+16] = np.nan
                    data[data < 0] = np.nan
                    # 2008m0101
                    newFileName = file.split('_')[2]
                    newFolderName = dir.split('_')[0]
                    newDir = outRootPath + newFolderName + '\\'
                    if not os.path.exists(newDir):
                        os.mkdir(newDir)
                    newRasterName = newDir + newFileName + '.tif'
                    if os.path.exists(newRasterName):
                        os.remove(newRasterName)
                    rasterOrigin = (-180, 90)
                    x_size = 0.25
                    y_size = -0.25
                    array2raster(newRasterName, rasterOrigin, x_size, y_size, data)


def convertHDF2Tif(inFile, outFile):
    src_ds = gdal.Open(inFile)
    sub_ds = src_ds.GetSubDatasets()
    print('The number of sub-datasets is : {}'.format(len(sub_ds)))
    for sd in sub_ds:
        print('Name: {0}\nDescription:{1}\n'.format(*sd))
    o3_ds = gdal.Open(sub_ds[0][0]).ReadAsArray()
    data = o3_ds[:]
    # data[data > 2e+16] = np.nan
    # data[data < 0] = np.nan
    if os.path.exists(outFile):
        os.remove(outFile)
    rasterOrigin = (-180, 90)
    x_size = 0.25
    y_size = -0.25
    array2raster(outFile, rasterOrigin, x_size, y_size, data)


def array2raster(newRasterfn, rasterOrigin, pixelWidth, pixelHeight, array):
    cols = array.shape[1]  # obtain cols
    rows = array.shape[0]  # obtain rows
    originX = rasterOrigin[0]  # upper left corner X
    originY = rasterOrigin[1]  # upper left corner Y

    format = 'GTiff'
    driver = gdal.GetDriverByName(format)

    # create a single band raster
    outRaster = driver.Create(newRasterfn, cols, rows, 1, gdal.GDT_Float32)
    # set GeoTransform parameters
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
    # read band 1
    outband = outRaster.GetRasterBand(1)
    outband.WriteArray(array)
    # EPSG4326
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromEPSG(4326)
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()


# 计算每年的平均O3量
def calYearAverage(inRootPath):
    yearMeanArr = []
    yearsArr = []
    daysArr = []
    # 访问根路径
    for root, dirs, files in os.walk(inRootPath, topdown=False):
        # 遍历年份的文件夹,eg:2008
        for dir in dirs:
            dirPath = os.path.join(root, dir)
            # print("Processing year: " + dir)
            file_list = os.listdir(dirPath)
            yearSum = 0.0
            days = 0
            for file in file_list:
                # 计算并记录平均值
                if file.endswith('.tif'):
                    # print('Processing file: ' + file)
                    yearSum += calFileAverage(os.path.join(dirPath, file))
                    days += 1
            if days > 0:
                yearMean = yearSum / days
                yearMeanArr.append(yearMean)
                yearsArr.append(dir)
                daysArr.append(days)
                print("year:%s days:%d mean:%.3f" % (dir, days, yearMean))
    return yearMeanArr, yearsArr,daysArr


def calMonthAverageEveryYear(inRootPath):
    yearMonthlyArr = []
    yearsArr = []
    # 访问根路径
    for root, dirs, files in os.walk(inRootPath, topdown=False):
        # 遍历年份的文件夹,eg:2008
        for dir in dirs:
            dirPath = os.path.join(root, dir)
            print("Processing year: " + dir)
            file_list = os.listdir(dirPath)
            year = dir
            monthArrayMean = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            monthArraySum = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            monthArrayCount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for file in file_list:
                # 计算并记录平均值
                if file.endswith('.tif'):
                    month = int(file.split('m')[1][0:2])
                    monthArraySum[month - 1] += calFileAverage(os.path.join(dirPath, file))
                    monthArrayCount[month - 1] += 1
            for i in range(0, 12):
                monthArrayMean[i] = monthArraySum[i] / monthArrayCount[i]
            yearMonthlyArr.append(monthArrayMean)
            yearsArr.append(year)
    return yearMonthlyArr, yearsArr


def calFileAverage(file):
    # 注册类
    gdal.AllRegister()
    ds = gdal.Open(file)
    if ds is None:
        print('Could not open image')
        sys.exit(1)
    # 读取行列、波段
    rows = ds.RasterYSize
    cols = ds.RasterXSize
    bands = ds.RasterCount
    # 读取第一波段
    band = ds.GetRasterBand(1)
    # 读取栅格，并转为array
    data = band.ReadAsArray(0, 0, cols, rows)

    # 忽略nan值后的平均值
    # nanIndex = np.where(np.isnan(data))
    ignoreNanMean = np.nanmean(data)
    return ignoreNanMean


if __name__ == '__main__':
    # he5批量转tif
    he5RootPath = u'D:\\lzu\courses\\atmosphericRemoteSensing\\2008-2018_OMI_O3_DATA\\'
    tifRootPath = u'D:\\lzu\courses\\atmosphericRemoteSensing\\2008-2018_TIF_O3_DATA\\'
    jpgRootPath = u'D:\\lzu\courses\\atmosphericRemoteSensing\\picture\\'
    # batchConvertHDF2Tif(he5RootPath,tifRootPath)

    # he5单文件转tif
    # testInFile = u'D:\\lzu\courses\\atmosphericRemoteSensing\\test\\testin.he5'
    # testOutFile = u'D:\\lzu\courses\\atmosphericRemoteSensing\\test\\testout.tif'
    # convertHDF2Tif(testInFile,testOutFile)



    # 计算O3每年平均值数组
    yearMeanArr, yearsArr,daysArr = calYearAverage(tifRootPath)
    drawer.drawLineChart("2008-2018年全球O3年均总柱量变化趋势图","year","O3(DU)",yearsArr,yearMeanArr,"Annual mean ozone",jpgRootPath + "yearMean.jpg")

    # yearsArr = [1,2,3]
    # daysArr = [1,2,3]
    # 绘制年份和有效天数图
    # drawer.drawBarChart("2008-2018年全球O3年有效计算天数","year","days",yearsArr,daysArr,"Annual valid calculation days",jpgRootPath + "days.jpg")


    # 计算O3每年每月的平均值数组
    yearMonthlyArr, yearsArr = calMonthAverageEveryYear(tifRootPath)
    monthArr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    drawer.drawMultiLineChart("2008-2018年全球O3月均总柱量变化趋势图", "month", "O3(DU)", monthArr, yearMonthlyArr, yearsArr,
                              jpgRootPath + "yearMonthlyMean.jpg")
