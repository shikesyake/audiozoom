path = 'named_pipe'

f = open(path, 'rb')
while True:
	data = f.read(1)
	print(data)
	if not data:
		f.close()
		break

# import os
# import random
# path = 'named_pipe'

# f = open(path, 'wb')
# while True:
# 	data = random.randint(0, 255)
# 	f.write(bytes([data]))

# f.close()

# # path = 'sample/茨城県立IT未来高等学校 2 copy.wav'
# # out = 'sample/out.txt'

# # f = open(path, 'rb')
# # ff = open(out, 'wb')
# # for i in range(500):
# # 	data = f.read(1)
# # 	print(data)
# # 	if data != b'0':
# # 		ff.write(bytes(data))

# # f.close()
# # ff.close()