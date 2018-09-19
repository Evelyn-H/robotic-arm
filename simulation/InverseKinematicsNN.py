import numpy
from math import pi
from keras.models import Sequential
from keras.models import save_model
from keras.layers import Dense
from keras.layers import Dropout
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from ForwardKinamatics import ForwardKinematics
import random
from keras.callbacks import CSVLogger
from keras.callbacks import ModelCheckpoint


class KerasNet(object):


    def createDataSet(self, fk):
        output = numpy.zeros((2000000, 4))
        input = numpy.zeros((2000000, 4))
        for i in range(2000000):
            theta0 = numpy.random.uniform(0, 0.5*pi)
            theta1 = numpy.random.uniform(-0.5*pi, 0.5*pi)
            theta2 = numpy.random.uniform(0, 0.5*pi)
            theta3 = numpy.random.uniform(-0.5*pi, 0.5*pi)
            result = fk.move([theta0, theta1, theta2, theta3])
            output[i, 0] = theta0/(0.5*pi)
            output[i, 1] = theta1/(0.5*pi)
            output[i, 2] = theta2/(0.5*pi)
            output[i, 3] = theta3/(0.5*pi)

            input[i, 0] = result[0]/34
            input[i, 1] = result[1]/34
            input[i, 2] = result[2]/34
            input[i, 3] = (theta1+theta2+theta3)/(1.5*pi)

        # print("Number of values: " + str(len(output)))
        # print(str(output))
        return (input, output)


    def baseline_model(self):
        # create model
        model = Sequential()
        model.add(Dense(50, input_dim=4, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(50, input_dim=50, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(50, input_dim=50, activation='relu'))
        model.add(Dropout(0.5))
        # model.add(Dense(50, input_dim=50, kernel_initializer='normal', activation='relu'))
        # model.add(Dense(50, input_dim=50, kernel_initializer='normal', activation='relu'))
        # model.add(Dense(50, input_dim=50, kernel_initializer='normal', activation='relu'))
        model.add(Dense(4))
        # Compile model
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
        return model

    def run(self, fk):
        X, Y = self.createDataSet(fk)
        # fix random seed for reproducibility
        # evaluate model with standardized dataset
        csv_logger = CSVLogger('log.csv', append=True, separator=';')
        checkpoint = ModelCheckpoint('checkpoint.h5', monitor='val_acc', verbose=2, save_best_only=False, save_weights_only=False, mode='auto', period=1)
        estimator = KerasRegressor(build_fn=self.baseline_model, epochs=100, batch_size=16, verbose=2)
        estimator.fit(X,Y, callbacks=[csv_logger, checkpoint], validation_split=0.1)
        estimator.model.save('model.h5')
        #kfold = KFold(n_splits=10, random_state=seed)
        #results = cross_val_score(estimator, X, Y, cv=kfold)
        #print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))
       # estimator.

    def predict(self, fk):
        #X, Y = self.createDataSet(fk)
       # print("Created data")
        model = self.baseline_model()
        model.load_weights("checkpoint.h5")
        print("Loaded model")
        data = numpy.zeros((1,4))
        data[0,0] = 9/34
        data[0,1] = 0/34
        data[0,2] = 17/34
        data[0,3] = (0.5*pi)/(1.5*pi)
        prediction = model.predict(data)
        print(prediction)
        return prediction
        #scores = model.evaluate(X, Y, verbose=0)
        #print("%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
