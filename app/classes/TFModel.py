import cv2 as cv
import numpy as np
import yaml
import os
from tensorflow.keras.models import load_model
from models import Prediction
from logger import logger
from PIL import Image, ImageOps


np.set_printoptions(suppress=True)

models = {}

class TFModel:
    
    def __init__(self, name):       
        try:            
            with open('config.yml', 'r') as f:
                config = yaml.safe_load(f)                
            self.name = name
            self.path = config['models']['path']
            print('Loading Model ', name)
            
        except Exception as e:            
            logger.error('TFModel::__init__::Invalid Model Configuration::'+str(e))
    
    def predict(self, image:np.ndarray) -> Prediction:
        global models

        size = 224
        channels = 3

        if channels == 1:
            image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        else:
            image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
            
        image = cv.resize(image, (size, size), cv.INTER_AREA)        
        image = (image / 127.0) - 1
        image = image.reshape(1, size, size, channels)

        self.load_single_model()               

        net = models[self.name]['graph']
        res = net.predict(image)
        index = int(res.argmax(axis=1)[0])        
        label = models[self.name]['labels'][index].upper()
        confidence = float(round(res[0][index], 2))        
        return Prediction(label, confidence)


    def predict_keras(self, image):
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        data[0] = normalized_image_array
        

    def load_single_model(self):
        global models

        filename = 'keras_model.h5'

        if self.name in models:
            return print('Model Loaded from Cache')            
        
        labels = []
        label_file = open(f'{self.path}/{self.name}/labels.txt', 'r')

        for line in label_file:
            label = line.split(' ')[-1][:-1]            
            labels.append(label)

        label_file.close()

        models[self.name] = { 'labels': labels, 'graph': load_model(f'{self.path}/{self.name}/{filename}', compile=False)}
    

    def load_models(self):
        global models       

        for model_name in os.listdir(self.path):
            if not model_name in models:
                for file in os.listdir(f'{self.path}/{model_name}'):                
                    if file == self.default_graph_file:
                        # logging.info('Loading Model: ' + model_name)
                        print('Loading Model: ' + model_name)
                        labels = []
                        label_file = open('labels.txt', 'r')
                        for line in label_file:
                            label = line.split(' ')[-1][:-1]
                            labels.append(label)
                        label_file.close()
                        models[model_name] = {                         
                            'graph': load_model(f'{self.path}/{model_name}/{self.default_graph_file}', compile=False),
                            'labels': labels
                        }

