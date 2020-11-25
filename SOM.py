import numpy as np

class SOM:
    def __init__(self, train_data, test_data):
        self.train_data = train_data
        self.test_data = test_data

    def euclidian_distance(self, a, b):
        return np.linalg.norm(a - b)

    def clusterization(self):
        # Número de entradas del patrón Xi
        num_xi = 1000 
        # Necesitamos 2 clases, por tanto hacemos el mapa de 2 x 2
        rows = 2
        columns = 2
        

    def single_clusterization(self, test_tweet)
