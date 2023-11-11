import requests


# response = requests.post('http://127.0.0.1:5000/adv', 
#                          json={'header': 'header_2', 
#                                'description': 'descr_2', 
#                                'owner': 'owner_2'},
#                          headers={'Authorization': 'some_token'})

response = requests.get('http://127.0.0.1:5000/adv/1', )

# response = requests.delete('http://127.0.0.1:5000/adv/1', )


print(response.status_code)
print(response.text)