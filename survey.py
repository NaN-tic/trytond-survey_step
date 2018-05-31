#!/usr/bin/env python
# This file is part of the survey_step module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond import backend
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import Pool, PoolMeta
from trytond.tools.multivalue import migrate_property
from trytond.modules.company.model import (
    CompanyMultiValueMixin, CompanyValueMixin)

__all__ = ['SurveyStep', 'SurveyField', 'Configuration', 'ConfigurationStep']

step = fields.Many2One('survey.step', 'Step', required=True)


class SurveyStep(ModelSQL, ModelView):
    'Survey Step'
    __name__ = 'survey.step'
    name = fields.Char('Name', required=True, translate=True)
    code = fields.Char('Code', required=True)
    sequence = fields.Integer('Sequence')

    @staticmethod
    def default_sequence():
        return 1

    @classmethod
    def __setup__(cls):
        super(SurveyStep, cls).__setup__()
        cls._order.insert(0, ('sequence', 'ASC'))


class SurveyField:
    __metaclass__ = PoolMeta
    __name__ = 'survey.field'
    step = fields.Many2One('survey.step', 'Step', ondelete='CASCADE',
        select=True)

    @classmethod
    def default_step(cls):
        Config = Pool().get('survey.configuration')
        config = Config(1)
        return config.step.id if config.step else None


class Configuration(CompanyMultiValueMixin):
    __metaclass__ = PoolMeta
    __name__ = 'survey.configuration'
    step = fields.MultiValue(step)


class ConfigurationStep(ModelSQL, CompanyValueMixin):
    "Survey Configuration Step"
    __name__ = 'survey.configuration.step'
    step = step

    @classmethod
    def __register__(cls, module_name):
        TableHandler = backend.get('TableHandler')
        exist = TableHandler.table_exist(cls._table)

        super(ConfigurationStep, cls).__register__(module_name)

        if not exist:
            cls._migrate_property([], [], [])

    @classmethod
    def _migrate_property(cls, field_names, value_names, fields):
        field_names.extend(['step'])
        value_names.extend(['step'])
        fields.append('company')
        migrate_property('survey.configuration', field_names, cls, value_names,
            fields=fields)
