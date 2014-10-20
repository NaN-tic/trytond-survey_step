#!/usr/bin/env python
# This file is part of the survey_step module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import Pool, PoolMeta

__all__ = ['SurveyStep', 'SurveyField', 'Configuration']
__metaclass__ = PoolMeta


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
    __name__ = 'survey.field'
    step = fields.Many2One('survey.step', 'Step', ondelete='CASCADE',
        select=True)

    @classmethod
    def default_step(cls):
        Config = Pool().get('survey.configuration')
        config = Config(1)
        return config.step.id if config.step else None

    @classmethod
    def __setup__(cls):
        super(SurveyField, cls).__setup__()
        cls._order.insert(0, ('step', 'ASC'))
        cls._order.insert(1, ('sequence', 'ASC'))


class Configuration:
    __name__ = 'survey.configuration'
    step = fields.Property(fields.Many2One('survey.step', 'Step', required=True))
