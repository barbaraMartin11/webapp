#!/usr/bin/env python
# -*- coding: utf-8 -*
"""This is very simple demo that executes a script and counts the number of
models it generates.
"""
##############################################################################
# Copyright (c) 2017 martin@bigml.com
# All rights reserved.
# This software is proprietary and confidential and may not under
# any circumstances be used, copied, or distributed.
##############################################################################
import sys
import argparse
import re

from bigml.constants import FINISHED
from bigml.api import BigML

API = BigML()


def create_parser():
    """Parses the user-given parameters.
    """
    parser = argparse.ArgumentParser(
        description="First example",
        epilog="Batch 2017")

    # script
    parser.add_argument('--script',
                        required=True,
                        action='store',
                        dest='script',
                        help="A script to execute")

    parser.add_argument('--dataset',
                        required=True,
                        action='store',
                        dest='dataset',
                        help="A dataset to use")
#
#    parser.add_argument('--features',
#                        required=True,
#                        action='store',
#                        dest='features',
#                        help="Number of features")
    return parser


def main(args=sys.argv[1:]):
    """Parses command-line parameters and calls the actual main function.
    """

    # Parse arguments
    args = create_parser().parse_args(args)

    execution = API.create_execution(
        args.script, {'inputs': [['dataset-id', args.dataset]]})

    execution_id = execution['resource']
    e_id = re.split('execution/', execution_id)[1]
    execution_status = 0

    while execution_status != FINISHED:
        execution_resource = API.get_execution(execution_id)
        execution_status = execution_resource['object']['status']['code']
        number_of_models = API.list_models(
            "execution_id=%s" % e_id)['meta']['total_count']
        print "models: %s" % number_of_models
    return

if __name__ == "__main__":
    main()
