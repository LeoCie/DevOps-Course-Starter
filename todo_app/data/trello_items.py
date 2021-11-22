import requests
import os

trello_base_url = 'https://api.trello.com/1'
board = os.getenv('TRELLO_BOARD_ID')
token = os.getenv('TRELLO_TOKEN')
key = os.getenv('TRELLO_KEY')
authParams = f'?token={token}&key={key}'

def get_items():
    listsWithCards = makeGetRequest(trello_base_url + f'/boards/{board}/lists{authParams}&cards=open')
    todoCards = [list for list in listsWithCards if list['name'] == 'To Do'][0]['cards']
    doingCards = [list for list in listsWithCards if list['name'] == 'Doing'][0]['cards']
    doneCards = [list for list in listsWithCards if list['name'] == 'Done'][0]['cards']

    return parseItems(todoCards, 'Not Started') + parseItems(doingCards, 'In Progress') + parseItems(doneCards, 'Done')

def mark_as_complete(cardId):
    lists = makeGetRequest(trello_base_url + f'/boards/{board}/lists{authParams}')
    doneListId = [list for list in lists if list['name'] == 'Done'][0]['id']
    print(doneListId)
    return makePutRequest(trello_base_url + f'/cards/{cardId}{authParams}&idList={doneListId}')

def parseItems(listOfCards, status):
    returnList = []
    for card in listOfCards:
            returnList.append(Item(card['id'], card['name'], status))
    return returnList

def makeGetRequest(url):
    request = requests.get(url)
    return request.json()

def makePutRequest(url):
    request = requests.put(url)
    return request.status_code == 200

class Item:
    def __init__(self, id, title, status):
        self.title = title
        self.status = status
        self.id = id