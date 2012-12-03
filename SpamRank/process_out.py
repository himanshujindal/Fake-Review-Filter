import csv
res_map = {}
f = open('out', 'r')
for line in f:
    if 'ITERATION' not in line:
        a = line.split(',')
        res_map.setdefault(a[0], [])
        res_map[a[0]].append(float(a[1]))
f.close()
f = open('out_new.csv', 'w')
try:
    writer = csv.writer(f)
    writer.writerow(['Review_id', 'Iteration 1', 'Iteration 2', 'Iteration 3', 'Iteration 4'])
    for key in res_map:
        values = res_map[key]
        writer.writerow([key, values[0], values[1], values[2], values[3]])
finally:
        f.close()
