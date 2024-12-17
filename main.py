# -*- coding: utf-8 -*-
"""AnimalEncFinal.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Dg57Y4cfqo3eipjKBpsxdkKOF1ngpXoM
"""

import numpy as np
import os
import cv2
import time
import glob
import datetime
from collections import deque
from matplotlib import pylab
import IPython
from pylab import *

from skimage import img_as_float
import tensorflow
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing import image

img = cv2.imread(r"C:\Users\Likhita\OneDrive - XLRI\Desktop\sem 7\Project\el.JPG")

cv2.imshow("framfr",cv2.resize(img,None,fx=0.65,fy=0.65))
cv2.waitKey(0)


img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img_blur = cv2.GaussianBlur(img_gray, (3,3), 0)

sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5)
sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5)
sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)

cv2.imshow(sobelx)
cv2.waitKey(0)
cv2.imshow(sobely)
cv2.waitKey(0)
cv2.imshow( sobelxy)
cv2.waitKey(0)

from PIL import ImageFile
from twilio.rest import Client
from PIL import Image

account_sid = "AC63ab36a20b5bfa5f0d2278ddc9457546"
auth_token  = "4d8c31e7a38ed86a0c411c469d4dfd01"

client = Client(account_sid, auth_token)

import pickle

pip install opencv-python

pip install tensorflow

pip install keras

train_animal = r"C:\Users\Likhita\OneDrive - XLRI\Desktop\animal-or-human\train\animals"
train_misc= r"C:\Users\Likhita\OneDrive - XLRI\Desktop\animal-or-human\train\humans"

valid_dir = r"C:\Users\Likhita\OneDrive - XLRI\Desktop\animal-or-human\validation"
train_dir = r"C:\Users\Likhita\OneDrive - XLRI\Desktop\animal-or-human\train"

train_animal_names = os.listdir(train_animal)
print(len(train_animal_names))

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(16, (3,3), activation='relu', input_shape=(300, 300, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.summary()

model.compile(loss='binary_crossentropy',
              optimizer=RMSprop(lr=0.001),
              metrics=['acc'])

train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1/255,
                                                                width_shift_range=[-200,200],
                                                                height_shift_range=[-200,200],
                                                                horizontal_flip=True)
valid_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1/255,
                                                                width_shift_range=[-200,200],
                                                                height_shift_range=[-200,200],
                                                                horizontal_flip=True)

train_gen = train_datagen.flow_from_directory(train_dir,
                                             target_size=(300,300),
                                             class_mode='binary'
                                             )

valid_gen = train_datagen.flow_from_directory(
    valid_dir,
    target_size = (300,300),
    class_mode = 'binary'
)

ImageFile.LOAD_TRUNCATED_IMAGES = True

hist = model.fit(
    train_gen,
    epochs = 13,
)

with open('clf.pickle', 'wb') as f:
    pickle.dump(hist, f)

os.listdir()

model.save(path)

path = './model.h5'
loaded_model= tf.keras.models.load_model(path )

type(loaded_model)

def detection(files):
  limit = 0
  for myFiles in files:
    img = tf.keras.utils.load_img(myFiles, target_size=(300, 300))
    x = tf.keras.utils.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    classes = loaded_model.predict(images)
    print(classes[0])
    if classes[0]>0.5:
      print("Miscellaneous movement")
    else:
      print("Movement by Animal")
      limit = limit + 1
  if limit > 3:
    display(IPython.display.Audio(alarm, autoplay=True))
    calls = client.calls.create(
    to='+919014742653',
    from_='+12762955240',
    twiml='<Response><Say>Animal Detected!</Say></Response>',)
    print(calls.sid)
    print("Animal detected")
  else:
    print("No animal detected")

hist.history['acc']

import matplotlib.pyplot as plt
plt.plot(hist.history["loss"])
plt.plot(hist.history['acc'])
plt.title("model accuracy")
plt.ylabel("Accuracy")
plt.xlabel("Epoch")
plt.legend(["Loss","Accuracy"])
plt.show()

from itertools import combinations_with_replacement
from collections import defaultdict

from numpy.linalg import inv

R, G, B = 0, 1, 2

