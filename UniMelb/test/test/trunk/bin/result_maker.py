import os
for f in os.listdir("/home/arbazk/MTT/UniMelb/test/test/trunk/bin/results/"):
	print f
	if f.startswith("result"):
		fl=open("results/"+f)
		g=open("results/o_"+f,"w")
		for line in fl:
			l=line.split()
			try:
				g.write(l[0]+"\t"+l[-1]+"\n")
			except:
				pass
				
