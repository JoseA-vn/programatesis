import csv
import time 

start_time = time.time()
ejemplo = None
variable = 'shallow'
with open(variable + '.csv', 'w', newline='') as file:
    escribir = csv.writer(file, delimiter=';')
    escribir.writerow([123, 'esto', 'pico'])
    escribir.writerow([1234, 'esto', 'pico'])
last_time = time.time() - start_time

print('se demoró un total de %f segundos' % last_time)
