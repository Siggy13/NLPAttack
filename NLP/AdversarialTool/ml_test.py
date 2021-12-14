import numpy as np
from sklearn.linear_model import LinearRegression
# import textattack

X = np.array([[1,1],[1,2],[2,2],[2,3]])

y = np.dot(X,np.array([1,2]))+3

reg = LinearRegression().fit(X,y)

def predict(inputText):
    print(inputText)
    predict = reg.predict([inputText])
    return predict 

# print(predict())