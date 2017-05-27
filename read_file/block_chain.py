#coding:utf-8
import struct
import binascii
import pickle
import os
import codecs
import hashlib
def get_transaction_hash(content):
    content_bin = codecs.decode(content,'hex_codec')
    transaction_hash=hashlib.sha256(hashlib.sha256(content_bin).digest()).digest()
    return codecs.encode(transaction_hash[::-1],'hex_codec')
def get_check_flag(attr='output_index'):
    if attr == 'output_index':
        flag = str(b'ffffffff')[2:-1]
    else:
        base = '0'
        flag = ''
        for _ in range(64):
            flag+=base
    return flag
CHECK_FLAG = get_check_flag()
def str_reverse(string_):
    if len(string_)<=2:
        return string_
    else:
        return str_reverse(string_[2:])+string_[0:2]
class block(object):
    def __init__(self,magic_num, block_size, block_head, block_trans_num, coinbase_trans, normal_trans):
        self._magic_num = magic_num
        self._block_size = block_size
        self._block_head = block_head
        self._block_trans_num = block_trans_num
        self._coinbase_trans = coinbase_trans
        self._normal_trans = normal_trans
    @property
    def magic_num(self):
        return self._magic_num
    @property
    def block_size(self):
        return self._block_size
    @property
    def block_head(self):
        return self._block_head
    @property
    def block_trans_num(self):
        return self._block_trans_num
    @property
    def coinbase(self):
        return self._coinbase_trans
    @property
    def normal_trans(self):
        return self._normal_trans
    def print_Info(self, block_no):
        print('\n******************************\n  第', block_no, '个区块 基本信息\n')
        print('     区块大小：', self.block_size)
        print('     区块头：')
        print('         版本：',self.block_head["version"])
        print('         父区块头Hash：', self.block_head["father_head_hash"])
        print('         Merkle根：', self.block_head["Merkle_root"])
        print('         时间戳：', self.block_head["time_stamp"])
        print('         难度目标：', self.block_head["difficulty_goal"])
        print('         Nonce：',self.block_head["Nonce"])
        print('     交易计数：', self.block_trans_num)
        print('\n******************************')
    def print_normal_trans_Info(self, block_no):
        print('\n  第', block_no, '个区块 普通交易基本信息\n')
        print('     交易计数：', len(self.normal_trans))
        print('\n******************************')
class coinbase(object):
    def __init__(self,type,version,input_count,trans_hash, trans_output_index, data_size, data, order_no, output_count, total,\
                                     lock_script_size,lock_script, lock_time):
        self._type = type
        self._version = version
        self._input_count = input_count
        self._trans_hash = trans_hash
        self._trans_output_index = trans_output_index
        self._data_size = data_size
        self._data = data
        self._order_no = order_no
        self._output_count = output_count
        self._total = total
        self._lock_script_size = lock_script_size
        self._lock_script = lock_script
        self._lock_time = lock_time
    @property
    def type(self):
        return self._type
    @property
    def version(self):
        return self._version
    @property
    def input_count(self):
        return self._input_count
    @property
    def trans_hash(self):
        return self._trans_hash
    @property
    def trans_output_index(self):
        return binascii.b2a_hex(self._trans_output_index)
    @property
    def data_size(self):
        return self._data_size
    @property
    def data(self):
        return self._data
    @property
    def order_no(self):
        return self._order_no
    @property
    def output_count(self):
        return self._output_count
    @property
    def total(self):
        return self._total
    @property
    def lock_script_size(self):
        return self._lock_script_size
    @property
    def lock_script(self):
        return self._lock_script
    @property
    def lock_time(self):
        return self._lock_time
    def print_Info(self,block_no):
        print('\n  第',block_no,'个区块coinbase 基本信息\n')
        print('     版本：     ',self.version)
        print('     输入计数器：',self.input_count)
        print('     交易hash：',self.trans_hash,type(self.trans_hash),len(self.trans_hash))
        print('     交易输出索引：',self.trans_output_index,'变换后：',int(self.trans_output_index,16))
        print('     输出计数器：', self.output_count)
        print('     总量：', self.total)
        print('     锁定时间：', self.lock_time)
        print('\n******************************')

