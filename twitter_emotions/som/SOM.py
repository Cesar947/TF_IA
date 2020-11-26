import numpy as np
import matplotlib.pyplot as plt
import math


class SOM:

    def __init__(self, trainData, testData, rows, cols, learningRate, iterations):
        #numpy array
        self.trainData = trainData
        self.testData = testData

        #number of rows and cols of the SOM 
        self.rows = rows
        self.cols = cols
        self.features = len(trainData)
        self.learningRate = learningRate
        self.iterations = iterations

    def euclidianDistance(self, a, b):
        return np.linalg.norm(a - b)

    def clusterization(self):
        # Número de entradas del patrón Xi
        num_xi = 1000 
        # Necesitamos 2 clases, por tanto hacemos el mapa de 2 x 2
        rows = 2
        columns = 2
        

    def singleClusterization(self, test_tweet):
        return

    def bmu(self, data, weights, index, rows, cols):
        result = (0,0)
        minDistance = math.inf

        for i in range(rows):
            for j in range(cols):
                distance = np.linalg.norm(weights[i][j] - data[index])
                if distance < minDistance:
                    minDistance = distance
                    result = (i,j)

        return result

    def manhattanDistance(self, r1, c1, r2, c2):
        return np.abs(r1 - r2) + np.abs(c1 - c2)

    def training(self):
        #una fila, va a tener 4 features, por eso dimension 4
        features = self.features
        #si quieres 4 clusters, entonces deberia ser mayor a 4*4 
        rows = self.rows
        cols = self.cols
        maxRange = rows + cols #VER POR QUÉ LO SUMA
        learningRate = self.learningRate
        iterations = self.iterations
        dataSize = len(self.trainData)
        

        dataset = "dataset.txt"
        trainingData = np.loadtxt(dataset, delimiter=",", usecols=range(0,4), dtype=np.float64)

        #Inicializamos los weights
        weights = np.random.randn(rows,cols,features)
        print(weights)

        #Training
        for i in range(iterations):

            #El factor de aprendizaje va a ir cambiando por cada iteracion
            alpha = 1.0 - ( (i*1.0) / iterations)
            currentRange = (int) (alpha * maxRange)
            currentAlpha = alpha * learningRate

            #se elige un patron de entrenamiento random
            #index = np.random.randint(len(trainingData))
            index = np.random.randint(dataSize)
            (bmuRow, bmuCol) = self.bmu(self.trainData, weights, index, rows, cols)

            #Iterar el vecindario topologico del BMU
            for r in range(rows):
                for c in range(cols):
                    if(self.manhattanDistance(bmuRow, bmuCol, r, c)  < currentRange):
                        weights[r][c] = weights[r][c] + currentAlpha * (self.trainData[index] - weights[r][c])

        
        #Generar rango para poder obtener las clases
        #iterar todo el dataset y obtener, para cada uno, su BMU
        #guardar esta matriz donde cada row va a ser un dato (patron de entrenamiento) y las columnas van a ser los pesos del BMU hacia ese nodo de entrada
        #sumar todos los pesos por cada fila
        #una vez calculado todo, hallar el maximo y minimo
        #hallar la diferencia entre ambos valores
        #dividirlo entre 2 (las clases que queremos)
        #hallar los intervalos minimo + resultado division 
        #maximo - resultado division
        #guardar estos intervalos
        
        labels = []
        for r in range(dataSize):
            for c in range(features):
                (currentBmuRow,currentBmuCol) = self.bmu(self.trainData, weights, r, rows, cols)
                sum = 0

                for x in range(features):
                    sum += self.trainData[currentBmuRow][currentBmuCol][x]
                
                labels.append(sum)

        maxValue = max(labels)
        minValue = min(labels)

        breakpoint = (maxValue-minValue) / 2

        for i in range(len(labels)):
            if labels[i] < breakpoint:
                labels[i] = 0
            else:
                labels[i] = 1

        print(labels)




      
        """
          # Observamos
        for i in range(iterations):
            (bmuRow, bmuCol) = self.bmu(trainingData, weights, index, rows, cols)
            print(i, " ", bmuRow, bmuCol, weights[bmuRow][bmuCol])

        # Visualización
        mapa = np.empty(shape=(rows,cols), dtype=np.int)
        for i in range(rows):
            for j in range(cols):
                mapa[i][j] = -1
        for t in range(10):
            (bmuRow, bmuCol) = bmu(trainingData, weights, index, rows, cols)
            mapa[bmuRow][bmuCol] = salida[t]
        """




