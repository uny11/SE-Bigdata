
import os
import time

# Array
# file_status_array = os.stat('bigdata.sqlite')
# print(file_status_array)

# vars
(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat('bigdata.sqlite')
print(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime)
print(size,' en bytes')
print(size/1024,' en KB')

# Los tiempos de acceso, modificación y creación necesitan ser formateados para ser comprensibles
# Para formatear estos tiempos usaremos time.ctime()

print(time.ctime(ctime))  # Output: 'Tue Dec 30 08:35:53 2014'

time.ctime(atime)  # Output: 'Tue Jan 13 09:15:29 2015'

time.ctime(mtime)  # Output: 'Mon Jan 12 08:57:29 2015'
