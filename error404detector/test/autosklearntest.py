
from systemtools.basics import *
import autosklearn.classification
cls = autosklearn.classification.AutoSklearnClassifier(ensemble_size=1, initial_configurations_via_metalearning=0)
features = []
labels = []
for i in range(1000):
    if getRandomFloat() > 0.5:
        current = [0, 0, 1]
        label = 1
    else:
        current = [0, 1, 0]
        label = 1
    features.append(current)
    labels.append(label)
cls.fit(features, labels)
predictions = cls.predict([[0, 0, 1]])
print(predictions)
exit()
