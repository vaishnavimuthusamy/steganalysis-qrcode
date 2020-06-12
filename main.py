import random
import numpy
import os,sys
import pyqrcode
import cv2
import png
import time
from PIL import Image
from tkinter.filedialog import askopenfilename
from tkinter import *
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter.filedialog import askopenfilename

root = Tk()
root.eval('tk::PlaceWindow . center')
def callback():
        mb.showinfo('Secret Keys', 'Make key files..')
        os.system('RSA_key.py')
        mb.showinfo('Encryption', 'Now encode your message')
        os.system('encrypt.py') 
        mb.showinfo('Process-Image', 'Now you can select the image')
        rsaimage()
        encode()
        qrcode_e()
def callback2():
       qrcode_d()
       time.sleep(2)
       print(mb.showinfo('Decoded word',decode()))
       os.system('decrypt.py')
       time.sleep(5)

def rsaimage():
        jpgfile = Image.open(askopenfilename())
        jpgfile.show()

        print(jpgfile.bits, jpgfile.size, jpgfile.format)
        row,col = jpgfile.size
        pixels = jpgfile.load()

        row1 = 1000003
        phi = [0 for x1 in range(row1)]
        occ = [0 for x1 in range(row1)]
        primes = [] 
        phi[1] = 1
        #phi[2] = 1
        #print (phi)
        for i in range(2,1000001):
                #print (i)
                if(phi[i] == 0):
                        phi[i] = i-1
                        #print (i)
                        primes.append(i)
                        #j = 2*i
                        for j in range (2*i,1000001,i):
                                #print("j ",j)
                                #print(j)
                                if(occ[j] == 0):
                                        #print ("inside if2")
                                        occ[j] = 1
                                        phi[j] = j
                                        #print (phi[j])
                                        #print ((i-1)//i)
                                phi[j] = (phi[j]*(i-1))//i
                                #print(phi[j])
                                #j = j + i
        #print (primes)
        p = primes[random.randrange(1,167)]
        q = primes[random.randrange(1,167)]
        print(p," ", q)
        n = p*q
        mod = n
        phin1 = phi[n]
        phin2 = phi[phin1]
        e = primes[random.randrange(1,9000)]
        mod1 = phin1
        def power1(x,y,m):
                ans=1
                while(y>0):
                        if(y%2==1):
                                ans=(ans*x)%m
                        y=y//2
                        x=(x*x)%m
                return ans
        d = power1(e,phin2-1,mod1)
        enc = [[0 for x in range(row)] for y in range(col)]
        dec = [[0 for x in range(row)] for y in range(col)]
        for i in range(col):
                for j in range(row):
                        r,g,b = pixels[j,i]
                        r1 = power1(r+10,e,mod)
                        g1 = power1(g+10,e,mod)
                        b1 = power1(b+10,e,mod)
                        enc[i][j] = [r1,g1,b1]
        print(pixels[row-1,col-1])
        img = numpy.array(enc,dtype = numpy.uint8)
        img1 = Image.fromarray(img,"RGB")
        #pixels2 = img1.load()
        img1.show()
        for i in range(col):
                for j in range(row):
                        r,g,b = enc[i][j]
                        r1 = power1(r,d,mod)-10
                        g1 = power1(g,d,mod)-10
                        b1 = power1(b,d,mod)-10
                        dec[i][j] = [r1,g1,b1]
        img2 = numpy.array(dec,dtype = numpy.uint8)
        img3 = Image.fromarray(img2,"RGB")
        img3.show()
        img3.save('image_1.bmp')
        j = Image.open("image_1.bmp")
        img = j.save("image_2.jpeg")
        p = j.load()
        print(p[row-1,col-1])
# Convert encoding data into 8-bit binary 
# form using ASCII value of characters 
def genData(data): 
		
		# list of binary codes 
		# of given data 
		newd = [] 
		
		for i in data: 
			newd.append(format(ord(i), '08b')) 
		return newd 
		
