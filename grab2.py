# AdsMiner:Grabber2.0 (Grab1 + tasks support)
# Reads a task(list of urls) from tasksdir
# Moves task file to proc dir
# Grabes urls, parses ad blocks
# Saves results to logs dir, file name same as task file
# Moves task file to lists dir

import configparser
import hashlib
import os.path
import adsminer
import codecs

# Read config
config = configparser.ConfigParser()
try:
    config.read('miner.conf')
except:
    print('Cant read config file')
    assert False

# Init
urlsdir = 'lists'
procdir = 'proc'
logsdir = 'logs'
tasksdir = 'tasks'
jsondir = 'json'
if not os.path.exists(logsdir):
    os.makedirs(logsdir)
if not os.path.exists(urlsdir):
    os.makedirs(urlsdir)
if not os.path.exists(procdir):
    os.makedirs(procdir)
if not os.path.exists(jsondir):
    os.makedirs(jsondir)

datadir = config['GRABBER']['DataDir']
if not os.path.exists(datadir):
    os.makedirs(datadir)
run = config['GRABBER']['Run']
run1 = config['GRABBER']['Run1']
block_complexity = int(config['GRABBER']['BlockComplexity'])
maxBlockSize = int(config['GRABBER']['MaxBlockSize'])
minBlockSize = int(config['GRABBER']['MinBlockSize'])
maxLinks = int(config['GRABBER']['MaxLinks'])
Timeout = int(config['GRABBER']['Timeout'])

##isLogFile = adsminer.initLog(log_file,'Grabber started\n')

# Looking for tasks
proc_path = ''
try:
    for file in os.listdir(tasksdir):
        if file.endswith('.txt'):
            print('Reading tasks file: ',file)
            tasks_path = os.path.join(tasksdir, file)
            proc_path = os.path.join(procdir, file)
            urls_path = os.path.join(urlsdir, file)
            ##log_file = os.path.join(logsdir, file)
            jsonfile = os.path.join(jsondir, file)
            if os.path.isfile(proc_path) == True:
                os.remove(proc_path)
            os.rename(tasks_path, proc_path) # Moving the task to proc dir
            break
except:
    print('No tasks')
    assert False

if proc_path=='':
    print('No tasks')
    assert False
else:
    urls = adsminer.file2list(proc_path)
    if len(urls)==0:
        print('No urls found')
        assert False

total_blocks = 0
to_json = []
target_urls = []

for url in urls:
    try:
        url = adsminer.clearUrl(url)
    except:
        continue
    url_id = hashlib.md5(url.encode('utf-8')).hexdigest()    
    path = os.path.join(datadir, url_id + '.html')

    print(url, path)
    text = adsminer.url2html(run, url, path, Timeout)
    
    # TODO add tidy html?
    ads = adsminer.parseBlocks(text, url, block_complexity, minBlockSize, maxBlockSize, maxLinks)
    try:
        ads_num = len(ads.keys())
    except:
        del(ads)
        continue
    total_blocks +=ads_num
        
    if ads_num>0:
        for id in ads.keys():          
            json_block = adsminer.Block2List(url, id, ads[id])
            for target_url in json_block[2]:
                target_urls.append(target_url)

            to_json.append(json_block)
                

    del(ads)
    #break

f = codecs.open(os.path.join(tasksdir, 'targets.wget'), 'w', encoding='utf-8')
target_urls = adsminer.uniqList(target_urls)
for target_url in target_urls:
    f.write(target_url+'\n')
f.close()

# Writing json data to file
adsminer.writeJson(jsonfile, to_json)
    
# Moving finished list to lists dir    
if os.path.isfile(urls_path) == True:
    os.remove(urls_path)
os.rename(proc_path,urls_path) 
##adsminer.writeLog(log_file, 'Total blocks found: '+str(total_blocks)+'\n', isLogFile)
##adsminer.writeLog(log_file, 'Done\n', isLogFile)