class normal_trans(object):
    def __init__(self, _type, version, input_count, input, output_count, output, lock_time, according_hash):
        self._type = _type
        self._version = version
        self._input_count = input_count
        self._input = input
        self._output_count = output_count
        self._output = output
        self._lock_time = lock_time
        self._according_hash = according_hash
    @property
    def type(self):
        return self._type
    @property
    def version(self):
        return self._version
    @property
    def input_count(self):
        return self._input_count
    @property
    def input(self):
        return self._input
    @property
    def output_count(self):
        return self._output_count
    @property
    def output(self):
        return self._output
    @property
    def lock_time(self):
        return self._lock_time
    def according_hash(self):
        return self._according_hash
    def print_Info(self, block_no,normal_trans_no):
        print('\n  第',block_no,'个区块，第',normal_trans_no,'个普通交易 基本信息\n')
        print('         交易hash:',self.according_hash())
        print('    输入计数器：', self.input_count)
        print('     交易哈希值：')
        for i in range(self.input_count):
            print('     ',i+1,'-',self.input[i]["trans_hash"],' 输出索引 - ',self.input[i]["output_index"])
            print('         解锁脚本：',self.input[i]["unlock_script"])
        print('    输出计数器：', self.output_count)
        print('     总量')
        for i in range(self.output_count):
            print('     ',i+1,'-',self.output[i]["total"])
            print('         锁定脚本：',self.output[i]["lock_script"])
        print('     锁定时间：', self.lock_time)
        print('\n******************************')
def get_transaction(file,block_size_count,_type):
    # 挖矿交易
    if _type == 'coinbase':
        coinbase_size = 0
        # 版本，这笔交易参照的规则
        version = int(bytes(str_reverse(str(binascii.b2a_hex(file.read(4)))[2:-1]),encoding="utf8"),16)
        # coinbase 输入计数器
        input_count = int(binascii.b2a_hex(file.read(1)),16)
        # coinbase 交易hash，不引用任何一个交易，值全部为0
        trans_hash = str_reverse(str(binascii.b2a_hex(file.read(32)))[2:-1])
        # 交易输出索引
        trans_output_index = file.read(4) #int(binascii.b2a_hex(file.read(4)),16)
        # coinbase 数据长度
        data_size = int(binascii.b2a_hex(file.read(1)),16)
        data = binascii.b2a_hex(file.read(data_size))
        # 顺序号
        order_no = binascii.b2a_hex(file.read(4))
        output_count = int(binascii.b2a_hex(file.read(1)),16)
        total = int(bytes(str_reverse(str(binascii.b2a_hex(file.read(8)))[2:-1]),encoding="utf8"),16)
        lock_script_size = int(binascii.b2a_hex(file.read(1)),16)
        lock_script = binascii.b2a_hex(file.read(lock_script_size))
        lock_time = int(binascii.b2a_hex(file.read(4)),16)
        transaction_re = coinbase(_type,version,input_count,trans_hash, trans_output_index, data_size, data, order_no, output_count, total,\
                                     lock_script_size,lock_script, lock_time)
        block_size_count_re = block_size_count+4+1+32+4+1+data_size+4+1+8+1+lock_script_size+4
        coinbase_size = 4+1+32+4+1+data_size+4+1+8+1+lock_script_size+4
        return transaction_re, block_size_count_re,coinbase_size
    # 普通交易
    elif _type == 'normal':
        block_size_count_re = block_size_count
        # 版本号
        version_ff = binascii.b2a_hex(file.read(4))
        version = int(bytes(str_reverse(str(version_ff)[2:-1]),encoding="utf8"),16)
        # 输入计数器
        input_count_ff = binascii.b2a_hex(file.read(1))
        input_count = int(input_count_ff,16)
        normal_input = []
        Cur_trans_bytes = version_ff + input_count_ff
        block_size_count_re = block_size_count_re +4+1
        for i in range(input_count):
            Cur_input = {}
            trans_hash_ff = binascii.b2a_hex(file.read(32))
            Cur_input["trans_hash"] = str_reverse(str(trans_hash_ff)[2:-1])
            # Cur_input["trans_hash"] = binascii.b2a_hex(file.read(32))
            # 输出索引 - 小端格式
            output_index_ff = binascii.b2a_hex(file.read(4))
            Cur_input["output_index"] = int(bytes(str_reverse(str(output_index_ff)[2:-1]),encoding='utf-8'),16)
            unlock_script_size_ff = binascii.b2a_hex(file.read(1))
            Cur_input["unlock_script_size"] = int(unlock_script_size_ff,16)
            unlock_script_ff = binascii.b2a_hex(file.read(Cur_input["unlock_script_size"]))
            Cur_input["unlock_script"] = unlock_script_ff
            Cur_input["serial"] = binascii.b2a_hex(file.read(4))
            normal_input.append(Cur_input)
            Cur_trans_bytes = Cur_trans_bytes + trans_hash_ff + output_index_ff + unlock_script_size_ff + unlock_script_ff + \
                            Cur_input["serial"]
            block_size_count_re = block_size_count_re + 32+4+1+Cur_input["unlock_script_size"]+4
        # 输出计数器
        output_count_ff = binascii.b2a_hex(file.read(1))
        output_count = int(output_count_ff,16)
        block_size_count_re = block_size_count_re+1
        normal_output = []
        Cur_trans_bytes = Cur_trans_bytes + output_count_ff
        for i in range(output_count):
            Cur_output = {}
            total_ff = binascii.b2a_hex(file.read(8))
            Cur_output["total"] = int(bytes(str_reverse(str(total_ff)[2:-1]),encoding="utf8"),16)
            lock_sp_size_ff = binascii.b2a_hex(file.read(1))
            Cur_output["lock_script_size"] = int(lock_sp_size_ff,16)
            Cur_output["lock_script"] = binascii.b2a_hex(file.read(Cur_output["lock_script_size"]))
            block_size_count_re = block_size_count_re + 8+1+Cur_output["lock_script_size"]
            normal_output.append(Cur_output)
            Cur_trans_bytes = Cur_trans_bytes + total_ff + lock_sp_size_ff + Cur_output["lock_script"]
        lock_time = binascii.b2a_hex(file.read(4))
        block_size_count_re = block_size_count_re + 4
        Cur_trans_bytes += lock_time
        according_hash = get_transaction_hash(str(Cur_trans_bytes)[2:-1])
        transaction_re = normal_trans(_type, version, input_count, normal_input, output_count, normal_output, lock_time,according_hash)
        return transaction_re,block_size_count_re
