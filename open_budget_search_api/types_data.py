TYPES_DATA = [
    {
        'type_name': 'exemption',
        'mapping': {
            'properties': {
                'publication_id': {
                    'type': 'integer'
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
                    'type': 'long'
                },
                'start_date': {
                    'type': 'date',
                    'format': 'date'
                },
                'end_date': {
                    'type': 'date',
                    'format': 'date'
                },
                'claim_date': {
                    'type': 'date',
                    'format': 'date'
                },
                'last_update_date': {
                    'type': 'date',
                    'format': 'date'
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
                    }
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
                    'type': 'double'
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
                    }
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
                    }
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

    },
    {
        'type_name': 'budget',
        'mapping': {
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
                    'type': 'date'
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
                    'type': 'long'
                },
                'net_revised': {
                    'type': 'long'
                },
                'net_used': {
                    'type': 'long'
                },
                'gross_allocated': {
                    'type': 'long'
                },
                'gross_revised': {
                    'type': 'long'
                },
                'personnel_allocated': {
                    'type': 'double'
                },
                'personnel_revised': {
                    'type': 'double'
                },
                'commitment_allocated': {
                    'type': 'long'
                },
                'commitment_revised': {
                    'type': 'long'
                },
                'amounts_allocated': {
                    'type': 'long'
                },
                'amounts_revised': {
                    'type': 'long'
                },
                'contractors_allocated': {
                    'type': 'long'
                },
                'contractors_revised': {
                    'type': 'long'
                },
                'dedicated_allocated': {
                    'type': 'long'
                },
                'dedicated_revised': {
                    'type': 'long'
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
            'properties': {
                'year': {
                    'type': 'date'
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
                    }
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
                    'type': 'long'
                },
                'amount_allocated': {
                    'type': 'long'
                },
                'amount_supported': {
                    'type': 'long'
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
            'properties': {
                'year': {
                    'type': 'date',
                },
                'leading_item': {
                    'type': 'long'
                },
                'req_code': {
                    'type': 'long'
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
                    'type': 'long'
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
                    'type': 'long'
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
                    'type': 'long'
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
                'net_expense_diff': {
                    'type': 'long'
                },
                'gross_expense_diff	': {
                    'type': 'long'
                },
                'allocated_income_diff': {
                    'type': 'long'
                },
                'commitment_limit_diff	': {
                    'type': 'long'
                },
                'personnel_max_diff': {
                    'type': 'double'
                },
                'date': {
                    'type': 'date',
                    'format': 'dd/MM/yyyy||yyyy-MM-dd'
                },
                'pending': {
                    "type": "boolean"
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
            'properties': {
                'id': {
                    'type': 'long'
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
                    'type': 'boolean'
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
                    'type': 'long'
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
                    }
                },
                'company_city': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'company_ceo': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'lat': {
                    'type': 'double'
                },
                'lng': {
                    'type': 'double'
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
                    'type': 'long'
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
                    'type': 'double'
                },
                'executed': {
                    'type': 'double'
                },
                'currency': {
                    'type': 'string',
                    'index': 'not_analyzed'
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
                    'type': 'string'
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
                    'type': 'long'
                },
                'sensitive_order': {
                    'type': 'boolean'
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
