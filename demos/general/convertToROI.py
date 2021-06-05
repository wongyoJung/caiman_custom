#!/usr/bin/env python 

import os
import struct
from read_roi import read_roi_file
from read_roi import read_roi_zip
from pymagej.roi import ROIEncoder, ROIRect


def int_to_hex(i): # for 16 bit integers
	return('{:04x}'.format(i).decode('hex'))

def float_to_hex(f): # for 32 bit floats
	return(hex(struct.unpack('<I', struct.pack('<f', f))[0])[2:]).decode('hex')
	

'''
Definition of the ROI format
https://imagej.nih.gov/ij/developer/source/ij/io/RoiEncoder.java.html
https://imagej.nih.gov/ij/developer/source/ij/io/RoiDecoder.java.html
 ImageJ/NIH Image 64 byte ROI outline header
    2 byte numbers are big-endian signed shorts
    
    0-3     "Iout"
    4-5     version (>=217)
    6-7     roi type
    8-9     top
    10-11   left
    12-13   bottom
    14-15   right
    16-17   NCoordinates
    18-33   x1,y1,x2,y2 (straight line)
    34-35   stroke width (v1.43i or later)
    36-39   ShapeRoi size (type must be 1 if this value>0)
    40-43   stroke color (v1.43i or later)
    44-47   fill color (v1.43i or later)
    48-49   subtype (v1.43k or later)
    50-51   options (v1.43k or later)
    52-52   arrow style or aspect ratio (v1.43p or later)
    53-53   arrow head size (v1.43p or later)
    54-55   rounded rect arc size (v1.43p or later)
    56-59   position
    60-63   header2 offset
    64-     x-coordinates (short), followed by y-coordinates
'''

def write_imagej_roi (coordinates,name,path,stroke_width=3,stroke_col='88FFFF00',fill_col='00000000'):


	# Creates ImageJ compatible ROI files for points or circles
	# Parameters:
	#	coordinates:		for circles (t,l,b,r) or (x,y,r) for points (x,y)
	#	name:				Name of the roi (and exported file)
	#	path:				path to write the output files
	# Optional parameters:
	#	stroke_width [int]
	#	stroke_col [0xAARRGGBB]
	#
	# Return: path to output file
	
	pasfloat=False
	offset_filename=128 
	if len(coordinates)==4: # Bounding box
		#type='\x01\x00' # For rectangles
		type='\x02\x00'
		top,left,bottom,right=coordinates
	elif len(coordinates)==3: # x,y,r : Circle
		type='\x02\x00'
		x,y,r=coordinates
		top,left,bottom,right= int(round(y-r)),int(round(x-r)),int(round(y+r)),int(round(x+r))
	elif len(coordinates)==2: # x,y: Point
		type='\x01\x00' # This is actualy a one pixel rectangle
		x,y=coordinates
		top,left,bottom,right=int(x),int(y),int(x+1),int(y+1)
		pasfloat= (not (int(x)==x and int(y)==y)) # add subpixel resolution (here it's a real point)
	
	filelength=128+len(name)*2+pasfloat*8
	print(filelength)
	data=bytearray(filelength)

	data[0:4]='\x49\x6F\x75\x74'   					#"Iout" 0-3
	data[4:6]='\x00\xE3'           					#Version 4-5

	data[6:8]=type                  				# roi type   6-7     # Ovals/points
	data[8:10] = int_to_hex(top)     				# top      8-9    
	data[10:12]= int_to_hex(left)    				# left    10-11   
	data[12:14]= int_to_hex(bottom)  				# bottom  12-13    
	data[14:16]= int_to_hex(right)   				# right   14-15
	data[34:36]= int_to_hex(stroke_width)  		    # Stroke Width  34-35  
	data[40:44]= stroke_col.decode('hex')			# Storke Color 40-43 
	data[44:48]= fill_col.decode('hex')
	data[60:64]= '\x00\x00\x00\x40'					# header2offset 60-63   

	if (pasfloat):
		offset_filename= 128+12 						#header2offset +12
		data[ 6: 8] =' \x0A\x00' 
		data[16:18] = '\x00\x01' 						# Marker for 1 exact coordinate
		data[50:52] = '\x00\x80' 						# set options SUB_PIXEL_RESOLUTION 
		data[68:72] = float_to_hex(x)
		data[72:72] = float_to_hex(y)
		data[60:64] = '\x00\x00\x00\x4C' 				
		data[94:96] = '\x00\x8C' 						# Name offset
		data[98:100]= int_to_hex(len(name))			# Name Length

	else:
		data[82:84]='\x00\x80'						# Name offset
		data[86:88]=int_to_hex(len(name))			# Name Length

	p=offset_filename								# add name
	for c in name:
		print(p,c)
		data[p]=0x00
		data[p+1]=c
		p=p+2
	print(data)
	filename=os.path.join(path,name+".roi")			# write file
	file = open(filename,'wb')
	file.write(data)
	file.close()
	return(filename)


if __name__ =="__main__":
    #ex = "E:/2P_Kim/06012021 fasted SA-SO test/1-5/G1-5-Fasted-Lick-SO/RoiSet.zip"
    #rois = read_roi_zip(ex)
    #print(rois)
    roi_obj = ROIRect(20, 30, 40, 50) # Make ROIRect object specifing top, left, bottom, right
    with ROIEncoder('roi_filepath.roi', roi_obj) as roi:
        roi.write()


## Examples
# write_imagej_roi ((150,200),"test_point",".") 									                 # point (single pixel)
# write_imagej_roi ((150.5,200.8),"test_subpoint",".")    						             # point (subpixel)
# write_imagej_roi ((200,200,100),"test_circle",".",stroke_width=10) 				       # Circle
# write_imagej_roi ((100,200,300,300),"test_oval",".",stroke_col='88FF0000')    	 # Oval