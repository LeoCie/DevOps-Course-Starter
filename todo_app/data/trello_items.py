import requests
import os
import urllib.parse
from todo_app.models.Item import Item

trello_base_url = 'https://api.trello.com/1'

def get_items():
    board, authParams = getBoardAndAuthParams()
    listsWithCards = makeGetRequest(trello_base_url + f'/boards/{board}/lists{authParams}&cards=open')
    todoCards = [list for list in listsWithCards if list['name'] == 'To Do'][0]['cards']
    doingCards = [list for list in listsWithCards if list['name'] == 'Doing'][0]['cards']
    doneCards = [list for list in listsWithCards if list['name'] == 'Done'][0]['cards']
    return parseItems(todoCards, 'Not Started') + parseItems(doingCards, 'In Progress') + parseItems(doneCards, 'Done')

def change_item_status(cardId, status):
    board, authParams = getBoardAndAuthParams()
    lists = makeGetRequest(trello_base_url + f'/boards/{board}/lists{authParams}')
    listId = [list for list in lists if list['name'] == status][0]['id']
    return requests.put(trello_base_url + f'/cards/{cardId}{authParams}&idList={listId}')

def delete_item(cardId):
    board, authParams = getBoardAndAuthParams()
    return requests.delete(trello_base_url + f'/cards/{cardId}{authParams}')

def create_item(title):
    board, authParams = getBoardAndAuthParams()
    title = urllib.parse.quote(title.replace('&',' '))
    lists = makeGetRequest(trello_base_url + f'/boards/{board}/lists{authParams}')
    todoListId = [list for list in lists if list['name'] == 'To Do'][0]['id']
    requests.post(trello_base_url + f'/cards{authParams}&name={title}&idList={todoListId}')

def parseItems(listOfCards, status):
    returnList = []
    for card in listOfCards:
        returnList.append(Item.from_trello_card(card, status))
    return returnList

def makeGetRequest(url):
    request = requests.get(url)
    return request.json()

def getBoardAndAuthParams():
    board = os.getenv('TRELLO_BOARD_ID')
    token = os.getenv('TRELLO_TOKEN')
    key = os.getenv('TRELLO_KEY')
    authParams = f'?token={token}&key={key}'
    return board, authParams