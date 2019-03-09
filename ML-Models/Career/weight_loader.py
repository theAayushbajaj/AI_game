import _pickle as pickle
from sklearn.preprocessing import LabelEncoder
import numpy
from keras.models import load_model
import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_career():
    #clf.predict([[85.859834,56.391853,55.401763,21.368436,55.869562,11.490600,73.845602,57.813019]])
    #list(le.inverse_transform([267]))
    encoder = LabelEncoder()
    encoder.classes_ = numpy.load(ROOT_DIR + '/classes.npy')
    with open(ROOT_DIR + '/career.pkl', 'rb') as f:
        clf = pickle.load(f)
    return clf,encoder

def predict(clf):
    pass

def load_mitheory():
    # x=np.array([86.645904,85.070347,44.236459,72.588626,71.285970,68.394287])
    # inp=x.reshape(1,6,1)
    # model_lstm.predict(inp)
    model = load_model(ROOT_DIR + '/MI_childaptitude_model.h5')
    return model
