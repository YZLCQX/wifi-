#21:48 2020/1/26
def cfp(file_rows):
    i = []
    if file_rows <= 200:
        i.append(False)
        i.append(int(200/file_rows))
        return i
    else:
        i.append(True)
        i.append(int(file_rows/200))
        return i

if __name__ == '__main__':
    print(cfp(425))
