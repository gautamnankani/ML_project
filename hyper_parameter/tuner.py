import yaml
import re
class CNN():
    def __init__(self,dir_path,counter,config):
        with open(dir_path+'/'+'new_file.py','w') as new_file:
            with open(dir_path+'/'+'model_train.py','r') as old_file:
                for key in config['HyperParameter'].keys():
                    print("key:",key)
                    change_this_line=""
                    for line in old_file:
                        if 'S'+key not in line:
                            new_file.writelines(line)
                            continue
                        else:
                            new_file.writelines('\n')
                            break
                    for line in old_file:
                        if 'E'+key not in line:
                            print(line)
                            change_this_line+=line
                        else:
                            break
                    for arg in config['HyperParameter'][key]: 
                        pattern=r'{}[ ]*=.*,'.format(arg)
                        replace_value=config['HyperParameter'][key][arg][counter]
                        if type(replace_value) is str:
                            replace_value="'"+replace_value+"'"
                        change_this_line=re.sub(pattern,"{}= {},".format(arg,replace_value),change_this_line)
                    new_file.writelines(change_this_line)
                else:
                    new_file.write(old_file.read())
                    if config['Kind']=="CNN":
                        hyp_para_parsing=""
                        for param in config['HyperParameter']:
                            hyp_para_parsing=hyp_para_parsing+param+":- "
                            for sub_variable in config['HyperParameter'][param]:
                                hyp_para_parsing+=sub_variable+": "+str(config['HyperParameter'][param][sub_variable][counter])+" , "
                            hyp_para_parsing+='  |  '
                        new_file.writelines("""
import csv
with open('stats.csv','a') as stats_file:
    additional_data= {}.history
    additional_data['HyperParameter']="{}"
    additional_data['Serial_No']={}
    writer=csv.DictWriter(stats_file,fieldnames=[x for x in additional_data])
    if additional_data['Serial_No']==0:
        writer.writeheader()
    writer.writerow(additional_data)
""".format(config['ModelFitVariable'],hyp_para_parsing,counter))
                old_file.close()
            new_file.close()


import os
yaml_file=open('config.yml')
config=yaml.load(yaml_file, Loader= yaml.FullLoader)
for counter in range(config['Counter']):
    CNN('../',counter,config)
    os.system("python3 ../new_file.py")