import requests
import hashlib
import sys

def requestPassApi(dataPass): #requesting the data from the server
    url = 'https://api.pwnedpasswords.com/range/'+ dataPass #url of the server with data
    res = requests.get(url)
    if res.status_code != 200: #for erroe 400 or bad request
        raise RuntimeError(f'somthing went wrong and your status code is {res.status_code} please try again!')
    return res
def leakCount(hashes,hashCheck): #find no of time the password got leaked
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h,count in hashes:
        if h == hashCheck:
            return count
    return 0


def checkPassApi(password): #checking the givven password
    sha1Pass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper() #convert password to SHA1
    first,last = sha1Pass[:5], sha1Pass[5:] #we only need first 5 letters soo diving the hex
    response = requestPassApi(first)#request the api using first 5 letters 
    return leakCount(response,last)#sends the response and remaining lettes to leakCount



def main(args):
    for password in args:
        count = checkPassApi(password)
        if count:
            print(f'{password} was found {count} many time u have to change you\'r password')
        else:
            print(f'{password} was not found u can use it!')
    return 'done!'

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))#using sys module



    

'''
.status_code => to check the response from the server 200 = good and 400 is bad
.splitlines => used for spliting of the texts
.encode => do codes the password in words
.hexdigest() => converts the words into hex values(SHA1)
.upper() => everything will be in capital  '''