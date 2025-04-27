dat = []
with open('./imgdat.py', "r") as file:
            content = file.read()
            dat = content.split('},')
im = []
for l in dat:
	# print(l)
	ll = l[l.find('file_path')+14: l.find('.jpg')]
	im.append(ll)

# print(len(im), im)
# print(im)
pre = 'https://image.tmdb.org/t/p/original/'
r = ''
c = len(im) 
for i in range(c):
	n = im[i] 
	r += '<img src="' + pre + n + '.jpg"></br>'

print(r)


	 	

