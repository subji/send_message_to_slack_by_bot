import json
import pandas
import requests

# Get slack bot token
def getBotConfiguration():
  token_path = './bot_config.json'

  with open(token_path, 'r') as json_item:
    result = json.load(json_item)
  
  return result

def getChannelInfo(token, channel_name):
  CHANNEL_INFO_URL = 'https://slack.com/api/conversations.list'

  params = {
    'Content-Type': 'application/x-www-form-urlencoded', 
    'token': token
  }

  response = requests.get(CHANNEL_INFO_URL, params = params)

  channel_list = pandas.json_normalize(response.json()['channels'])
  channel_id = list((channel_list.loc[channel_list['name'] == channel_name]).get('id'))[0]

  return channel_id

def writeChatMessage(token, channel_id, message):
  data = {
    'Content-Type': 'application/x-www-form-urlencoded', 
    'token': token, 
    'channel': channel_id, 
    'text': message, 
    'reply_broadcast': 'True', 
  }

  WRITE_CHAT_URL = 'https://slack.com/api/chat.postMessage'

  response = requests.post(WRITE_CHAT_URL, data = data)

if __name__ == "__main__":
  bot_config = getBotConfiguration()
  token = bot_config['bot_token']
  channel_name = bot_config['channel_name']
  channel_id = getChannelInfo(token, channel_name)

  writeChatMessage(token, channel_id, 'Test')