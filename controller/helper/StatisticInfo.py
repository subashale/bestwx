import numpy as np


class StatisticInfo:
    def __init__(self, df):
        self.df = df
        self.storeType = {}

        for attribute in df.keys():
            self.storeType[attribute] = self.getType(attribute)

    def getType(self, attributeName):
        datatype = {}
        for i in self.df[attributeName].tolist():
            # checking nan or empty
            if i == i:
                datatype[type(i)] = i
            else:
                datatype["None"] = i

        if len(datatype) == 1 and "None" in datatype.keys():
            return "None"
        else:

            if len(datatype) == 1 and float in datatype: return "Real"
            if len(datatype) == 2 and float in datatype and int in datatype: return "Real"
            if len(datatype) == 2 and float in datatype and "None" in datatype.keys(): return "Real"

            if len(datatype) == 1 and int in datatype: return "Integer"
            if len(datatype) == 2 and int in datatype and "None" in datatype.keys(): return "Integer"

            if len(datatype) > 1 and str in datatype and (float in datatype or int in datatype):
                return "Mix-Danger"

            if str in datatype:
                if len(datatype) < 2 or "None" in datatype.keys():
                    unique = {}
                    count = 0
                    for i in self.df[attributeName]:
                        unique[i] = count + 1
                        # now calculate value
                    if len(unique) == 2:
                        return "Binominal"
                    elif len(unique) > 2:
                        return "Polynominal"
                    else:
                        return "Single Value"

    def showType(self, attributeName):
        return self.storeType[attributeName]

    def getMissing(self, attributeName):
        return self.df[attributeName].isna().sum()

    def getStatistics(self, attributeName):
        if self.showType(attributeName) == "Polynominal" or self.getType(attributeName) == "Binominal":
            least, most, values = self.getValues(attributeName)
            return {"Least": least, "Most": most, "Values": values}
        elif self.getType(attributeName) == "Real" or self.getType(attributeName) == "Integer":
            minv, maxv, avg = self.getAverageValue(attributeName)
            return {"Min": minv, "Max": maxv, "Average": avg}
        elif self.getType(attributeName) == "Single Value":
            singleValue = str(self.df[attributeName][0])
            countSingleValue = str(len(self.df[attributeName]))
            return {"Least": singleValue + "(" + countSingleValue + ")",
                    "Most": singleValue + "(" + countSingleValue + ")",
                    "Value": singleValue + "(" + countSingleValue + ")"}
        else:
            # return "No data type found" + attributeName
            return {"Least": None, "Most": None, "Values": None}

    # Polinominal or Binomial
    def getValues(self, attributeName):
        countData = {}
        for i in self.df[attributeName]:
            # skipping empty or non values
            if i == i:
                if i not in countData:
                    countData[i] = 1
                else:
                    oldValue = countData[i]
                    countData[i] = oldValue + 1

        key_max = max(countData.keys(), key=(lambda k: countData[k]))
        key_min = min(countData.keys(), key=(lambda k: countData[k]))

        return key_min + " : " + str(countData[key_min]), key_max + " : " + str(countData[key_max]), countData

    # Real or Integer
    def getAverageValue(self, attributeName):
        minv = np.nanmin(self.df[attributeName])
        maxv = np.nanmax(self.df[attributeName])
        avg = self.df[attributeName].sum() / len(self.df[attributeName])
        return minv, maxv, avg