def get_delta(trans_output_index,FLAG):
    delta = 0
    for i in range(len(trans_output_index)):
        if trans_output_index[i]!=FLAG[i]:
            delta += 1
        else:
            break
    return delta
def get_one_block(file,block_no,offset = 0,block_trans_num_s = 1,read_from_now = False):
    if not read_from_now:
        for i in range(block_no-1):
            # 神奇数
            file.read(4)
            # 区块大小
            block_size = file.read(4)
            block_size = struct.unpack('i', block_size)[0]
            file.read(block_size)
    else:
        file.seek(-1*offset,1)
    magic_num = str(binascii.b2a_hex(file.read(4)))[2:-1]
    if magic_num!='f9beb4d9':

        print('区块读取有问题！！！')
        exit()
    block_size = struct.unpack('i',file.read(4))[0]
    # print(block_no,'区块大小：',block_size)
    # 记录当前区块读取了多少字节
    block_size_count = 0
    # block_head = binascii.b2a_hex(file.read(80))
    block_head = {}
    block_head["version"] = int(bytes(str_reverse(str(binascii.b2a_hex(file.read(4)))[2:-1]), encoding="utf8"), 16)
    block_head["father_head_hash"] = str_reverse(str(binascii.b2a_hex(file.read(32)))[2:-1])
    block_head["Merkle_root"] = str_reverse(str(binascii.b2a_hex(file.read(32)))[2:-1])
    block_head["time_stamp"] = int(bytes(str_reverse(str(binascii.b2a_hex(file.read(4)))[2:-1]), encoding="utf8"), 16)
    block_head["difficulty_goal"] = int(bytes(str_reverse(str(binascii.b2a_hex(file.read(4)))[2:-1]), encoding="utf8"),16)
    block_head["Nonce"] = int(bytes(str_reverse(str(binascii.b2a_hex(file.read(4)))[2:-1]), encoding="utf8"), 16)
    block_size_count += 80
    # 交易计数器 1~9
    block_trans_num = binascii.b2a_hex(file.read(block_trans_num_s))
    if read_from_now:
        # 小端格式
        # 去掉fd ，使用剩下的代表交易计数器
        # trans_num_confirm = int(bytes(str_reverse(str(block_trans_num)[2:-1])[0:-2],encoding='utf8'),16)+int(bytes(str_reverse(str(block_trans_num)[2:-1])[-2:],encoding='utf8'),16)
        trans_num_confirm = int(bytes(str_reverse(str(block_trans_num)[2:-1])[0:-2],encoding='utf8'),16)

        print('交易计数：',trans_num_confirm,'变换前:',str_reverse(str(block_trans_num)[2:-1])[0:-2])
    else:
        trans_num_confirm = int(block_trans_num,16)

    block_size_count += 1
    normal_trans = []

    for i in range(trans_num_confirm):
        # 挖矿交易
        if i == 0:
            coinbase,block_size_count,coinbase_size = get_transaction(file,block_size_count,_type = 'coinbase')
            # 检查coinbase是否读对了
            delta = get_delta(str(coinbase.trans_output_index)[2:-1],CHECK_FLAG)
