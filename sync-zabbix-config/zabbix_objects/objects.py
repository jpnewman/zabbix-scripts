from collections import OrderedDict

ZABBIX_OBJECTS = OrderedDict({
    'action': {
        'get_query': [
            'selectFilter',
            'selectOperations',
            'selectRecoveryOperations'
        ],
        'exclude_create_keys': [
            'eval_formula',
            'maintenance_mode',
            'operationid'
        ],
        'exclude_update_keys': [
            'eval_formula',
            'eventsource',
            'maintenance_mode'
        ]
    },
    'alert': {
        'get_query': [
            'selectHosts',
            'selectMediatypes',
            'selectUsers'
        ]
    },
    'application': {
        'get_query': [
            'selectHost',
            'selectItems',
            'selectDiscoveryRule',
            'selectApplicationDiscovery'
        ],
        'exclude_update_keys': [
            'flags'
        ]
    },
    'correlation': {
        'get_query': [
            'selectFilter',
            'selectOperations'
        ]
    },
    'dhost': {
        'get_query': [
            'selectDRules',
            'selectDServices'
        ]
    },
    'dservice': {
        'get_query': [
            'selectDRules',
            'selectDHosts',
            'selectHosts'
        ]
    },
    'dcheck': {
        'import': False
    },
    'drule': {
        'get_query': [
            'selectDChecks',
            'selectDHosts'
        ]
    },
    'event': {
        'get_query': [
            'selectHosts',
            'selectRelatedObject',
            'select_alerts',
            'select_acknowledges',
            'selectTags'
        ],
        'import': False
    },
    'graph': {
        'get_query': [
            'selectGroups',
            'selectTemplates',
            'selectHosts',
            'selectItems',
            'selectGraphDiscovery',
            'selectGraphItems',
            'selectDiscoveryRule'
        ],
        'exclude_update_keys': [
            'groups',
            'templates',
            'hosts',
            'items',
            'graphDiscovery',
            'graphItems',
            'discoveryRule',
            'templateid',
            'flags',
            'gitems'
        ]
    },
    'graphitem': {
        'get_query': [
            'selectGraphs'
        ],
        'id': 'gitemid',
        'import': False
    },
    'graphprototype': {
        'get_query': [
            'selectDiscoveryRule',
            'selectGraphItems',
            'selectGroups',
            'selectHosts',
            'selectItems',
            'selectTemplates'
        ],
        'id': 'graphid',
        'exclude_update_keys': [
            'templateid',
            'flags'
        ]
    },
    'history': {
        'import': False
    },
    'host': {
        'get_query': [
            'selectGroups',
            'selectApplications',
            'selectDiscoveries',
            'selectDiscoveryRule',
            'selectGraphs',
            'selectHostDiscovery',
            'selectHttpTests',
            'selectInterfaces',
            'selectInventory',
            'selectItems',
            'selectMacros',
            'selectParentTemplates',
            'selectScreens',
            'selectTriggers'
        ]
    },
    'hostgroup': {
        'get_query': [
            'selectDiscoveryRule',
            'selectGroupDiscovery',
            'selectHosts',
            'selectTemplates'
        ],
        'id': 'groupid',
        'exclude_update_keys': [
            'internal'
        ]
    },
    'hostinterface': {
        'get_query': [
            'selectItems',
            'selectHosts'
        ],
        'id': 'interfaceid'
    },
    'hostprototype': {
        'get_query': [
            'selectDiscoveryRule',
            'selectGroupLinks',
            'selectGroupPrototypes',
            'selectInventory',
            'selectParentHost',
            'selectTemplates'
        ],
        'id': 'hostid',
        'exclude_update_keys': [
            'discoveryRule',
            'groupLinks',
            'groupPrototypes',
            'parentHost',
            'templates',
            'maintenance_type',
            'available',
            'jmx_.*',
            'ipmi_.*',
            'snmp_.*',
            'lastaccess',
            'proxy_hostid',
            'tls_.*',
            'description',
            'error',
            'maintenanceid',
            'disable_until',
            'flags',
            'templateid',
            'maintenance_from',
            'maintenance_status'
        ]
    },
    'iconmap': {
        'get_query': [
            'selectMappings'
        ]
    },
    'image': {
        'exclude_update_keys': [
            'imagetype'
        ]
    },
    'item': {
        'get_query': [
            'selectHosts',
            'selectInterfaces',
            'selectTriggers',
            'selectGraphs',
            'selectApplications',
            'selectDiscoveryRule',
            'selectItemDiscovery'
        ],
        'exclude_update_keys': [
            'templateid',
            'state'
        ]
    },
    'itemprototype': {
        'get_query': [
            'selectApplications',
            'selectApplicationPrototypes',
            'selectDiscoveryRule',
            'selectGraphs',
            'selectHosts',
            'selectTriggers'
        ],
        'id': 'itemid',
        'exclude_update_keys': [
            'applications',
            'applicationPrototypes',
            'discoveryRule',
            'graphs',
            'hosts',
            'triggers',
            'templateid',
            'state'
        ]
    },
    'service': {
        'get_query': [
            'selectParent',
            'selectDependencies',
            'selectParentDependencies',
            'selectTimes',
            'selectAlarms',
            'selectTrigger'
        ]
    },
    'discoveryrule': {
        'get_query': [
            'selectFilter',
            'selectGraphs',
            'selectHostPrototypes',
            'selectHosts',
            'selectItems',
            'selectTriggers'
        ],
        'id': 'itemid',
        'exclude_update_keys': [
            'templateid',
            'state'
        ]
    },
    'maintenance': {
        'get_query': [
            'selectGroups',
            'selectHosts',
            'selectTimeperiods'
        ]
    },
    'map': {
        'get_query': [
            'selectIconMap',
            'selectLinks',
            'selectSelements',
            'selectUrls',
            'selectUsers',
            'selectUserGroups'
        ],
        'id': 'sysmapid'
    },
    'usermedia': {
    },
    'mediatype': {
        'get_query': [
            'selectUsers'
        ]
    },
    'problem': {
        'get_query': [
            'selectAcknowledges',
            'selectTags'
        ]
    },
    'proxy': {
        'get_query': [
            'selectHosts',
            'selectInterface'
        ]
    },
    'screen': {
        'get_query': [
            'selectUsers',
            'selectUserGroups',
            'selectScreenItems'
        ],
        'exclude_update_keys': [
            'templateid'
        ]
    },
    'screenitem': {
    },
    'script': {
        'get_query': [
            'selectGroups',
            'selectHosts'
        ]
    },
    'template': {
        'get_query': [
            'selectGroups',
            'selectHosts',
            'selectTemplates',
            'selectParentTemplates',
            'selectHttpTests',
            'selectItems',
            'selectDiscoveries',
            'selectTriggers',
            'selectGraphs',
            'selectApplications',
            'selectMacros',
            'selectScreens'
        ]
    },
    'templatescreen': {
        'get_query': [
            'selectScreenItems'
        ],
        'id': 'hostid',
        'exclude_update_keys': [
            'templateid',
            'userid',
            'private'
        ]
    },
    'templatescreenitem': {
        'id': 'screenitemid',
        'import': False
    },
    'trend': {
        'import': False
    },
    'trigger': {
        'get_query': [
            'selectGroups',
            'selectHosts',
            'selectItems',
            'selectFunctions',
            'selectDependencies',
            'selectDiscoveryRule',
            'selectLastEvent',
            'selectTags'
        ],
        'exclude_update_keys': [
            'value',
            'lastchange',
            'error',
            'templateid',
            'state',
            'flags'
        ]
    },
    'triggerprototype': {
        'get_query': [
            'selectDiscoveryRule',
            'selectFunctions',
            'selectGroups',
            'selectHosts',
            'selectItems',
            'selectDependencies',
            'selectTags'
        ],
        'id': 'triggerid',
        'exclude_update_keys': [
            'discoveryRule',
            'functions',
            'groups',
            'hosts',
            'items',
            'dpendencies',
            'tags',
            'value',
            'lastchange',
            'templateid',
            'state',
            'flags',
            'description',
            'recovery_mode',
            'correlation_mode',
            'manual_close',
            'expression'
        ]
    },
    'user': {
        'get_query': [
            'selectMedias',
            'selectMediatypes',
            'selectUsrgrps'
        ]
    },
    'usergroup': {
        'get_query': [
            'selectUsers',
            'selectRights'
        ],
        'id': 'usrgrpid'
    },
    'usermacro': {
        'get_query': [
            'selectGroups',
            'selectHosts',
            'selectTemplates'
        ]
    },
    'valuemap': {
        'get_query': [
            'selectMappings'
        ]
    },
    'httptest': {
        'get_query': [
            'selectHosts',
            'selectSteps'
        ]
    }
})
