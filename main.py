from ivm import IVM
from nexposeLogs import LOG
import yaml
import csv

logFile = open("log.txt", "w")  # To add in our logs for checking results

#Load configuration from yaml file

with open('config.yaml', 'r') as file:
    ivmConfigDetails = yaml.safe_load(file)
    
file.close()

tagFile = ivmConfigDetails['tagFile']

# Define file for logging
fileObj = LOG(logFile)

#Send initial configuration to IVM object
ivmobj = IVM(ivmConfigDetails, fileObj)

# Adding all tags and their IDs from Nexpose console to dictionary
tags = ivmobj.getTags()

fileObj.writeLog("Tags added to dictionary\n" + str(tags))

# Read CSV file with tags and name

with open(tagFile, "r") as f:
    csvreader = csv.reader(f)

    for line in csvreader:
        ip = line[0]
        potentialNewTag = line[1]
        
        # At the same time, check if all tags are available on R7, if not - create them
        if tags.get(potentialNewTag) is None:
            
            fileObj.writeLog(potentialNewTag + " not in Rapid7")
            
            tid = str(ivmobj.createTag(potentialNewTag))
            tags[potentialNewTag] = tid #Add to dictionary for future checking
            fileObj.writeLog("New tag created " + potentialNewTag)
        else:
            tid = str(tags[potentialNewTag])
        
        fileObj.writeLog("Tag ID is " + tid)
            
        aid = str(ivmobj.getAssets(ip)) # Returning Asset ID of the required IP
        fileObj.writeLog("ID of IP " + ip + " is " + aid)
        
        #Add assets to the tag with https://help.rapid7.com/insightvm/en-us/api/index.html#operation/tagAsset
        url = "assets/" + aid + "/tags/" + tid
        
        # Start tagging on the console using PUT API
        fileObj.writeLog("API url generated: " + url)
        
        # Check if any returns errors and log them
        potentialError = ivmobj.startTagging(url)
        if potentialError:
            fileObj.writeLog(ip + "to be added to " + potentialNewTag + "ran into error " + potentialError)
        else:
            fileObj.writeLog(ip + " added to " + potentialNewTag)
            
fileObj.writeLog("Script complete, closing file")
f.close()
logFile.close()