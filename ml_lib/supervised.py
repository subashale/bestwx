import sklearn

#from sklearn.tree import DecisionTreeClassifier
#from sklearn.linear_model import LogisticRegression

# For now we are totally depended on sklearn ;#

def find_model_group():
    pass

def import_lib(models):
    #from sklearn.tree import DecisionTreeClassifier as dt
    #clf = dt()
    #return clf

    model_obj = {}

    for model in models:
        # check before importing its root model and create obj

        # tree_model
        if model == "DecisionTreeClassifier":
            from sklearn.tree import DecisionTreeClassifier as dt
            dt_model = dt()
            model_obj[model] = dt_model

        # linar model
        elif model == "LogisticRegression":
            from sklearn.linear_model import LogisticRegression as lr
            lr_model = lr()
            model_obj[model] = lr_model

    return model_obj


def call():
    pass