def boxfilter(I, r):
    M, N = I.shape
    dest = np.zeros((M, N))
    sumY = np.cumsum(I, axis=0)
    dest[:r + 1] = sumY[r:2*r + 1]
    dest[r + 1:M - r] = sumY[2*r + 1:] - sumY[:M - 2*r - 1]
    dest[-r:] = np.tile(sumY[-1], (r, 1)) - sumY[M - 2*r - 1:M - r - 1]

    sumX = np.cumsum(dest, axis=1)
    dest[:, :r + 1] = sumX[:, r:2*r + 1]
    dest[:, r + 1:N - r] = sumX[:, 2*r + 1:] - sumX[:, :N - 2*r - 1]
    dest[:, -r:] = np.tile(sumX[:, -1][:, None], (1, r)) - sumX[:, N - 2*r - 1:N - r - 1]
    return dest


def guided_filter(I, p, r=15, eps=1e-3):
    M, N = p.shape
    base = boxfilter(np.ones((M, N)), r)
    means = [boxfilter(I[:, :, i], r) / base for i in range(3)]
    mean_p = boxfilter(p, r) / base

    means_IP = [boxfilter(I[:, :, i]*p, r) / base for i in range(3)]

    covIP = [means_IP[i] - means[i]*mean_p for i in range(3)]
    var = defaultdict(dict)
    for i, j in combinations_with_replacement(range(3), 2):
        var[i][j] = boxfilter(I[:, :, i]*I[:, :, j], r) / base - means[i]*means[j]

    a = np.zeros((M, N, 3))
    for y, x in np.ndindex(M, N):
        Sigma = np.array([[var[R][R][y, x], var[R][G][y, x], var[R][B][y, x]],
                          [var[R][G][y, x], var[G][G][y, x], var[G][B][y, x]],
                          [var[R][B][y, x], var[G][B][y, x], var[B][B][y, x]]])
        cov = np.array([c[y, x] for c in covIP])
        a[y, x] = np.dot(cov, inv(Sigma + eps*np.eye(3)))  # eq 14


    b = mean_p - a[:, :, R]*means[R] - a[:, :, G]*means[G] - a[:, :, B]*means[B]
    q = (boxfilter(a[:, :, R], r)*I[:, :, R] + boxfilter(a[:, :, G], r)*I[:, :, G] + boxfilter(a[:, :, B], r)*I[:, :, B] + boxfilter(b, r)) / base

    return q

def get_illumination_channel(I, w):
    M, N, _ = I.shape
    padded = np.pad(I, ((int(w/2), int(w/2)), (int(w/2), int(w/2)), (0, 0)), 'edge')
    darkch = np.zeros((M, N))
    brightch = np.zeros((M, N))

    for i, j in np.ndindex(darkch.shape):
        darkch[i, j] = np.min(padded[i:i + w, j:j + w, :])
        brightch[i, j] = np.max(padded[i:i + w, j:j + w, :])
    print("channels")
    return darkch, brightch

def get_atmosphere(I, brightch, p=0.1):
    M, N = brightch.shape
    flatI = I.reshape(M*N, 3)
    flatbright = brightch.ravel()

    searchidx = (-flatbright).argsort()[:int(M*N*p)]
    A = np.mean(flatI.take(searchidx, axis=0), dtype=np.float64, axis=0)
    print("atmosphere")
    return A

def get_initial_transmission(A, brightch):
    A_c = np.max(A)
    init_t = (brightch-A_c)/(1.-A_c)
    print("initial transition")
    return (init_t - np.min(init_t))/(np.max(init_t) - np.min(init_t))


def get_corrected_transmission(I, A, darkch, brightch, init_t, alpha, omega, w):
    im = np.empty(I.shape, I.dtype);
    for ind in range(0, 3):
        im[:, :, ind] = I[:, :, ind] / A[ind]
    dark_c, _ = get_illumination_channel(im, w)
    dark_t = 1 - omega*dark_c
    corrected_t = init_t
    diffch = brightch - darkch

    for i in range(diffch.shape[0]):
        for j in range(diffch.shape[1]):
            if(diffch[i, j] < alpha):
                corrected_t[i, j] = dark_t[i, j] * init_t[i, j]
    print("corrected")
    return np.abs(corrected_t)

