def table_pretty(csvfile):
    '''Display tables from CSV in a pretty way'''
    my_file = os.path.join(THIS_FOLDER, csvfile)
    with open(my_file, "r") as fp:
        x = from_csv(fp)
    #estados=[]
    for row in x:
        row.border = False
        row.header = False
        #estados.append(row.get_string(fields=["Estado"]).strip())
    print(x)
    return x