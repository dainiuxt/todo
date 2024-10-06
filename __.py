from alembic import op
from datetime import date

users_table = op.tables['users'] 
tasks_table = op.tables['tasks']

op.bulk_insert(
    users_table,
    [
        {'id':1,
        'email':'john@smith.com',
        'password':'secret',
        'name':'John Smith'},
        {'id':2,
        'email':'ed@williams.com',
        'password':'secret2',
        'name':'Ed Williams'},
        {'id':3,
        'email':'jane@dow.com',
        'password':'secret5',
        'name':'Jane Dow'},
    ],
    tasks_table,
    [
        {'id':1, 'user_id':1, 'created':date(2007, 5, 27),
                'content':'content 1', 'completed':False},
        {'id':2, 'user_id':1, 'created':date(2007, 5, 27),
                'content':'content 2', 'completed':False},
        {'id':3, 'user_id':2, 'created':date(2007, 5, 28),
                'content':'content 3', 'completed':True},
        {'id':4, 'user_id':3, 'created':date(2007, 5, 29),
                'content':'content 4', 'completed':False},
    ]

)