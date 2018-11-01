from core.speakout import tts_main
from core import wav2pcm
import multiprocessing
import re
from setting import settings
from datetime import datetime

queue = multiprocessing.JoinableQueue()  # 进程间通信所用
# share_value = multiprocessing.Value("i", 0)  # 进程间共享所用
lock = multiprocessing.Lock()  # 进程间共享内存时，采用锁同步机制

def make_data(queue, num_list):
    for i in num_list:
        dt = datetime.now()
        nowtime = dt.strftime("%Y%m%d%H%M%S%f")
        record_path = settings.SPEACK_PATH + nowtime + r".wav"  # 以时间命名
        tts_main(i, record_path)
        queue.put(record_path)
    queue.join()


def handle_data(queue,lock):
    while True:
        data = queue.get()
        # print('Get from queue.')
        lock.acquire()
        wav2pcm.audio_play(data)
        lock.release()
        queue.task_done()       #向q.join()发送一次信号,证明一个数据已经被取走了


def text_vad(respond_words):
    # pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| |…|（|）'
    # test_text = 'b,b.b/b;b\'b`b[b]b<b>b?b:b"b{b}b~b!b@b#b$b%b^b&b(b)b-b=b_b+b，b。b、b；b‘b’b【b】b·b！b b…b（b）b'
    pattern = r',|\.|;|\?|:|!|，|。|、|；|·|！| |…|（|）'
    result_list = re.split(pattern, respond_words)
    re_list = [x for x in result_list if x!='']
    return re_list      # 返回列表形式的数据


if __name__ == "__main__":
    respond_words = '这几天心里颇不宁静。今晚在院子里坐着乘凉，忽然想起日日走过的荷塘，在这满月的光里，总该另有一番样子吧。月亮渐渐地升高了，墙外马路上孩子们的欢笑，已经听不见了；'
    result_list = text_vad(respond_words)

    make_wave = multiprocessing.Process(target=make_data, args=(queue, result_list, ))  # 生成数据进程
    read_wave = multiprocessing.Process(target=handle_data, args=(queue,lock ))
    read_wave.daemon = True      #设为守护线程

    make_wave.start()
    read_wave.start()

    make_wave.join()
    # read_wave.join()
    print('Ended!')

    #主进程等--->p1,p2,p3等---->c1,c2
    #p1,p2,p3结束了,证明c1,c2肯定全都收完了p1,p2,p3发到队列的数据
    #因而c1,c2也没有存在的价值了,应该随着主进程的结束而结束,所以设置成守护进程