#datamodelUtil

#cols is a string array of column names to remove
#returns new data  with removed cols
#data is dictionary of data
def removeColsFromData(data, cols):
    if data != None:
        for col_name in cols:
            data.pop(col_name, None)
        return data
        
#takes array produced by column and returns median
def medianOfCol(col):
    if len(col) == 0:
        return None
    elif len(col) % 2 == 0:
        return (col[len(col)//2 - 1] + col[len(col)//2]) / 2
    else:
        return col[len(col)//2]

def meanOfCol(col):
    if len(col) == 0:
        return None
    return float(sum(col)) / float(len(col))
#returns array in format [colA0 * colB0, ..., colAn*colBn]
#if arrays are not same size, then processing will stop after shortest array completes
def productOfCols(colA, colB):
    minLength = min(len(colA), len(colB))
    return [colA[i] * colB[i] for i in range(minLength)]