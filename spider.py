import json
import requests
import os
download_list_file="download_list.sh"
asus_api_endpoint_products = "https://www.asus.com/support/api/product.asmx/GetPDLevel?website=global&type=2&typeid={}&productflag=1"
asus_api_endpoint_mainboards = "https://www.asus.com/support/api/product.asmx/GetPDBIOS?website=global&pdhashedid="
headers = {'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}
#"https://www.asus.com/support/api/product.asmx/GetPDLevel?website=global&type=1&typeid=1849&productflag=0"
# router_type_list="https://www.asus.com/support/api/product.asmx/GetPDLevel?website=global&type=1&typeid=1849&productflag=0"

# type_list_get=requests.get(router_type_list,headers=headers)
# json.loads(type_list_get.text)
type_list=['3158', '3004', '21981', '2850', '25266', '2773', '2696', '2619', '2542', '3081']
def download_firmware(url,path):
    down_api=requests.get(url,headers=headers)
    back_info=json.loads(str(down_api.text))
    print(back_info)
    if back_info["Status"]=="SUCCESS":
        obj=back_info["Result"]["Obj"][0]
        if obj["Name"]=="Firmware" :
            des=[]
            desc_file_path=path+"/desription.json"
            for i in obj["Files"]:
                desription={"title":i["Title"],"version":i["Version"],"desc":i["Description"],"release_date":i["ReleaseDate"]}
                des.append(desription)
                filename=i["DownloadUrl"]["Global"].split("/")[-1]
                firmware_path=path+"/"+filename
                with open(download_list_file,"a") as f:
                    wget_command="wget -c --verbose"+' "'+i["DownloadUrl"]["Global"]+'" '+'-O "'+firmware_path+'"\n'
                    f.write(wget_command)
            with open(desc_file_path,"w") as f:
                f.write(str(des))
                # print(i["DownloadUrl"]["Global"])
# download_firmware("https://www.asus.com/support/api/product.asmx/GetPDBIOS?website=global&pdhashedid=pezdd5ujcut73gz5","123")

def requestMainboard(hash, name):  
    name=name.replace('/', "-").replace(" ","_")
    folder="download/"+name
    product_api=asus_api_endpoint_mainboards+hash
    if not os.path.exists(folder):
        os.makedirs(folder)
    download_firmware(asus_api_endpoint_mainboards+hash,folder)

def requestproductlist(type_id):
    asus_products_list = "https://www.asus.com/support/api/product.asmx/GetPDLevel?website=global&type=2&typeid="+type_id+"&productflag=1"
    res=requests.get(asus_products_list,headers=headers)
    data=json.loads(res.text)
    for i in data['Result']["Product"]:
        requestMainboard(i["PDHashedId"],i["PDName"])





def main():

    with open(download_list_file,"w") as f:
        f.write("#!/bin/bash\n")
    for i in type_list:
        requestproductlist(i)
    
main()
# # data=json.loads(str(response.text))
# f=open("./products.json",'r')
# data=f.read()
# f.close()
# product_info=json.loads(data)
# print(len(product_info['Result']["Product"]))
# for i in product_info['Result']["Product"]:
#     # print(i["PDId"])
#     print(i['PDName'].replace('/', "-").replace(" ","_"))
# # with open("./products.json",'r') as f:
# #     f.write(str(response.text))
# # print(data)


    


