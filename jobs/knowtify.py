#!/usr/bin/env python
import json
import os
import random
from datetime import datetime, timedelta

import psycopg2
import psycopg2.extras
import requests


def get_connection():
    """
    Get a connection, if a connect cannot be made an exception will be raised here.

    """
    conn_string = "host='{0}' port='{1}' dbname='sitterfied' user='{2}' password='{3}'".format(
        env.get('DOTCLOUD_DATA_SQL_HOST'),
        env.get('DOTCLOUD_DATA_SQL_PORT'),
        env.get('DOTCLOUD_DATA_SQL_LOGIN'),
        env.get('DOTCLOUD_DATA_SQL_PASSWORD')
    )

    # print the connection string we will use to connect
    #print("Connecting to database\n	->%s" % (conn_string))

    # get a connection, if a connection cannot be made an exception will be raised here
    return psycopg2.connect(conn_string)


def get_friends(parent_id):
    """
    Get all friends associated with a parent.

    """
    query = """
SELECT
    f.id as friend_id,
    f.first_name || ' ' || f.last_name as friend_name,
    f.email as friend_email,
    f.avatar as friend_avatar
FROM public.app_parent as p
LEFT OUTER JOIN public.app_user up on up.id = p.user_ptr_id
LEFT OUTER JOIN public.app_user_friends uf on uf.from_user_id = up.id
LEFT OUTER JOIN public.app_user f on f.id = uf.to_user_id
WHERE up.id = {0}
GROUP BY up.id, f.id, f.first_name, f.last_name, f.email, f.avatar
ORDER BY up.id
    """.format(parent_id)

    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(query)

    return [{
        'id': record['friend_id'],
        'name': record['friend_name'],
        'email': record['friend_email'],
        'avatar': record['friend_avatar'],
    } for record in cursor.fetchall()]


def get_sitter_team(parent_id, added_since=datetime(1970, 1, 1)):
    """
    Get all sitters on a parent's sitter team that have been added to the team
    in the interval specified by the added_since parameter (typically 1 week).

    """
    query = """
SELECT
    us.id as sitter_id,
    us.first_name || ' ' || us.last_name as sitter_name,
    us.email as sitter_email,
    us.avatar as sitter_avatar,
    t.created as sitter_added
FROM public.app_parent as p
LEFT OUTER JOIN public.app_user up on up.id = p.user_ptr_id
LEFT OUTER JOIN public.app_parent_sitter_teams t on up.id = t.parent_id
LEFT OUTER JOIN public.app_user us on us.id = t.sitter_id
WHERE up.id = {0} AND t.created >= '{1}'
GROUP BY us.id, up.id, us.first_name, us.last_name, us.email, us.avatar, t.created
ORDER BY up.id
    """.format(parent_id, added_since.strftime('%Y-%m-%d %H:%M:%S'))

    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(query)
    records = cursor.fetchall()

    sitters = []
    for record in records:
        if record['sitter_id']:
            sitter = {
                'id': record['sitter_id'],
                'name': record['sitter_name'],
                'email': record['sitter_email'],
                'avatar': record['sitter_avatar'],
                'added': record['sitter_added'].isoformat(),
            }
            sitters.append(sitter)

    return sitters


def get_parents():
    """
    Retrieve all parents

    """
    query = """
SELECT
    up.id as parent_id,
    up.first_name as first_name,
    up.last_name as last_name,
    up.email as email
FROM public.app_parent as p
LEFT OUTER JOIN public.app_user up on up.id = p.user_ptr_id
GROUP BY up.id, up.first_name, up.last_name, up.email
ORDER BY up.id"""

    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(query)
    return cursor.fetchall()


def get_sitters(added_since):
    """
    Retrieve sitters that have been added to a parent's sitter team since the
    value of the added_since parameter (typically 1 week).

    """
    query = """
SELECT
    us.id as sitter_id,
    us.first_name as first_name,
    us.last_name as last_name,
    us.email as email
FROM public.app_sitter as s
LEFT OUTER JOIN public.app_user us ON us.id = s.user_ptr_id
LEFT OUTER JOIN public.app_parent_sitter_teams pst ON pst.sitter_id = s.user_ptr_id
WHERE pst.created > '{}'
GROUP BY pst.id, us.id, us.first_name, us.last_name, us.email
ORDER BY us.id
    """.format(added_since.strftime('%Y-%m-%d %H:%M:%S'))

    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(query)
    return cursor.fetchall()


def get_sitter_sitter_team_activity(sitter_id, added_since):
    """
    Retrieve the parents that have added this sitter in the interval specified
    by the added_since parameter (typically 1 week).

    """
    query = """
SELECT
    up.id as parent_id,
    up.first_name || ' ' || up.last_name as parent_name,
    up.email as parent_email,
    up.avatar as parent_avatar
FROM public.app_parent as p
LEFT OUTER JOIN public.app_user up on up.id = p.user_ptr_id
LEFT OUTER JOIN public.app_parent_sitter_teams t on up.id = t.parent_id
WHERE t.sitter_id = {} AND t.created > '{}'
GROUP BY up.id, up.first_name, up.last_name, up.email, up.avatar
ORDER BY up.id
    """.format(sitter_id, added_since.strftime('%Y-%m-%d %H:%M:%S'))

    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(query)

    return [{
        'id': record['parent_id'],
        'name': record['parent_name'],
        'email': record['parent_email'],
        'avatar': record['parent_avatar'],
    } for record in cursor.fetchall()]


