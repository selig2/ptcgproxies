#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of pokemontcgsdk.
# https://github.com/PokemonTCG/pokemon-tcg-sdk-python

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2016, Andrew Backes <backes.andrew@gmail.com>

from pokemontcgsdk.querybuilder import QueryBuilder

class Subtype(object):
    RESOURCE = 'subtypes'

    @staticmethod
    def all():
        return QueryBuilder(Subtype).array()