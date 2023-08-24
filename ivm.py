import requests
import json
import sys

class IVM:
    def __init__(self, config, fileObject):
        self.connection = config["mainUrl"] + "/api/3/"
        self.headers = {
            'Authorization': (config["authHash"]),
            'Content-Type': 'application/json'
            }
        self.fileObject = fileObject
        
    def getTags(self):
        tags = {}
        response = requests.get(
            self.connection + "tags/?size=500",
            verify=False,
            headers = self.headers
            )
        
        IVM.checkError(self, response)
                
        details = response.json()["resources"]
        for tagDetails in details:
            name = tagDetails["name"]
            tags[name] = tagDetails["id"]
        return tags
    
    def createTag(self, tagName):
        response = requests.post(
            self.connection + "tags",
            verify=False,
            headers = self.headers,
            data=json.dumps(
                {
                    "name": tagName,
                    "type": "owner",
                }
            ),
        )
        
        IVM.checkError(self, response)
        return response.json()["id"]
    
    def getAssets(self, ip):

        response = requests.post(
            self.connection + "assets/search",
            verify=False,
            headers = self.headers,
            data=json.dumps(
                {
                    "filters": [{"field": "ip-address", "operator": "is", "value": ip}],
                    "match": "any",
                }
            ),
        )
        IVM.checkError(self, response)
        details = response.json()["resources"]
        return details[0]["id"]
        
    def startTagging(self,url):
        #If asset-tag already exists, update them
        response = requests.put(
            self.connection + url,
            verify=False,
            headers = self.headers
        )
        # Dont exit code in case of error, move to next and log it
        if response.status_code != 200:
            return response.text
        
    def checkError(self, response):
        if response.status_code != 200:
            self.fileObject.writeLog("Exiting " + response.text)
            sys.exit()
        