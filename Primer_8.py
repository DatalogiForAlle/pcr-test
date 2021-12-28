def read_DNA(file):
# Læs FASTA-fil, fjerne unødige tegn og returnere DNA-koden som en tekststreng
    f = open(file) # Åbner filen
    f.readline()   # læser linjen med beskrivelsen af gensekvensen
    gen_kode = f.readline()
    # Fjern end-of-line karakteren (\n) i slutningen af DNA-strengen
    # dvs fjern det sidste tegn i tekst-strengen gen_kode inden den returneres
    return gen_kode[0:-1]

def count_bases(gen_kode):
# Funktionen finder antallet af de 4 forskellige baser
# Forholdet mellem antal C+G og A+T baser, bestemmer
# hvordan primeren binder til DNA-strengen
    noA = gen_kode.count('A')    
    noC = gen_kode.count('C')    
    noG = gen_kode.count('G')    
    noT = gen_kode.count('T')
    # find summen af de 4 baser = samlet længde af gen_koden
    noBaser = noA + noC + noG + noT
    print("Antallet af A-baser: " + str(noA))
    print("Antallet af C-baser: " + str(noC))
    print("Antallet af G-baser: " + str(noG))
    print("Antallet af T-baser: " + str(noT))
    print("Antal baser i alt: " + str(noBaser))
    
def smeltepunkt(gen_kode):
# Funktionen finder antallet af de 4 forskellige baser
# Derefter beregnes smeltepunktet, som er den temperatur
# hvor primeren sætter sig fast på DNA-molekylet
    noA = gen_kode.count('A')    
    noC = gen_kode.count('C')    
    noG = gen_kode.count('G')    
    noT = gen_kode.count('T')
    noBaser = noA + noC + noG + noT
    # beregne smeltepunktet
    temp = 64.9 + 41*(noC + noG)/noBaser - 41*16.4/noBaser
    return temp

def check_slutning(gen_kode):
    noBaser = len(gen_kode)
    n = 0
    # check sidste 5 baser
    for i in range(5):
        if gen_kode[noBaser-1-i] == "G" or gen_kode[noBaser-1-i] == "C":
            n +=1
    return n

DNA = read_DNA("DNA1.csv")
print(DNA)
print(len(DNA))
count_bases(DNA)
text = "DNA-strengens smeltepunkt er {:.2f}°C"
print(text.format(smeltepunkt(DNA)))

igen = "y"
while igen == "y":
    start = int(input("Indtast startposition: "))
    length = int(input("Indtast længde af primer: "))
    primer = DNA[start-1:start-1+length]
    text = "Primerens smeltepunkt er {:.2f}°C"
    print(text.format(smeltepunkt(primer)))
    print("Antal C eller G-baser i slutningen af primeren: " +str(check_slutning(primer)))
    igen = input("Prøv igen? y/n ")



