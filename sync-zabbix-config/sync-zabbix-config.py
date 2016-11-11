#!/usr/bin/env python

import argparse
import logging
import inspect
import json
import sys
import log
import os
import re

from zabbix.api import ZabbixAPI
from zabbix_objects import objects as zo
from collections import OrderedDict

# shorten, refer, extend
DEFAULT_OUTPUT = 'extend'
DEFAULT_QUARY_OUTPUT = 'extend'

SCRIPT_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


# Based on code from: http://stackoverflow.com/questions/27838319/python-delete-all-specific-keys-in-json
def remove_dict_item_by_keys(d, key_pattens=[]):
    """Remove items from dict by keys."""
    if not key_pattens:
        return d

    combined_pattern = "(" + ")|(".join(key_pattens) + ")"
    return remove_dict_item_by_key_patten(d, combined_pattern)


def remove_dict_item_by_key_patten(d, key_patten):
    """Returns items from dict that don't match key regex patten."""
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [remove_dict_item_by_key_patten(v, key_patten) for v in d]
    return {k: remove_dict_item_by_key_patten(v, key_patten) for k, v in d.items()
            if not re.match(key_patten, k)}


# http://stackoverflow.com/questions/27973988/python-how-to-remove-all-empty-fields-in-a-nested-dict/35263074
def remove_empty_dict_items(d):
    """Returns items from dict without empty values."""
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [v for v in (remove_empty_dict_items(v) for v in d) if v]
    return {k: v for k, v in ((k, remove_empty_dict_items(v)) for k, v in d.items()) if v}


def _parse_args():
    """Parse Command Arguments."""
    desc = 'Python zabbix api'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('action',
                        choices=['export', 'import'],
                        help='Sync Action')
    parser.add_argument('server',
                        help='Zabbix Server')
    parser.add_argument('-u', '--user',
                        default='Admin',
                        help='Zabbix Username')
    parser.add_argument('-p', '--password',
                        default='zabbix',
                        help='Zabbix Password')
    parser.add_argument('-o', '--objects',
                        nargs='+',
                        type=str,
                        default=[],
                        help='Sync Objects')
    parser.add_argument('-a', '--data-path',
                        default=os.path.join(SCRIPT_DIR, '_data'),
                        help='Archive Data Path')
    parser.add_argument('-q', '--exclude-queries',
                        action='store_true',
                        default=False,
                        help='Exclude Get Queries')
    parser.add_argument('-e', '--exclude-empty-objects',
                        action='store_true',
                        default=False,
                        help='Exclude Empty Objects')
    parser.add_argument('-l', '--log-level',
                        default='INFO',
                        help='Log Level')
    parser.add_argument('-d', '--dry-run',
                        action='store_true',
                        default=False,
                        help='Dry-run. No action taken')

    args = parser.parse_args()

    print("{0} Zabbix server '{1}' objects...".format(args.action.title(), args.server))

    args.data_path = os.path.abspath(args.data_path)
    print("Data Path: {0}".format(args.data_path))

    if len(args.objects) > 0:

        if args.action.lower() == 'export':
            print('Exporting objects: -')
        elif args.action.lower() == 'import':
            print('Importing objects: -')
        else:
            print('Syncing objects: -')

        for object_name in args.objects:
            if object_name in zo.ZABBIX_OBJECTS.keys():
                print("  {0}".format(object_name))
            else:
                log.error("'{0}' is not a known Zabbix object!".format(object_name))
                raise
    else:
        args.objects = zo.ZABBIX_OBJECTS.keys()

    return args


def export_object(zapi,
                  object_name,
                  output_file,
                  exclude_empty_objects=False,
                  params={
                      'output': DEFAULT_OUTPUT
                  }):
    """Export Zabbix Object."""
    objects = zapi.do_request(object_name + '.get', params)

    if not objects['result'] and exclude_empty_objects:
        print("{0} (EMPTY)".format(object_name.title()))
    else:
        print("{0}: -".format(object_name.title()))
        for object_data in objects['result']:
            if 'name' in object_data:
                print("  {0}".format(object_data['name']))

        with open(output_file, 'w') as outfile:
            json.dump(objects, outfile, indent=4, sort_keys=True)


def export_objects(zapi,
                   object_names,
                   data_path,
                   exclude_queries=False,
                   exclude_empty_objects=False,
                   params={
                       'output': DEFAULT_OUTPUT
                   }):
    """Export Zabbix Objects."""

    for object_name in object_names:
        params = {'output': DEFAULT_OUTPUT}

        if not exclude_queries:
            if 'get_query' in zo.ZABBIX_OBJECTS[object_name]:
                for query in zo.ZABBIX_OBJECTS[object_name]['get_query']:
                    params[query] = DEFAULT_QUARY_OUTPUT

        output_file = os.path.join(data_path, object_name + '.json')
        export_object(zapi, object_name, output_file, exclude_empty_objects, params)


