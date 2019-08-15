from controller.common_view.common_pandas_function import read_data
from ml_lib.supervised import import_lib
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

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
    def read_hold(self, fileLocation, task):
        # holding task obj in self
        self.task = task

        # reading data
        self.data_frame = read_data(fileLocation)

        self.call_for_sklearn()
    # importing particular selected library only
    def call_for_sklearn(self):

        self.models = import_lib(self.task["model"])

        self.find_label_feature()

    def find_label_feature(self):
        if self.task["select_input"] == "all":
            self.all_inputs = self.data_frame[['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']].values

        self.all_classes = self.data_frame[self.task["label"]].values

        self.data_separate()

    # separate data for train and test
    def data_separate(self):
        (train_inputs, test_inputs, train_classes, test_classes) = train_test_split(self.all_inputs, self.all_classes,
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
