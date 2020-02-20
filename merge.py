import os

path = r'D:\Python\saveVip\video'
os.chdir(path)
cmd = "copy /b *.ts new.mp4"
os.system(cmd)
os.system('del /Q *.ts')
print("successfully!")
