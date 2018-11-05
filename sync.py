#!/usr/bin/env python

import requests
import json

masterEnv = "https://example.live.dynatrace.com/api/config/v1/"
masterEnvToken = "23413441234"

syncEnvList = [
    {"URL" :"https://example.live.dynatrace.com/api/config/v1/","token":"23413441234"},
    {"URL" :"https://example.dynatrace-managed.com/e/d3cc8e25-2968-45b4-896f-754f3e26b4a8/api/config/v1/","token":"23413441234"},
    {"URL" :"https://example.dynatrace-managed.com/e/2318471f-e9f3-4d14-8c61-6cf4e5bd48f6/api/config/v1/","token":"23413441234"},
    {"URL" :"https://example.dynatrace-managed.com/e/293d4569-1cd7-4875-b9a1-3b380d2dc41e/api/config/v1/","token":"23413441234"},
]


requestAttributesEnabled = True   
autoTaggingRulesEnabled = False
managementZonesRulesEnabled = False

addNotExisting = True
updateExisting = False



def compare(listA,listB):
    diff = []
    for item in listA:
        if not any(item['name'].lower() == item2['name'].lower() for item2 in listB):
           diff.append(item)
    return diff

def makeRequestWithoutPayload(fullURL,token,typeOfRequest):
    querystring = {"includeProcessGroupReferences":"false","Api-Token": token}

    headers = {
        'accept': "application/json; charset=utf-8",
        'Cache-Control': "no-cache"
    }
    response = requests.request(typeOfRequest, fullURL, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.text
    else:
        print("Cannot connect to tenant")
        exit()
def makeRequestWithPayload(fullURL,token,typeOfRequest, payload):
    querystring = {"Api-Token":token }
    headers = {
        'accept': "application/json; charset=utf-8",
        'Content-Type': "application/json; charset=utf-8",
        'Cache-Control': "no-cache",
    }
    response = requests.request(typeOfRequest, fullURL, data=json.dumps(payload), headers=headers, params=querystring)
    print(response)
    print(response.text)
    if response.status_code == 200:
        return response.text
    else:
        return False

def getAllCongRules(env,token,endPoint):
    allRules = makeRequestWithoutPayload(env+endPoint,token,"GET")
    return json.loads(allRules)

def getDetails(env,token,endPoint,item):
    response=makeRequestWithoutPayload(env+ endPoint+"/"+item['id'],token,"GET")
    return json.loads(response)

def createItem(env,token,endPoint,item):
    makeRequestWithPayload(env+endPoint,token,"POST",item)

def updateItem(env,token,endPoint,item):
    makeRequestWithPayload(env+endPoint+"/"+item['id'],token,"PUT",item)

def syncRules(endPoint, add, update,syncEnv,syncEnvToken):
    allMasterConfig = getAllCongRules(masterEnv,masterEnvToken,endPoint)['values']
    allSync = getAllCongRules(syncEnv,syncEnvToken,endPoint)['values']
    if add:
        diff = compare(allMasterConfig,allSync)
        for item in diff:
            details = getDetails(masterEnv,masterEnvToken,endPoint,item)
            details['id'] = None
            createItem(syncEnv,syncEnvToken, endPoint,details)
    if update:
        for item in allMasterConfig:
           details = getDetails(masterEnv,masterEnvToken,endPoint,item)
           match = next((x for x in allSync if x['name'].lower()==item['name'].lower()),None)
           if not match == None:
            details['id'] = match['id']
            updateItem(syncEnv,syncEnvToken, endPoint,details)


def syncEnviroments():
    for item in syncEnvList:
        print(item["URL"])
        if requestAttributesEnabled:
            syncRules("requestAttributes",addNotExisting,updateExisting,item["URL"],item["token"])
        if autoTaggingRulesEnabled:
            syncRules("autoTags",addNotExisting,updateExisting,item["URL"],item["token"])
        if managementZonesRulesEnabled:
            syncRules("managementZones",addNotExisting,updateExisting,item["URL"],item["token"])

syncEnviroments()
