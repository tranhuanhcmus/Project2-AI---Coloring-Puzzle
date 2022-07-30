from utilities.util_funcs import model_to_matrix

def read_file(file_path):
    try:
        input_File = open(file_path, 'r')

        input_File.readline()#skip line 1
        
        temp=input_File.read().splitlines()#read matrix
        matrix=[]
        for i in temp:
            matrix.append([int(numeric_string) for numeric_string in i.split()])

        input_File.close()
    except FileNotFoundError:
        raise ValueError('File does not exist!!!')
    except ValueError:
        raise ValueError('Matrix contains data that is not a number!!!')

    return matrix


def write_file(file_path, model, rows, cols):
    try:
        writer = open(file_path, 'w')
        writer.write(str(rows) + ' ' + str(cols))
        writer.writelines(['\n' + ' '.join(row) for row in model_to_matrix(model, rows, cols)])
        writer.close()
    except:
        raise ValueError('Can not write data to file!!!')
