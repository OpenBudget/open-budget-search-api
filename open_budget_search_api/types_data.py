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
                    'type': 'long'
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
        'search_fields': ["exemption.publisher", "exemption.regulation", "exemption.supplier", "exemption.contact", "exemption.contact_email", "exemption.description", "exemption.reason", "exemption.decision", "exemption.url", "exemption.subjects", "exemption.source_currency", "exemption.page_title", "exemption.entity_kind"],
        'date_fields': {
            'from' : 'start_date',
            'to': 'end_date'
        },
        'range_structure': {
                            "start_date":{
                                        "gte": "from_date"
                                    },
                            "end_date":{
                                        "lte": "to_date"
                                    }
                            },
        'sort_method':[
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
        'search_fields': ["budget.title",
                          "budget.code",
                          "budget.kind",
                          "budget.subkind",
                          "budget.group_top",
                          "budget.group_full",
                          "budget.class_top",
                          "budget.class_full",
                          "budget.properties"],
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
        'sort_method':[
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
        'search_fields': ["supports.subject", "supports.code", "supports.recipient", "supports.kind", "supports.title", "supports.entity_id", "supports.entity_kind"],
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
        'search_fields': ["changes.req_title", "changes.change_title", "changes.change_type_name", "changes.budget_code", "changes.budget_title"],
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
    # {
    #     'type_name': 'change_history',
    #     'search_fields': ["change_history.model", "change_history.selector", "change_history.field", "change_history.from_value", "change_history.to_value"],
    #     'mapping': {
    #         'properties': {
    #             'model': {
    #                 'type': 'string'
    #             },
    #             'time': {
    #                 'type': 'date',
    #                 'format': 'dd/MM/yy||yyyy-MM-dd'
    #             },
    #             'field': {
    #                 'type': 'string',
    #             },
    #             'from_value': {
    #                 'type': 'string',
    #                 'analyzer': 'hebrew',
    #                 'fields': {
    #                     'raw': {
    #                         'type': 'string',
    #                         'index': 'not_analyzed'
    #                     }
    #                 }
    #             },
    #             'to_value': {
    #                 'type': 'string',
    #                 'analyzer': 'hebrew',
    #                 'fields': {
    #                     'raw': {
    #                         'type': 'string',
    #                         'index': 'not_analyzed'
    #                     }
    #                 }
    #             },
    #             'created': {
    #                 'type': 'boolean'
    #             }
    #         }
    #     },
    #     'date_fields': {
    #         'from': 'time',
    #         'to': 'time'
    #     },
    #     "range_structure": {
    #                         'time': {
    #                             "gte": "from_date",
    #                             "lte": "to_date"
    #                         }
    #                     },
    #     'sort_method': [
    #                     {
    #                         "time": {
    #                             "order": "desc"
    #                         }
    #                     }
    #                 ]
    # },
    {
        'type_name': 'entities',
        'search_fields': ["entities.kind", "entities.name", "entities.manpower_contractor", "entities.service_contractor", "entities.company_name", "entities.company_status", "entities.company_type", "entities.company_government", "entities.company_limit", "entities.company_government", \
                          "entities.company_limit", "entities.company_mafera", "entities.company_address", "entities.company_city"],
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
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'service_contractor': {
                    'type': 'string',
                    'analyzer': 'hebrew',
                    'fields': {
                        'raw': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
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
    }
]
