import subprocess as sp
import numpy as np
import cv2
import math
import commonFunc as cf
import classes

sp.call('cls', shell=True)

# ---------------------------------------------------------------------
#
# jpeg function
#
# ---------------------------------------------------------------------
def jpeg(img, div, fft = False, display8x8 = False):

    # begin scanning
    stop = False
    display = False
    matSize = 8         # size of matrix blocks to perform dct
    imgCopy = img.copy()
    for rowStart in range(0,512,matSize):
        for colStart in range(0,512,matSize):
            # take a matSize x matSize block
            imgSlice = img[rowStart:rowStart + matSize
                          ,colStart:colStart + matSize]

            if(not fft):
                # compute the discrete cosine transform of the block
                B = cv2.dct(imgSlice.astype('float32'))

                # quantize the block of DCT coefficients
                Bprime = cf.quantize(B,div)

                # calculate the inverse dct
                B = cv2.dct(Bprime.astype('float32'), B, cv2.DCT_INVERSE)
            else:
                # compute the discrete cosine transform of the block
                B = np.fft.fft2(imgSlice)

                # quantize the block of DCT coefficients
                Bprime = cf.quantize(B,div)

                # calculate the inverse dct
                B = np.fft.ifft2(Bprime)
                
            # replace the quantized blocks in the image's copy
            imgCopy[rowStart:rowStart + matSize
                   ,colStart:colStart + matSize] = B

            # display the 8 x 8 blocks for human inspection
            if display8x8:

                # display an image with another resolution on a resizable window
                winName = 'Original'
                cv2.namedWindow(winName, cv2.WINDOW_NORMAL)
                cv2.moveWindow(winName, winPosX, winPosY)
                cv2.imshow(winName,imgSlice)
                cv2.resizeWindow(winName, winWidth, winHeight)

                # increment next position of windows
                #winPosX = winPosX + winWidth

                # start plotting on another row
                if winPosX > 1430:
                    winPosY = winPosY + winHeight + 32
                    winPosX = 50

                # wait for a keypress from the user
                k = cv2.waitKey(0)
                if(k == 27):
                    stop = True

                # check if loop should be stopped
                if stop:
                    display8x8 = False

                # close all windows
                cv2.destroyAllWindows()

    return imgCopy

# ---------------------------------------------------------------------
#
# simple function to show an image at a certain location in the screen
#
# ---------------------------------------------------------------------
def showImg(img, winName, winPosX, winPosY):
    cv2.namedWindow(winName, cv2.WINDOW_NORMAL)
    cv2.moveWindow(winName, winPosX, winPosY)
    cv2.imshow(winName, img)
    cv2.resizeWindow(winName, winWidth, winHeight)

# ---------------------------------------------------------------------
#
# MAIN
#
# ---------------------------------------------------------------------
if __name__ == "__main__":
    sp.call('cls', shell = True)

    # load a color image in grayscale
    img = cv2.imread('./test images/peppers_gray.tif', 0)

    # ----------------------------------------
    # jpeg-type compression
    # ----------------------------------------
    idm = classes.ImageDisplayManager()
    for pwr in range(0,12):
        # divisor for quantization
        div = 2**pwr

        # perform jpeg quantization on the image
        ret = jpeg(img, div)

        # add each of the figures to be displayed
        idm.add(ret, 'div = 2**' + str(pwr))
    idm.show()

    ## ----------------------------------------
    ## comparison of quantization only and quantization with DCT
    ## ----------------------------------------
    ## initialize x and y position of windows
    #winPosY = 0         # y-coordinate of next window to plot
    #winPosX = 60        # x-coordinate of next window to plot
    #winWidth = 300      # width of window
    #winHeight = 300     # height of window

    #sp.call('cls', shell = True)
    #for pwr in range(0,12,2):
    #    # divisor for quantization
    #    div = 2**pwr

    #    # perform jpeg quantization on the image
    #    retJpeg = jpeg(img, div)

    #    # perform quantization on the image
    #    retQuant = cf.quantize(img, div)       

    #    # display an image with another resolution on a resizable window
    #    showImg(retJpeg, 'JPEG div = 2**' + str(pwr), winPosX, winPosY)
    #    showImg(retQuant, 'QUANT div = 2**' + str(pwr), winPosX, winPosY + winHeight + 32)

    #    # start plotting on another row
    #    if winPosX > 1430:
    #        winPosY = winPosY + winHeight + 32
    #        winPosX = 60
    #    else:
    #        # increment next position of windows
    #        winPosX = winPosX + winWidth

    #k = cv2.waitKey(0)
    #cv2.destroyAllWindows()

    ## ----------------------------------------
    ## comparison of compression using DCT and FFT
    ## ----------------------------------------
    ## initialize x and y position of windows
    #winPosY = 0         # y-coordinate of next window to plot
    #winPosX = 60        # x-coordinate of next window to plot
    #winWidth = 300      # width of window
    #winHeight = 300     # height of window

    #sp.call('cls', shell = True)
    #for pwr in range(0,12,2):
    #    # divisor for quantization
    #    div = 2**pwr

    #    # perform jpeg quantization on the image
    #    retDct = jpeg(img, div, fft = False)

    #    # perform quantization on the image
    #    #retFft = jpeg(img, div, fft = True)

    #    # display an image with another resolution on a resizable window
    #    showImg(retDct, 'DCT div = 2**' + str(pwr), winPosX, winPosY)
    #    #showImg(retFft, 'FFT div = 2**' + str(pwr), winPosX, winPosY + winHeight + 32)

    #    # start plotting on another row
    #    if winPosX > 1430:
    #        winPosY = winPosY + winHeight + 32
    #        winPosX = 60
    #    else:
    #        # increment next position of windows
    #        winPosX = winPosX + winWidth

    #k = cv2.waitKey(0)
    #cv2.destroyAllWindows()