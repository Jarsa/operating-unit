from odoo import models
from odoo.exceptions import ValidationError


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _create_invoice(self, order, so_line, amount):
        invoice = super(SaleAdvancePaymentInv, self)._create_invoice(
            order, so_line, amount
        )
        invoice.sudo().write({"operating_unit_id": order.operating_unit_id.id})
        return invoice

    def _prepare_invoice_values(self, order, name, amount, so_line):
        invoice_vals = super(SaleAdvancePaymentInv, self)._prepare_invoice_values(
            order, name, amount, so_line
        )
        journal = self.env["account.journal"].search(
            [
                ("operating_unit_id", "=", order.operating_unit_id.id),
                ("type", "=", "sale"),
            ],
            limit=1,
        )
        if not journal:
            raise ValidationError(
                _("You need to create a sales journal for this operating unit.")
            )
        invoice_vals.update(
            {
                "operating_unit_id": order.operating_unit_id.id,
                "journal_id": journal.id,
            }
        )
        return invoice_vals
