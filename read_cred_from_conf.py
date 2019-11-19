# test code
with open('send_email.conf') as file:
    content = file.read().splitlines()
    print(content)
    print (content[0], content[1])
    #return {content[0]:content[1]}
alfa = {'IOn':'maria'}

for key in alfa:
    print( key, alfa[key])