from test_accuracy_old import testOld
from test_accuracy_new import testNew

if __name__ == '__main__':
    dir_name = 'outcomes_obo_3'
    
    if 'old' in dir_name:
        testOld(dir_name)
    else:
        testNew(dir_name)