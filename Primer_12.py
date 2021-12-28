def hybridicering(prim1,prim2):
    n1 = len(prim1)
    n2 = len(prim2)
    nmin=min(n1,n2)
# Lav en tekststreng som svarer til den primer2 skal match med. Husk omvendt rækkefølge
    matchPrim2 = ""
    for i in range(n2):
        if prim2[n2-1-i]=="A":
            matchPrim2 +="T"
        elif prim2[n2-1-i]=="T":
            matchPrim2 +="A"
        elif prim2[n2-1-i]=="C":
            matchPrim2 +="G"
        elif prim2[n2-1-i]=="G":
            matchPrim2 +="C"
    print("match streng: " + matchPrim2)
# Check for match
    for i in range(n1):
        b = 0
        for j in range(nmin-i):
            if prim1[i+j]==matchPrim2[j]:
                b += 1
            else:
                break
        if b > 0:
            print("hybridisering mellem primere. Længde: " + str(b) + " Position " + str(i+1) + " på primer 1")
# Check for match
    for i in range(n2):
        b = 0
        nmin=min(n1,n2)
        for j in range(nmin-i):
            if prim1[j]==matchPrim2[i+j]:
                b += 1
            else:
                break
        if b > 0:
            print("hybridisering mellem primere. Længde: " + str(b) + " Position " + str(i+1) + " på primer 2")


igen = "y"
while igen == "y":
    primer1 = input("Indtast primer 1: ")
    primer2 = input("Indtast primer 2: ")
    print("Primer 1 er: " + primer1)
    print("Primer 2 er: " + primer2)
    hybridicering(primer1,primer2)
    igen = input("Prøv igen? y/n ")