def create_object(zapi,
                  object_name,
                  object_data):
    """Create Single Object."""

    # Remove keys with empty values
    object_data = {k: v for k, v in object_data.items() if v}

    # Cannot create items, so remove them.
    remove_keys = []
    if 'exclude_create_keys' in zo.ZABBIX_OBJECTS[object_name]:
        remove_keys = zo.ZABBIX_OBJECTS[object_name]['exclude_update_keys']

    objectid_key = get_object_id_key(object_name)
    remove_keys.append(objectid_key)

    # object_data = remove_empty_dict_items(object_data)
    # object_data = remove_dict_item_by_keys(object_data, remove_keys)

    # print(json.dumps(object_data))

    try:
        return zapi.do_request(object_name + '.create', object_data)
    except:
        log.error("Create Failed!")
        log.debug(sys.exc_info(), print_data_type=False)
        return {}


def update_object(zapi,
                  object_name,
                  object_data):
    """Update Single Object."""

    # Cannot update items, so remove them.
    remove_keys = []
    if 'exclude_update_keys' in zo.ZABBIX_OBJECTS[object_name]:
        remove_keys = zo.ZABBIX_OBJECTS[object_name]['exclude_update_keys']

    object_data = remove_empty_dict_items(object_data)
    object_data = remove_dict_item_by_keys(object_data, remove_keys)

    try:
        return zapi.do_request(object_name + '.update', object_data)
    except:
        log.error("Update Failed!")
        log.debug(sys.exc_info(), print_data_type=False)
        return {}


def get_object_id_key(object_name):
    """Get Object Id Key."""
    object_id_key = object_name + 'id'
    if 'id' in zo.ZABBIX_OBJECTS[object_name]:
        object_id_key = zo.ZABBIX_OBJECTS[object_name]['id']

    return object_id_key


def get_object_ids(zapi, object_name):
    """Get Object Ids"""
    current_objects_ids = []

    if not should_import(object_name):
        return current_objects_ids

    objects = zapi.do_request(object_name + '.get', {'output': 'refer'})
    object_id_key = get_object_id_key(object_name)

    for object_data in objects['result']:
        current_objects_ids.append(int(object_data[object_id_key]))

    return current_objects_ids


def should_import(object_name):
    """Should Import."""
    import_obj = True
    if 'import' in zo.ZABBIX_OBJECTS[object_name]:
        import_obj = zo.ZABBIX_OBJECTS[object_name]['import']

    return import_obj


def import_object(zapi,
                  object_name,
                  input_file,
                  exclude_empty_objects=False):
    """Import Zabbix Object."""
    sys.stdout.write(object_name)

    if not os.path.isfile(input_file):
        print(' (FILE NOT FOUND)')
        return

    if not should_import(object_name):
        print(' (SKIPPED)')
        return

    print('')

    object_id_key = get_object_id_key(object_name)
    current_object_ids = get_object_ids(zapi, object_name)

    with open(input_file) as data_file:
        data = json.load(data_file, object_pairs_hook=OrderedDict)

    for object_data in data['result']:
        if object_id_key in object_data:
            if int(object_data[object_id_key]) in current_object_ids:
                if 'name' in object_data:
                    print("  {0} ({1})".format(object_data['name'],
                                               log.colorText('UPDATING', log.CYAN)))

            update_object(zapi, object_name, object_data)
        else:
            if 'name' in object_data:
                print("  {0} ({1})".format(object_data['name'],
                                           log.colorText('CREATING', log.GREEN)))

            create_object(zapi, object_name, object_data)


def import_objects(zapi,
                   object_names,
                   data_path,
                   exclude_empty_objects=False):
    """"Import Zabbix Obejcts."""

    for object_name in object_names:
        input_file = os.path.join(data_path, object_name + '.json')
        import_object(zapi, object_name, input_file, exclude_empty_objects)


def main():
    """Main."""

    args = _parse_args()

    # Create ZabbixAPI class instance
    zapi = ZabbixAPI(url=args.server, user='Admin', password='zabbix')
    print("Auth: {0}".format(zapi.auth))

    # Logging
    stream = logging.StreamHandler(sys.stdout)
    stream.setLevel(logging.DEBUG)
    logger = logging.getLogger('pyzabbix')
    logger.addHandler(stream)
    log_level = logging.getLevelName(args.log_level)
    logger.setLevel(log_level)

    if args.action.lower() == 'export':
        if not os.path.exists(args.data_path):
            os.makedirs(args.data_path)

        export_objects(zapi,
                       args.objects,
                       args.data_path,
                       args.exclude_queries,
                       args.exclude_empty_objects)
    elif args.action.lower() == 'import':
        import_objects(zapi,
                       args.objects,
                       args.data_path,
                       args.exclude_empty_objects)

if __name__ == "__main__":
    main()
