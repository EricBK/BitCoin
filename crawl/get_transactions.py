import urllib.request
import json

def get_transaction_details(url,trans_only = True):

    response = urllib.request.urlopen(url)
    html = response.read()
    # html = json.load()
    html = json.loads(str(html)[2:-1])
    print(html)
    data = {}

    for key in sorted(html.keys()):
        if key == 'blockhash':
            data[key] = html[key]
        elif key == 'txid':
            data[key] = html[key]
        elif key == 'vin':
            data[key] = html[key]
            trans_in_addr = []
            trans_in_value = []
            for sub_trans_in in html[key]:
                for sub_key in sub_trans_in.keys():
                    if sub_key == 'value':
                        trans_in_value.append(float(sub_trans_in[sub_key]))
                    elif sub_key == 'addr':
                        trans_in_addr.append(sub_trans_in[sub_key])
            data['trans_in_addr'] = trans_in_addr
            data['trans_in_value'] = trans_in_value
        elif key == 'vout':
            data[key] = html[key]
            trans_out_addr = []
            trans_out_value = []
            for sub_trans_in in html[key]:
                for sub_key in sub_trans_in.keys():
                    if sub_key == 'value':
                        trans_out_value.append(float(sub_trans_in[sub_key]))
                    elif sub_key == 'scriptPubKey':
                        trans_out_addr.append(sub_trans_in[sub_key]['addresses'][0])
            data['trans_out_addr'] = trans_out_addr
            data['trans_out_value'] = trans_out_value
    if trans_only:
        vin = {}
        for vin_no in range(len(trans_in_value)):
            vin.setdefault(trans_in_addr[vin_no])
    else:
        return data
    '''
    for key in html.keys():
        print('key: ',key)
        print('   value:',html[key])
        if key == 'vin' or key == 'vout':
            Curvalue = html[key][0]
            for sub_key in Curvalue.keys():
                print('     sub_key:',sub_key)
                print('         sub_value',Curvalue[sub_key])
#    print(str(html)[2:-1])
    '''
def print_data_Info(data):
    for key in sorted(data.keys()):
        print('key:',key)
        print('     value:',len(data[key]),data[key])
if __name__ == '__main__':
    #main1()
    url_base = 'https://blockexplorer.com/api/tx/'
    #    trans_hash = '21fb5d5549f70de759b352c8c4deb9e7afb0b41b2e54d11895362ee72e5d690a'
    trans_hash = 'eca472e6d9238d459cf779527898b5c2de5407ad75ddc2f0a7148f89029b4690'
    url = url_base + trans_hash
    data = get_transaction_details(url,trans_only = True) #trans_only = True 表示只获取交易数据
    print_data_Info(data)
