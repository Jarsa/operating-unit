# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class TimesheetsAnalysisReport(models.Model):
    _inherit = "timesheets.analysis.report"

    operating_unit_id = fields.Many2one("operating.unit", readonly=True)

    @api.model
    def _select(self):
        res = super()._select()
        res += ", A.operating_unit_id AS operating_unit_id"
        return res
