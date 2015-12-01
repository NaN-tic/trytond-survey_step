# This file is part of the survey_step module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class SurveyStepCase(ModuleTestCase):
    'Test Survey Step module'
    module = 'survey_step'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        SurveyStepCase))
    return suite
