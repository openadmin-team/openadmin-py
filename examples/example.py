spec = {
    'version': '1.0.0',
    'name': "API Admin",
    'sections': [
        {
            'name': 'Users',
            'pages': [
                {
                    'name': 'User managment',
                    'description': 'CRUD for users',
                    'components': [
                        {
                            'type': 'stat',
                            'name': 'Active users',
                            'description': 'Active users',
                            'url': 'http://...',
                            'method': 'GET',
                        },
                        {
                            'type': 'table',
                            'name': 'Users',
                            'descritpion': 'Users table',
                            'url': 'http://...',
                            'method': 'GET',
                            'styles': {
                                'username': {
                                    'style': 'badge',
                                    'color': 'green',
                                },
                                'email': {
                                    'style': 'row',
                                },
                                'avatar': {
                                    'style': 'avatar',
                                }
                            },
                            'actions': [
                                {
                                    'name': "Ban",
                                    'method': 'post',
                                    'url': 'http://...',
                                    'query': {
                                        'name': 'id',
                                        'ref': 'id',
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}