import numpy as np
from sklearn.model_selection import KFold
from keras.models import Sequential
from keras.layers import SimpleRNN,Activation,Dense
from keras.layers import LSTM
from keras.utils import to_categorical
from keras import backend

#extract first 10 items from pattern
itemNum=10
np.random.seed(9434)
myData=np.loadtxt("path/to/train/data/set")
#tmpZero is to compulsarily extend the last time's features
tmpZero=np.zeros((np.shape(myData)[0],2),dtype=np.float)
#ten time noedes and one length node
X=myData[:,[1]+list(range(3,2+itemNum*3))]
X=np.hstack((X,myData[:,[2]],tmpZero))
#label
y=myData[:,[48]]
#the model need the label start from 0 `
y=y-1
y=to_categorical(y)
model=Sequential()
model.add(LSTM(200))
#the first parameter needs to be identical to the class num
model.add(Dense(3,activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
X=X.reshape(np.shape(X)[0],itemNum+1,3)
model.fit(X, y, epochs=30)
model.save('simuModel.h5')