# Pixels are modified according to the 
# 8-bit binary data and finally returned 
def modPix(pix, data): 
	
	datalist = genData(data) 
	lendata = len(datalist) 
	imdata = iter(pix) 

	for i in range(lendata): 
		
		# Extracting 3 pixels at a time 
		pix = [value for value in imdata.__next__()[:3] +
								imdata.__next__()[:3] +
								imdata.__next__()[:3]] 
									
		# Pixel value should be made 
		# odd for 1 and even for 0 
		for j in range(0, 8): 
			if (datalist[i][j]=='0') and (pix[j]% 2 != 0): 
				
				if (pix[j]% 2 != 0): 
					pix[j] -= 1
					
			elif (datalist[i][j] == '1') and (pix[j] % 2 == 0): 
				pix[j] -= 1
				
		# Eigh^th pixel of every set tells 
		# whether to stop ot read further. 
		# 0 means keep reading; 1 means the 
		# message is over. 
		if (i == lendata - 1): 
			if (pix[-1] % 2 == 0): 
				pix[-1] -= 1
		else: 
			if (pix[-1] % 2 != 0): 
				pix[-1] -= 1

		pix = tuple(pix) 
		yield pix[0:3] 
		yield pix[3:6] 
		yield pix[6:9] 

def encode_enc(newimg, filename): 
	w = newimg.size[0] 
	(x, y) = (0, 0) 
	
	for pixel in modPix(newimg.getdata(), filename): 
		
		# Putting modified pixels in the new image 
		newimg.putpixel((x, y), pixel) 
		if (x == w - 1): 
			x = 0
			y += 1
		else: 
			x += 1
			
# Encode data into image 
def encode(): 
	img = "image_2.jpeg"
	image = Image.open(img, 'r')
	#image.show()
	
	#data = input("Enter data to be encoded : ") 
	#if (len(data) == 0): 
		#raise ValueError('Data is empty')
	filename = 'encrypted_file.txt' 
	newimg = image.copy() 
	encode_enc(newimg, filename)
	new_img_name = "image.png" 
	newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

def qrcode_e():
        new_img_name = "image.png"
        qr = pyqrcode.create(new_img_name)
        qr.png("qr_code.png", scale=10)
        img = Image.open("qr_code.png")
        img.show()
# Decode the data in the image 
def decode(): 
	img =  "image.png"
	image = Image.open(img, 'r')
	image.show()
	
	data = '' 
	imgdata = iter(image.getdata()) 
	
	while (True): 
		pixels = [value for value in imgdata.__next__()[:3] +
								imgdata.__next__()[:3] +
								imgdata.__next__()[:3]] 
		# string of binary data 
		binstr = '' 
		
		for i in pixels[:8]: 
			if (i % 2 == 0): 
				binstr += '0'
			else: 
				binstr += '1'
				
		data += chr(int(binstr, 2)) 
		if (pixels[-1] % 2 != 0): 
			return data

def qrcode_d():
    filename = Image.open(askopenfilename())
    filename = "qr_code.png"

    # read the QRCODE image
    img = cv2.imread(filename)

    # initialize the cv2 QRCode detector
    detector = cv2.QRCodeDetector()

    # detect and decode
    data, bbox, straight_qrcode = detector.detectAndDecode(img)
    cv2.imshow('qr_code', img)
    cv2.waitKey(1)
    # if there is a QR code
    if bbox is not None:
        print(data)
        # display the image with lines
        # length of bounding box
        n_lines = len(bbox)
        for i in range(n_lines):
            # draw all lines
            point1 = tuple(bbox[i][0])
            point2 = tuple(bbox[(i+1) % n_lines][0])
            cv2.line(img, point1, point2, color=(255, 0, 0), thickness=2)


# display the menu
root.title("Steganalysis")
IMAGE_PATH = 'design_img.jpg'
WIDTH, HEIGTH = 700, 400
root.geometry('{}x{}'.format(WIDTH, HEIGTH))
canvas = tk.Canvas(root, width=WIDTH, height=HEIGTH)
canvas.pack()
img = ImageTk.PhotoImage(Image.open(IMAGE_PATH).resize((WIDTH, HEIGTH), Image.ANTIALIAS))
canvas.background = img  # Keep a reference in case this code is put in a function.
bg = canvas.create_image(0, 0, anchor=tk.NW, image=img)

# Put a tkinter widget on the canvas.
a = Button(text=" Encrypt   ", command=callback, padx=30)
b = Button(text="   Decrypt   ", command=callback2, padx=30)
c = Button(text="    Exit       ", command=root.destroy, padx=30)

a.place(relx=0.54, rely=0.2, anchor=CENTER)
b.place(relx=0.45, rely=0.3, anchor=NW)
c.place(relx=0.63, rely=0.5, anchor=SE)

menubar = Menu(root)
# create a pulldown menu, and add it to the menu bar
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Encrypt", command=callback)
filemenu.add_command(label="Decrypt", command=callback2)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="Menu", menu=filemenu)
root.config(menu=menubar)
root.mainloop()



