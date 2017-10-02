from open_budget_search_api.elastic import merge_highlight_into_source

def test_highlight_merge():

    source = {
        'a': 'a simple string',
        'ax': 'an unrelated string',
        'ab': True,
        'ai': 5,
        'b': {
            'prop': 'a simple internal property',
            'propx': 'an unrelated internal property',
            'propn': None,
            'propi': 8,
        },
        'c': [
            {'arrayprop': 'simple'},
            {'arrayprop': 'unrelated'},
        ],
        'd': ['simple', 'unrelated', 'simple'],
        'dd': [['simple', 'unrelated'], ['simple']]
    }

    highlights = {
        'a': ['<em>simple</em>'],
        'b.prop': ['<em>simple</em>'],
        'c.arrayprop': ['<em>simple</em>'],
        'd': ['<em>simple</em>'],
        'dd': ['<em>simple</em>'],
    }

    source = merge_highlight_into_source(source, highlights)

    assert source == {
        'a': 'a <em>simple</em> string',
        'ax': 'an unrelated string',
        'ab': True,
        'ai': 5,
        'b': {
            'prop': 'a <em>simple</em> internal property',
            'propx': 'an unrelated internal property',
            'propn': None,
            'propi': 8,
        },
        'c': [
            {'arrayprop': '<em>simple</em>'},
            {'arrayprop': 'unrelated'},
        ],
        'd': ['<em>simple</em>', 'unrelated', '<em>simple</em>'],
        'dd': [['<em>simple</em>', 'unrelated'], ['<em>simple</em>']]
    }