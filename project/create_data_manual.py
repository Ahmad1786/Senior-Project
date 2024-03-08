import json

# In Hindsight: these were just notes I was making trying to make sense of how best to create the data
# Decided to make some data manually to see some familiar names - rest will be done with faker

# define the model attributes
# user, server (house), participation (connection between user and server)
# Different Posts: chores (task), events, bill 
# Comments / Can also have Replies

# Simplifications to make my life easy
# For simplicity - Will ignore phone numbers and profile pictures / icons for now
# Will also ignore the due dates for things - may run another script to update the due dates by some fixed amount + now (now+10days)
# Will not do replies. Each comment will be a top level comment

# Some time fields are set to auto_now_add=True: all creation / date_joined dates # no need to worry about them

# Tricky thing will be creating participations 
# One trick - make all is_owner false and then make one true for each house - will just have to ignore the same date fallacy

# for manual data example (our 3 house) - just make owners now


Model_Types = {
    0: 'user',
    1: 'server',
    2: 'participation',
    3: 'task',
    4: 'event',
    5: 'bill',
    6: 'comment'
}

# Going to make some data manually that will be more relevant to us
first_names = ['Muhammad', 'Daniel', 'Luke', 'Mary', 'Tayyab', 'Doctor', 'Ridhaa']
last_names = ['Ahmad', 'Reger', 'Lachowicz', 'Monaco', 'Qaiser', 'Baliga', 'Rahman']

def create_email(f, l):
    return f.lower() + l.lower() + '@random.com'

# Two Houses # Lets say we "all live at rowan" and do rowan specific stuff
# And then Muhammad, Ridhaa, and Luke live together at Holly Point as well
# And then Daniel, Mary, and Tayyab live together at 220 Rowan Boulevard

# House names
Rowan = 'Rowan University Group'
Muhammad_House = 'Holly Point'
Tayyab_House = '220 Rowan Boulevard'

Houses = [Rowan, Muhammad_House, Tayyab_House]
owners = {
    Rowan: 'Doctor',
    Muhammad_House: 'Muhammad',
    Tayyab_House: 'Tayyab'
}

users = []
for f, l in zip(first_names, last_names):
    user = {
        'model': Model_Types[0],
        'first_name': f,
        'last_name': l,
        'email': create_email(f, l),
    }
    users.append(user)

houses = []
for house in Houses:
    house = {
        'model': Model_Types[1],
        'name': house
    }
    houses.append(house)

participations = []
for i, first in enumerate(first_names + ['Muhammad', 'Ridhaa', 'Luke'] + ['Daniel', 'Mary', 'Tayyab']):
    dict = {
        'model': Model_Types[2],
        'is_owner': False,
    }
    if i in range(7):
        dict['house'] = Rowan
        dict['user'] = first
        if first == owners[Rowan]:
            dict['is_owner'] = True
    elif i in range(7, 10):
        dict['house'] = Muhammad_House
        dict['user'] = first
        if first == owners[Muhammad_House]:
            dict['is_owner'] = True
    else:    
        dict['house'] = Tayyab_House
        dict['user'] = first
        if first == owners[Tayyab_House]:
            dict['is_owner'] = True

    participations.append(dict)  

# codes 0: Rowan, 1: Muhammad, 2: Tayyab house
codes = {
    0: Rowan,
    1: Muhammad_House,
    2: Tayyab_House
}

Chore_List = [('Fix the bookshelves', 0), ('Clean the whiteboards', 0)]
Chore_List += [('Clean the Kitchen', 1), ('Clean the Bathroom', 1), ('Vacuum the Living Room', 1), ('Take out the Trash', 1), ('Mop the Kitchen', 1)]
Chore_List += [('Put on the shower curtain', 2), ('Do the laundry', 2)]

Event_List = [('Leetcode workshop', 0)]
Event_List += [('Football with the boyz', 1)]
Event_List += [('Movie Night', 2), ('Study Session', 2)]

Bill_List = [('Rowan Laptop', 1000.00, 0), ('Rowan Fridge', 500.00, 0), ('Rowan TV', 300.00, 0), ('Rowan Couch', 400.00, 0), ('Rowan Table', 200.00, 0)]
Bill_List += [('Football', 20.00, 1), ('New TV Remote', 15.00, 1)]
Bill_List += [('Shower Curtain', 10.00, 2), ('New Shower Head', 20.00, 2), ('Toilet Paper', 5.00, 2)]

Chores, Events, Bills = [], [], []
for chore in Chore_List:
    dict = {
        'model': Model_Types[3],
        'name': chore[0],
        'house': codes[chore[1]],
        'description': f'Do you really need me to tell you? Its all in the title: {chore[0]} !!!',
        'creator': owners[codes[chore[1]]]
    }
    Chores.append(dict)

for event in Event_List:
    dict = {
        'model': Model_Types[4],
        'name': event[0],
        'house': codes[event[1]],
        'description': f'Come join us for {event[0]} at our place {codes[event[1]]}!!! Bring your friends too!',
        'creator': owners[codes[event[1]]]
    }
    Events.append(dict)

for bill in Bill_List:
    dict = {
        'model': Model_Types[5],
        'name': bill[0],
        'house': codes[bill[2]],
        'description': f"It's simple really - we gotta pay for {bill[0]} together!!!!",
        'cost': bill[1],
        'creator': owners[codes[bill[2]]],
        # Just make it owner for now
        'payers': [owners[codes[bill[2]]]]   
    }
    Bills.append(dict)

# create a comment for each post from the owner of that house
comments = []
for post in Chores + Events + Bills:
    house_owner = owners[post['house']]
    for user_house, user_name in owners.items():
        if user_name == house_owner:
            dict = {
                'model': Model_Types[6],
                'author': user_name,
                'post_name': post['name'],
                'text': f"I am the owner of {user_house} and I approve of this post!!"
            }
            comments.append(dict)
            break 

json_data = [users] + [houses] + [participations] + [Chores] + [Events] + [Bills] + [comments]
with open('manual_data.json', 'w') as f:
    json.dump(json_data, f, indent=2)