#            if read_from_now:
#                exit()
            if  delta!=0:
                # file 文件指针要向前移动
                offset = block_trans_num_s + coinbase_size + 80 + 8
                block_size,block_re = get_one_block(file,block_no=block_no,offset=offset,block_trans_num_s=int(delta/2)+1,read_from_now=True)
                return block_size,block_re
        # 普通交易, 每个普通交易都对应一个hash值
        else:
            Cur_normal_trans, block_size_count = get_transaction(file,block_size_count, _type='normal')
            normal_trans.append(Cur_normal_trans)
    if block_size != block_size_count:
        print('区块大小不一致')
        # exit()
    block_re = block(magic_num, block_size, block_head, trans_num_confirm, coinbase, normal_trans)
    # +8 是因为需要加上神奇数和表示区块大小的字节
    return block_size +8,block_re
def get_constant_block(file,file_size, block_num,method=2, read_all_blocks = True):
    # method = 1表示使用第一种方法,目前还存在问题
    # method = 2表示使用第二种方法
    # read_all_blocks = True 表示是否读取所有区块
    blocks = []
    if not read_all_blocks:
        if method == 1:
            for i in range(block_num):
                magic_num = str(binascii.b2a_hex(file.read(4)))[2:-1]
                print(magic_num)
                if magic_num != 'f9beb4d9':
                    print(i+1,'区块读取有问题！！！')
                    exit()
                block_size = struct.unpack('i', file.read(4))[0]
                block_size_count = 0
                # block_head = binascii.b2a_hex(file.read(80))
                block_head = {}
                block_head["version"] = int(bytes(str_reverse(str(binascii.b2a_hex(file.read(4)))[2:-1]), encoding="utf8"), 16)
                block_head["father_head_hash"] = str_reverse(str(binascii.b2a_hex(file.read(32)))[2:-1])
                block_head["Merkle_root"] = str_reverse(str(binascii.b2a_hex(file.read(32)))[2:-1])
                block_head["time_stamp"] = int(bytes(str_reverse(str(binascii.b2a_hex(file.read(4)))[2:-1]), encoding="utf8"),16)
                block_head["difficulty_goal"] = int(bytes(str_reverse(str(binascii.b2a_hex(file.read(4)))[2:-1]), encoding="utf8"), 16)
                block_head["Nonce"] = int(bytes(str_reverse(str(binascii.b2a_hex(file.read(4)))[2:-1]), encoding="utf8"), 16)
                block_size_count += 80
                block_trans_num = int(binascii.b2a_hex(file.read(1)), 16)
                block_size_count += 1
                normal_trans = []
                for i in range(block_trans_num):
                    # 挖矿交易
                    if i == 0:
                        coinbase,block_size_count = get_transaction(file, block_size_count,_type='coinbase')
                    # 普通交易
                    else:
                        Cur_normal_trans,block_size_count = get_transaction(file,block_size_count, _type='normal')
                        normal_trans.append(Cur_normal_trans)
                if block_size!= block_size_count:
                    print(i+1,'区块大小不一致')
                    print('block_size',block_size,'block_size_count',block_size_count)
                    exit()
                Cur_block = block(magic_num, block_size, block_head, block_trans_num, coinbase, normal_trans)
                blocks.append(Cur_block)
        elif method == 2:
            for block_no in range(block_num):
                block_size, Cur_block = get_one_block(file,block_no+1)
                print(block_no+1)
                blocks.append(Cur_block)
                file.seek(0,0)
    # read all blocks
    else:
        # 表示读取所有区块
        block_no = 0
        file_size_count = 0
        while True:
            block_size, Cur_block = get_one_block(file, block_no + 1)
            block_no += 1
            print(block_no)
            blocks.append(Cur_block)
            file_size_count += block_size
            # print(file_size,'bytes - ',file_size_count,'bytes')
            if file_size_count >= file_size:
                break
            file.seek(0,0)
    return blocks
def print_Menu():
    print('\n******************************')
    print('  有以下可执行操作')
    print('     1：读取区块链中的某个区块；')
    print('     2：读取连续的几个区块.')
    print('\n******************************')
