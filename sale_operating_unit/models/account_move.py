# © 2019 ForgeFlow S.L.
# - Jordi Ballester Alomar
# © 2019 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import _, api, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def _search_default_journal(self, journal_types):
        company_id = self._context.get("default_company_id", self.env.company.id)
        domain = [("company_id", "=", company_id), ("type", "in", journal_types)]
        if self._context.get("active_model") == "sale.order":
            order = self.env["sale.order"].search(
                [("id", "in", self._context.get("active_ids"))]
            )
            domain.append(("operating_unit_id", "=", order.operating_unit_id.id))
        journal = None
        if self._context.get("default_currency_id"):
            currency_domain = domain + [
                ("currency_id", "=", self._context["default_currency_id"])
            ]
            journal = self.env["account.journal"].search(currency_domain, limit=1)

        if not journal:
            journal = self.env["account.journal"].search(domain, limit=1)

        if not journal:
            company = self.env["res.company"].browse(company_id)

            error_msg = _(
                "No journal could be found in company %(company_name)s for any of those"
                " types: %(journal_types)s",
                company_name=company.display_name,
                journal_types=", ".join(journal_types),
            )
            raise UserError(error_msg)

        return journal
