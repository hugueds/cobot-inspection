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
            self.size = config['models']['size']
            self.channels = config['models']['channels']            
            
        except Exception as e:            
            logger.error('TFModel::__init__::Invalid Model Configuration::'+str(e))

    def preprocess(self, image:np.ndarray, mode=255) -> np.ndarray: 
        if self.channels == 1:
            image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        else:
            image = cv.cvtColor(image, cv.COLOR_RGB2BGR) # Check if it changes the performance
            
        image = cv.resize(image, (self.size, self.size), cv.INTER_AREA)        
        # image = (image / 127.0) - 1
        image = (image / 255.0)
        image = image.reshape(1, self.size, self.size, self.channels)
        return image
    
    def predict(self, image:np.ndarray) -> Prediction:
        global models        

        image = self.preprocess(image)

        self.load_single_model()               

        model = models[self.name]
        net = model['graph']
        res = net.predict(image)
        index = int(res.argmax(axis=1)[0])        
        label = model['labels'][index].upper()
        confidence = float(round(res[0][index], 2))
        
        return Prediction(label, confidence)


    def predict_keras(self, image):
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        data[0] = normalized_image_array
    
    def load_single_model(self, name=''):
        global models

        filename = 'keras_model.h5'

        if self.name in models:
            return logger.info(f'Model {self.name} Loaded from Cache')
        else:
            logger.info('Loading Model ', self.name)
        
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
                        logger.info('Loading Model: ' + model_name)                        
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

