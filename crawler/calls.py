import requests
import os
import json
from dotenv import load_dotenv

# loading environment variables from .env file
load_dotenv()

# constructing the API call
courseLinkAPI = "https://canvas.brown.edu/api/v1/courses"
queryParams = "?enrollment_state=active"
headers = {
    'Authorization': 'Bearer ' + os.getenv('API_AUTH_TOKEN_NOV22'),
}

coursesResponseList = requests.get(courseLinkAPI+queryParams, headers=headers)

for course in coursesResponseList.json():
    print(course["name"])


courseNametoId = {}
courseToFiles = {}

# function: 
#   input: <object> 
#   output: dict
#   description: given a course object, this function will return a dictionary with the key
#   as the courseName and the value as a dictionary of the type (fileType:list(fileDownloadLink)). 
def getCourseFiles(course):

    fileMap = {}
    folderRequestAPI = courseLinkAPI + "/" + str(courseNametoId[course["name"]]) + "/folders"

    while True:
        # get list of folders (page limit: 10)
        folderResponseList = requests.get(folderRequestAPI, headers=headers)
        
        # get file list in each folder
        for folder in folderResponseList.json():
            fileRequestAPI = "https://canvas.brown.edu/api/v1/folders/" + str(folder["id"]) + "/files"
            while True:
                fileResponseList = requests.get(fileRequestAPI, headers=headers)
                for file in fileResponseList.json():
                    if file != 'status' and file != 'errors':
                        if file['content-type'] in fileMap:
                            fileMap[file['content-type']].append(file['url'])
                        else:
                            fileMap[file['content-type']] = [file['url']]

                if 'next' not in fileResponseList.links:
                    break
                else:        
                    fileRequestAPI = fileResponseList.links['next']['url']
            # print("--------END---------")
        
        if 'next' not in folderResponseList.links:
            break
        else:
            folderRequestAPI = folderResponseList.links['next']['url']
    return fileMap

courseFileMap = {}
for course in coursesResponseList.json():
    courseNametoId[course["name"]] = course["id"]
    courseFileMap[course["name"]] = getCourseFiles(course)

    zeroFlag = True
    print("File summary for " + course["name"])
    for key in courseFileMap[course["name"]].keys():
        print("Number of " + key + " files found: " + str(len(courseFileMap[course["name"]][key])))
        zeroFlag = False
    if zeroFlag:
        print("No files found")

# test = courseFileMap["ASYR1600 Fall23 S01 Astronomy Before the Telescope"]["application/pdf"][0]
# print(test)
# r = requests.get(test, allow_redirects=True)
# open("download.pdf", "wb").write(r.content)