def get_suggested_sitters(parent_id, count=3):
    """
    Get a random selection of suggested sitters for a parent.

    This is determined by retrieving all second-level (sitters on friend's
    sitter teams), shuffling the returned results, and taking the number
    specified in the count parameter.

    """
    query = """
SELECT
    pst.sitter_id as sitter_id,
    u.avatar as sitter_avatar,
    u.email as sitter_email,
    u.first_name || ' ' || u.last_name as sitter_name
FROM
    app_parent_sitter_teams pst
INNER JOIN
    app_user u ON u.id = pst.sitter_id
WHERE
    pst.parent_id IN (SELECT uf.to_user_id FROM app_user_friends uf WHERE uf.from_user_id = {})
    AND
    pst.sitter_id NOT IN (SELECT pst.sitter_id FROM app_parent_sitter_teams pst WHERE pst.parent_id = {})
GROUP BY
    pst.sitter_id, u.avatar, u.email, u.first_name, u.last_name""".format(parent_id, parent_id)

    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(query)
    records = cursor.fetchall()
    random.shuffle(records)
    records = records[:3]

    return [{
        'id': record['sitter_id'],
        'name': record['sitter_name'],
        'email': record['sitter_email'],
        'avatar': record['sitter_avatar'],
    } for record in records]


def main():
    data = {'contacts': []}
    added_since = datetime.now() - timedelta(days=7)

    for record in get_parents():
        parent_id = record['parent_id']

        parent = {}
        parent['name'] = record['first_name'].strip() + " " + record['last_name'].strip()
        parent['email'] = record['email'].strip()
        parent['data'] = {
            'id': parent_id,
            'first_name': record['first_name'].strip(),
            'last_name': record['last_name'].strip(),
            'type': 'parent',
        }

        friends = get_friends(parent_id)
        parent['data']['friends'] = friends
        parent['data']['num_friends'] = len(friends)

        sitters = get_sitter_team(parent_id)
        sitter_team_size = len(sitters)
        parent['data']['sitters'] = sitters
        parent['data']['sitter_team_size'] = sitter_team_size

        new_sitters = get_sitter_team(parent_id, added_since)
        num_sitters_added = len(new_sitters)
        parent['data']['new_sitters'] = new_sitters
        parent['data']['num_sitters_added'] = num_sitters_added

        if num_sitters_added > 0 or sitter_team_size == 0:
            suggested_sitters = get_suggested_sitters(parent_id, 3)
            parent['data']['suggested_sitters'] = suggested_sitters
            parent['data']['num_suggested_sitters'] = len(suggested_sitters)

        data['contacts'].append(parent)

    for record in get_sitters(added_since):
        sitter_id = record['sitter_id']

        sitter = {}
        sitter['name'] = '{} {}'.format(record['first_name'].strip(), record['last_name'].strip())
        sitter['email'] = record['email'].strip()
        sitter['data'] = {
            'id': sitter_id,
            'first_name': record['first_name'].strip(),
            'last_name': record['last_name'].strip(),
            'type': 'sitter',
        }

        new_parents = get_sitter_sitter_team_activity(sitter_id, added_since)
        sitter['data']['new_parents'] = new_parents
        sitter['data']['num_new_parents'] = len(new_parents)

        data['contacts'].append(sitter)

    print('Request body\n	->%s' % (json.dumps(data)))

    api_token = env.get('KNOWTIFY_API_TOKEN')
    if api_token:
        try:
            r = requests.post(
                'http://www.knowtify.io/api/v1/contacts/upsert',
                data=json.dumps(data),
                headers={'Authorization': 'Token token="' + api_token + '"'}
            )
            print('API response\n      ->%s' % (r.content))
        except Exception as e:
            print('API error\n	->%s' % (e.message))
    else:
        print('An error occurred\n       ->The Knowtify API token is not set. Please set the KNOWTIFY_API_TOKEN environment variable.')


try:
    with open('/home/dotcloud/environment.json') as f:
        env = json.load(f)
except:
    # This is for testing purposes and will load variables from the
    # local environment if possible.
    env = {}
    env['DOTCLOUD_DATA_SQL_HOST'] = os.environ.get('DOTCLOUD_DATA_SQL_HOST')
    env['DOTCLOUD_DATA_SQL_PORT'] = os.environ.get('DOTCLOUD_DATA_SQL_PORT')
    env['DOTCLOUD_DATA_SQL_LOGIN'] = os.environ.get('DOTCLOUD_DATA_SQL_LOGIN')
    env['DOTCLOUD_DATA_SQL_PASSWORD'] = os.environ.get('DOTCLOUD_DATA_SQL_PASSWORD')
    env['KNOWTIFY_API_TOKEN'] = os.environ.get('KNOWTIFY_API_TOKEN')


conn = get_connection()


if __name__ == "__main__":
    main()
