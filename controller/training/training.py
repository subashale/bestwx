from controller.common_view.common_pandas_function import read_data
from ml_lib.supervised import import_lib
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import numpy as np
# tasks
# reading dataset as df
# finding label and features
# separating for training and testing
# using model
# training model
# predicting model
# report generation
# ;#

class Training:
    def __init__(self):
        pass

    # for holding given object and reading data
    def read_hold(self, processInfo):
        # holding task obj in self
        self.processInfo = processInfo

        print(processInfo.getTask())
        # reading data
        # self.data_frame = dataFrame

        self.call_for_sklearn()
    # importing particular selected library only
    def call_for_sklearn(self):

        self.models = import_lib(self.processInfo.getAlgos())

        self.find_label_feature()

    def find_label_feature(self):
        # if self.processInfo["select_input"] == "all":
        #     self.all_inputs = self.data_frame[['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']].values

        # self.all_classes = self.data_frame[self.processInfo["label"]].values
        index = self.processInfo.getHeaders()
        outputValue = self.processInfo.getOutputFeature()
        # output must be inside headers
        if outputValue not in self.processInfo.getHeaders():
            return False
        outputIdx = self.processInfo.getHeaders().index(outputValue)

        data = np.array(self.processInfo.getRows())

        input = np.delete(data, [outputIdx], 1)
        output = data[:, outputIdx]

        self.data_separate(input, output)

    # separate data for train and test
    def data_separate(self, input, output):
        (train_inputs, test_inputs, train_classes, test_classes) = train_test_split(input, output,
                                                                                    train_size=0.7, random_state=1)
        self.fit(train_inputs, test_inputs, train_classes, test_classes)

    # train each models and display result
    def fit(self, train_inputs, test_inputs, train_classes, test_classes):
        # training on each models
        results = {}
        predictions = {}
        for name, model in self.models.items():
            model_fit = model.fit(train_inputs, train_classes)
            # adding model to dictionary
            results[name] = model_fit
            y_pred = model_fit.predict(test_inputs)

            # y prediction to dictionary
            predictions[name] = y_pred

        for result , y_pred in zip(results, predictions):

            print("--------- result of "+result+"----------")

            print("score", results[result].score(test_inputs, test_classes))
            print(classification_report(test_classes, predictions[y_pred]))
            print(confusion_matrix(test_classes, predictions[y_pred]))
