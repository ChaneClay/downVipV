import requests
import time
from multiprocessing import Pool
import os

des = './video/'


def download(i):
    start = time.time()
    size = 0
    url = 'https://youku.cdn7-okzy.com/20200216/17191_347a9da2/1000k/hls/191d093cc3a00%04d.ts' % i
    response = requests.get(url, stream=True)
    # stream参数设置成True时，它不会立即开始下载，当你使用iter_content或iter_lines遍历内容或访问内容属性时才开始下载
    chunk_size = 1024  # 每次块大小为1024
    content_size = int(response.headers['content-length'])  # 返回的response的headers中获取文件大小信息

    total = str(round(float(content_size / chunk_size / 1024), 2)) + "MB"
    path = des+'{}'.format(url[-10:])
    with open(path, 'wb') as file:
        for data in response.iter_content(chunk_size=chunk_size):  # 每次只获取一个chunk_size大小
            file.write(data)
            size = len(data) + size
            print('\r' + "第" + str(i) + "块已经下载：" + int(size / content_size * 100) * "█" + " [" + str(
                round(size / chunk_size / 1024, 2)) + "MB/" + total + "]" + "[" + str(
                round(float(size / content_size) * 100, 2)) + "%" + "]", end="")

    end = time.time()  # 'r'每次重新从开始输出，end = ""是不换行
    print("总耗时:" + str(round(end - start, 2)) + "秒" + '\r')


if __name__ == '__main__':

    po = Pool(3)
    for i in range(10):
        po.apply_async(download, args=(i,))

    po.close()
    po.join()

    os.chdir(des)
    cmd = "copy /b *.ts translate.mp4"
    os.system(cmd)
    os.system('del /Q *.ts')
    print("successfully!")