def get_final_image(I, A, refined_t, tmin):
    refined_t_broadcasted = np.broadcast_to(refined_t[:, :, None], (refined_t.shape[0], refined_t.shape[1], 3))
    J = (I-A) / (np.where(refined_t_broadcasted < tmin, tmin, refined_t_broadcasted)) + A
    print("final")
    return (J - np.min(J))/(np.max(J) - np.min(J))

def dehaze(I, tmin=0.1, w=15, alpha=0.4, omega=0.75, p=0.1, eps=1e-3, reduce=False):
    I = np.asarray(I, dtype=np.float64)
    I = I[:, :, :3] / 255
    m, n, _ = I.shape
    Idark, Ibright = get_illumination_channel(I, w)
    A = get_atmosphere(I, Ibright, p)

    init_t = get_initial_transmission(A, Ibright)
    if reduce:
        init_t = reduce_init_t(init_t)
    corrected_t = get_corrected_transmission(I, A, Idark, Ibright, init_t, alpha, omega, w)

    normI = (I - I.min()) / (I.max() - I.min())
    refined_t = guided_filter(normI, corrected_t, w, eps)
    return refined_t

img = cv2.imread(r"C:\Users\Likhita\OneDrive - XLRI\Desktop\sem 7\Project\night.PNG")
new_i= dehaze(img)
cv2.imshow("frame",cv2.resize(new_i,None,fx=0.65,fy=0.65))
cv2.waitKey(0)

def animalEnc(video):
  cap = cv2.VideoCapture(video)
  kernel= None
  foog = cv2.createBackgroundSubtractorMOG2(detectShadows = True, varThreshold = 50, history = 500)
  thresh = 1100
  count = 0
  detect_thresh = 7
  currentframe = 0
  disp=[]
  while(1):
      ret, frame = cap.read()
      if not ret:
          break
      fgmask = foog.apply(frame)
      print(frame.shape)
      ret, fgmask = cv2.threshold(fgmask, 250, 255, cv2.THRESH_BINARY)
      fgmask = cv2.erode(fgmask,kernel,iterations = 1)
      fgmask = cv2.dilate(fgmask,kernel,iterations = 1)
      contours, hierarchy = cv2.findContours(fgmask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
      if contours:
          cnt = max(contours, key = cv2.contourArea)
          if cv2.contourArea(cnt) > thresh:
              x,y,w,h = cv2.boundingRect(cnt)
              cv2.rectangle(frame,(x ,y),(x+w,y+h),(0,0,255),2)
              cv2.putText(frame,'Movement Detected',(x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,255,0), 1, cv2.LINE_AA)
              count = count + 1
              cv2.imwrite(os.path.join('C:/Users/Likhita/OneDrive - XLRI/Desktop/sem 7/Project/temp','frame'+str(currentframe)+'.jpg'),frame)
              currentframe+=1
      fgmask_3 = cv2.cvtColor(fgmask, cv2.COLOR_GRAY2BGR)
      stacked = np.hstack((fgmask_3,frame))
      cv2.imshow("rame",cv2.resize(stacked,None,fx=0.65,fy=0.65))
      files=[]
      if count>detect_thresh:
        for img in glob.glob("C:/Users/Likhita/OneDrive - XLRI/Desktop/sem 7/Project/temp/*.jpg"):
            files.append(img)
        print("invoking", len(files))
        detection(files)
        break
      k = cv2.waitKey(40) & 0xff
      if k == ord('q'):
          break
  cap.release()

image = cv2.imread(r"C:\Users\Likhita\OneDrive - XLRI\Desktop\sem 7\Project\el.JPG")
cv2.imshow("frame",cv2.resize(image,None,fx=0.65,fy=0.65))
cv2.waitKey(0)

animalEnc(r"C:\Users\Likhita\OneDrive - XLRI\Desktop\sem 7\Project\fh2.mp4")

cv2.destroyAllWindows()

img = cv2.imread(r"C:\Users\Likhita\OneDrive - XLRI\Desktop\sem 7\Project\el.JPG")
cv2.imshow("frame", img)

img = cv2.imread(r"C:\Users\Likhita\OneDrive - XLRI\Desktop\sem 7\Project\el.JPG")

dehaze(img)
