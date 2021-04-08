
#on visualise la fonction
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

from keras.models import Sequential
from keras.layers import Dense

#mon intervalle
x=[i for i in np.arange(0,10,0.3)]+[10]

#ma fonction
y=2*np.cos(x)+4

#le graph
plt.plot(x,y)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Représentation de la fonction à approximer")
plt.show()

#on construit la base de données avec notre disretisation

x=pd.DataFrame(x)
y=pd.DataFrame(y)

#on normalise nos deux colonne pour préparre le terain au reseau de neurone
scalex = MinMaxScaler()
x=scalex.fit_transform(x)
scaley = MinMaxScaler()
y = scaley.fit_transform(y)

#The model
model=Sequential()

model.add(Dense(32,input_dim=1,activation='relu'))
model.add(Dense(64,activation='relu'))
model.add(Dense(128,activation='relu'))
model.add(Dense(256,activation='relu'))
model.add(Dense(1))

# compilateur avec loss= 'mse' puisque la comparaison des valeurs  numériques est possible 
model.compile(loss='mse', optimizer='adam')

#On fit notre modele

#on peut jouer avec les variables 
model.fit(x,y,epochs=100,batch_size=5,verbose=0)

#on obtient un meilleur résultat si on augmente epochs mais cela augmente considérablement le temps de calcul dans des cas plus complexes
yhat=model.predict(x)

x = scalex.inverse_transform(x)
y = scaley.inverse_transform(y)
yhat_plot = scaley.inverse_transform(yhat)

# l'erreur
print('MSE: %.3f' % mean_squared_error(y, yhat_plot))


# plot x vs y
plt.plot(x,y, label='y')

# plot x vs yhat
plt.plot(x,yhat_plot, label='yhat')
plt.title('Representation de la fonction et de son approximation en fonction de x')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()