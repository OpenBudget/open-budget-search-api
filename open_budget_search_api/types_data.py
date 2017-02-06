TYPES_DATA = [
    {
        'type_name': 'exemption',
        'mapping': {
            '_all': {
                'index_analyzer': 'nGram_analyzer',
                'search_analyzer': 'whitespace_analyzer'
            },
            'properties': {
                'publication_id': {
                    'type': 'integer',
                    'include_in_all': False
                },
                'publisher': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'regulation': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'supplier': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'supplier_id': {
                    'type': 'long',
                    'include_in_all': False
                },
                'start_date': {
                    'type': 'date',
                    'format': 'date',
                    'include_in_all': False
                },
                'end_date': {
                    'type': 'date',
                    'format': 'date',
                    'include_in_all': False
                },
                'claim_date': {
                    'type': 'date',
                    'format': 'date',
                    'include_in_all': False
                },
                'last_update_date': {
                    'type': 'date',
                    'format': 'date',
                    'include_in_all': False
                },
                'contact': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'contact_email': {
                    'type': 'string',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    },
                    'include_in_all': False
                },
                'description': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'volume': {
                    'type': 'double',
                    'include_in_all': False
                },
                'reason': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'decision': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'url': {
                    'type': 'string',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    },
                    'include_in_all': False
                },
                'subjects': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'source_currency': {
                    'type': 'string',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    },
                    'include_in_all': False
                },
                'page_title': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'entity_id': {
                    'type': 'string',
                    'include_in_all': False
                },
                'entity_kind': {
                    'type': 'string',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                }
            }
        },
        'search_fields': ["publisher",
                          "regulation",
                          "supplier",
                          "contact",
                          "contact_email",
                          "description",
                          "reason",
                          "decision",
                          "url",
                          "subjects",
                          "source_currency",
                          "page_title",
                          "entity_kind"],
        'date_fields': {
            'from': 'start_date',
            'to': 'end_date'
        },
        'range_structure': {
            "start_date": {
                "gte": "from_date"
            },
            "end_date": {
                "lte": "to_date"
            }
        },
        'sort_method': [
            {
                "start_date": {
                    "order": "desc"
                }
            },
            {
                "volume": {
                    "order": "desc"
                }
            }
        ]

    },
    {
        'type_name': 'budget',
        'mapping': {
            '_all': {
                'index_analyzer': 'nGram_analyzer',
                'search_analyzer': 'whitespace_analyzer'
            },
            'properties': {
                'code': {
                    'type': 'string',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'year': {
                    'type': 'date',
                    'include_in_all': False
                },
                'title': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'net_allocated': {
                    'type': 'long',
                    'include_in_all': False
                },
                'net_revised': {
                    'type': 'long',
                    'include_in_all': False
                },
                'net_used': {
                    'type': 'long',
                    'include_in_all': False
                },
                'gross_allocated': {
                    'type': 'long',
                    'include_in_all': False
                },
                'gross_revised': {
                    'type': 'long',
                    'include_in_all': False
                },
                'personnel_allocated': {
                    'type': 'double',
                    'include_in_all': False
                },
                'personnel_revised': {
                    'type': 'double',
                    'include_in_all': False
                },
                'commitment_allocated': {
                    'type': 'long',
                    'include_in_all': False
                },
                'commitment_revised': {
                    'type': 'long',
                    'include_in_all': False
                },
                'amounts_allocated': {
                    'type': 'long',
                    'include_in_all': False
                },
                'amounts_revised': {
                    'type': 'long',
                    'include_in_all': False
                },
                'contractors_allocated': {
                    'type': 'long',
                    'include_in_all': False
                },
                'contractors_revised': {
                    'type': 'long',
                    'include_in_all': False
                },
                'dedicated_allocated': {
                    'type': 'long',
                    'include_in_all': False
                },
                'dedicated_revised': {
                    'type': 'long',
                    'include_in_all': False
                },
                'equiv_code': {
                    'type': 'string',
                    'analyzer': 'hebrew'
                },
                'group_full': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'group_top': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'class_full': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'class_top': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'kind': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'subkind': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                }
            }
        },
        'search_fields': ["title",
                          "code",
                          "kind",
                          "subkind",
                          "group_top",
                          "group_full",
                          "class_top",
                          "class_full",
                          "properties"],
        'date_fields': {
            'from': 'year',
            'to': 'year'
        },
        "range_structure": {
            'year': {
                "gte": "from_date",
                "lte": "to_date"
            }
        },
        'sort_method': [
            {
                "year": {
                    "order": "desc"
                }
            },
            {
                "net_revised": {
                    "order": "desc"
                }
            }
        ]
    },
    {
        'type_name': 'supports',
        'search_fields': ["subject",
                          "code",
                          "recipient",
                          "kind",
                          "title",
                          "entity_id",
                          "entity_kind"],
        'mapping': {
            '_all': {
                'index_analyzer': 'nGram_analyzer',
                'search_analyzer': 'whitespace_analyzer'
            },
            'properties': {
                'year': {
                    'type': 'date',
                    'include_in_all': False
                },
                'subject': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'code': {
                    'type': 'string',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    },
                    'include_in_all': False
                },
                'recipient': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'kind': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'title': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'num_used': {
                    'type': 'long',
                    'include_in_all': False
                },
                'amount_allocated': {
                    'type': 'long',
                    'include_in_all': False
                },
                'amount_supported': {
                    'type': 'long',
                    'include_in_all': False
                },
                'entity_id': {
                    'type': 'string',
                    'include_in_all': False
                },
                'entity_kind': {
                    'type': 'string',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                }
            }
        },
        'date_fields': {
            'from': 'year',
            'to': 'year'
        },
        "range_structure": {
            'year': {
                "gte": "from_date",
                "lte": "to_date"
            }
        },
        'sort_method': [
            {
                "year": {
                    "order": "desc"
                }
            },
            {
                "amount_allocated": {
                    "order": "desc"
                }
            }
        ]
    },
    {
        'type_name': 'changes',
        'search_fields': ["req_title",
                          "change_title",
                          "change_type_name",
                          "budget_code",
                          "budget_title"],
        'mapping': {
            '_all': {
                'index_analyzer': 'nGram_analyzer',
                'search_analyzer': 'whitespace_analyzer'
            },
            'properties': {
                'year': {
                    'type': 'date',
                    'include_in_all': False
                },
                'leading_item': {
                    'type': 'long',
                    'include_in_all': False
                },
                'req_code': {
                    'type': 'long',
                    'include_in_all': False
                },
                'req_title': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'change_code': {
                    'type': 'long',
                    'include_in_all': False
                },
                'change_title': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'change_type_id': {
                    'type': 'long',
                    'include_in_all': False
                },
                'change_type_name': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'committee_id': {
                    'type': 'long',
                    'include_in_all': False
                },
                'budget_code': {
                    'type': 'string',
                    'include_in_all': False
                },
                'budget_title': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'net_expense_diff': {
                    'type': 'long',
                    'include_in_all': False
                },
                'gross_expense_diff	': {
                    'type': 'long',
                    'include_in_all': False
                },
                'allocated_income_diff': {
                    'type': 'long',
                    'include_in_all': False
                },
                'commitment_limit_diff	': {
                    'type': 'long',
                    'include_in_all': False
                },
                'personnel_max_diff': {
                    'type': 'double',
                    'include_in_all': False
                },
                'date': {
                    'type': 'date',
                    'format': 'dd/MM/yyyy||yyyy-MM-dd',
                    'include_in_all': False
                },
                'pending': {
                    "type": "boolean",
                    'include_in_all': False
                }
            }
        },
        'date_fields': {
            'from': 'date',
            'to': 'date'
        },
        "range_structure": {
            'date': {
                "gte": "from_date",
                "lte": "to_date"
            }
        },
        'sort_method': [
            {
                "date": {
                    "order": "desc"
                }
            },
            {
                "gross_expense_diff": {
                    "order": "desc"
                }
            }
        ]
    },
    {
        'type_name': 'entities',
        'search_fields': ["kind",
                          "name",
                          "manpower_contractor",
                          "service_contractor",
                          "company_name",
                          "company_status",
                          "company_type",
                          "company_government",
                          "company_limit",
                          "company_government",
                          "company_limit",
                          "company_mafera",
                          "company_address",
                          "company_city"],
        'mapping': {
            '_all': {
                'index_analyzer': 'nGram_analyzer',
                'search_analyzer': 'whitespace_analyzer'
            },
            'properties': {
                'id': {
                    'type': 'long',
                    'include_in_all': False
                },
                'kind': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'name': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'manpower_contractor': {
                    'type': 'object',
                },
                'service_contractor': {
                    'type': 'object',
                },
                'gov_company': {
                    'type': 'boolean',
                    'include_in_all': False
                },
                'company_name': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'company_status': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'company_type': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'company_government': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'company_limit': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'company_postal_code': {
                    'type': 'long',
                    'include_in_all': False
                },
                'company_mafera': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'company_address': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    },
                    'include_in_all': False
                },
                'company_city': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    },
                    'include_in_all': False
                },
                'company_ceo': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    },
                    'include_in_all': False
                },
                'lat': {
                    'type': 'double',
                    'include_in_all': False
                },
                'lng': {
                    'type': 'double',
                    'include_in_all': False
                },
            }
        },
        'date_fields': {
            'from': 'NA',
            'to': 'NA'
        },
        "range_structure": {
            'time': {
                "gte": "NA",
                "lte": "NA"
            }
        },
        'sort_method': [
            {
                "id": {
                    "order": "desc"
                }
            }
        ]
    },
    {
        'type_name': 'procurement',
        'mapping': {
            '_all': {
                'index_analyzer': 'nGram_analyzer',
                'search_analyzer': 'whitespace_analyzer'
            },
            'properties': {
                'publisher': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'purchasing_unit': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'buyer_description': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'budget_code': {
                    'type': 'string'
                },
                'budget_title': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'supplier_code': {
                    'type': 'long',
                    'include_in_all': False
                },
                'supplier_name': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'volume': {
                    'type': 'double',
                    'include_in_all': False
                },
                'executed': {
                    'type': 'double',
                    'include_in_all': False
                },
                'currency': {
                    'type': 'string',
                    'index': 'not_analyzed',
                    'include_in_all': False
                },
                'purchase_method': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'manof_ref': {
                    'type': 'string',
                    'include_in_all': False
                },
                'exemption_reason': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'purpose': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'order_id': {
                    'type': 'long',
                    'include_in_all': False
                },
                'sensitive_order': {
                    'type': 'boolean',
                    'include_in_all': False
                },
                'report_date': {
                    'type': 'date',
                    'format': 'date'
                },
                'report_title': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'report_publisher': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'report_subunit': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'report_error': {
                    'type': 'string',
                    'index': 'not_analyzed'
                },
                'report_href': {
                    'type': 'string',
                    'index': 'not_analyzed'
                },
                'report_container_href': {
                    'type': 'string',
                    'index': 'not_analyzed'
                },
                'report_year': {
                    'type': 'integer'
                },
                'report_period': {
                    'type': 'integer'
                },
                'report_date': {
                    'type': 'date',
                    'format': 'date'
                },
                'entity_id': {
                    'type': 'string'
                },
                'entity_kind': {
                    'type': 'string',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                }
            }
        },
        'search_fields': ["publisher",
                          "regulation",
                          "supplier",
                          "contact",
                          "contact_email",
                          "description",
                          "reason",
                          "decision",
                          "url",
                          "subjects",
                          "source_currency",
                          "page_title",
                          "entity_kind"],
        'date_fields': {
            'from': 'start_date',
            'to': 'end_date'
        },
        'range_structure': {
            "start_date": {
                "gte": "from_date"
            },
            "end_date": {
                "lte": "to_date"
            }
        },
        'sort_method': [
            {
                "start_date": {
                    "order": "desc"
                }
            },
            {
                "volume": {
                    "order": "desc"
                }
            }
        ]

    }
]

KEYS = {
    'budget': ['year', 'code'],
    'exemption': ['publication_id'],
    'supports': ['year', 'code', 'recipient', 'kind'],
    'changes': ['year', 'leading_item', 'req_code', 'budget_code'],
    'entities': ['id'],
    'procurement': ['order_id', 'budget_code', 'report_date', 'report_title']
}