def print_block_Info(block, block_no):
    # 当前区块基本信息
    block.print_Info(block_no)
    # 当前区块对应的 coinbase 基本信息
    block.coinbase.print_Info(block_no)
    # 当前区块对应的 普通交易 基本信息
    block.print_normal_trans_Info(block_no)
    # 当前区块普通交易中某一个交易的基本信息
    normal_trans_no = input('请输入要显示第几个交易信息\n')
    assert int(normal_trans_no) < block.block_trans_num
    block.normal_trans[int(normal_trans_no) - 1].print_Info(block_no, int(normal_trans_no))
def save_trans_graph(blocks):
    # 把blocks 中所有的交易保存下来
    # 挖矿交易 coinbase 中，表示God给了自己一些Bitcoin
    coinbase_graph = {}
    coinbase_value = []
    normal_trans_graph = {}
    for block in blocks:
        coinbase_value.append({block.coinbase.lock_script:block.coinbase.total})
        #print('交易数：',block.block_trans_num)
        #print('普通交易数：',len(block.normal_trans))
        for normal_trans in block.normal_trans:
            # 普通交易中的 in 只有一个
            # print('in:',normal_trans.input_count,'out:',normal_trans.output_count)
            if normal_trans.input_count == 1:
                # in 对应的 pub_key
                script_pub_key = normal_trans.input[0]["unlock_script"]
            Cur_in_key_value = []
            for normal_trans_output_no in range(normal_trans.output_count):
                Cur_in_key_value.append({normal_trans.output[normal_trans_output_no]["lock_script"]:normal_trans.output[normal_trans_output_no]["total"]})
            # 表示之前没有 in 对应的key
            if script_pub_key not in normal_trans_graph.keys():
                normal_trans_graph.update({script_pub_key:Cur_in_key_value})
            # 表示之前有存在 in 对应的 key
            else:
                Cur_in_key_value.extend(normal_trans_graph.get(script_pub_key))
                normal_trans_graph.update({script_pub_key: Cur_in_key_value})
    coinbase_graph.update({'God':coinbase_value})
    with open('..\\graph_data\\coinbase_graph.pkl','wb') as file:
        pickle.dump(coinbase_graph,file, -1)
    with open('..\\graph_data\\normal_trans_graph.pkl','wb') as file:
        pickle.dump(normal_trans_graph, file, -1)
    # print(len(normal_trans_graph.keys()))
    # print(coinbase_graph)
def main():
    print_Menu()
    # 表示连续读取几个文件
    data_file_num = 1
    # 表示连读读取的文件计数
    data_file_count = 0
    sourceFilePath = 'D:\\data\\block\\'
    for data_file in os.listdir(sourceFilePath):
        data_file_count += 1
        sourceFile = sourceFilePath+data_file
        file_size = os.path.getsize(sourceFile)
        with open(sourceFile,'rb') as file:
            select = input('请输入要执行的操作号码\n')
            #select = '2'
            if select == '1':
                # block_no 表示读取第几个区块
                block_no = input('请输入要读取第几个区块（从 1 开始）\n')
                block_size,block = get_one_block(file, int(block_no))
                print_block_Info(block, block_no)
                block.print_normal_trans_Info
                file.seek(0, 0)
            elif select == '2':
                # 读取前10个区块,放在list中
                block_num = input('请输入要连续读取几个区块\n')
                # read_all_blocks = True 表示是否读取所有区块
                blocks = get_constant_block(file,file_size, int(block_num),method=2, read_all_blocks = False)
                # block_no = int(block_num)
                # block = blocks[block_no-1]
                # print_block_Info(block,block_no)
                save_trans_graph(blocks)
            else:
                pass
        if data_file_count == data_file_num:
            break
def read_graph():
    print('\n******************************')
    print('  有以下图数据')
    print('     1：coinbase_graph ；')
    print('     2：normal_trans_graph .')
    print('\n******************************')
    select_num = int(input('您要查看哪个图的数据？'))
    #select_num = 1
    if select_num == 1:
        with open('..\\graph_data\\coinbase_graph.pkl','rb') as pkl_file:
            coinbase_graph = pickle.load(pkl_file)
            print(coinbase_graph)
    elif select_num == 2:
        with open('..\\graph_data\\normal_trans_graph.pkl','rb') as pkl_file:
            normal_trans_graph = pickle.load(pkl_file)
            for key_ in normal_trans_graph.keys():
                print(key_,':',normal_trans_graph.get(key_))
if __name__ == '__main__':
    main()
    #read_graph()
