text = open("Email-EuAll.txt", "r")
h = open('emailnoloop.txt', 'w') #creacion archivo con semilla para IC
lineas = text.readlines()
for i in range(len(lineas)):
    lineas[i] = lineas[i].rstrip("\n").split("\t")
    if lineas[i][0] == lineas[i][1]:
        None
    else:
        aux = lineas[i][0] + " " + lineas[i][1] + " 1" +"\n"
        h.write(str(aux))
#mensaje[i] = mensaje[i].rstrip("\n").split(" ")