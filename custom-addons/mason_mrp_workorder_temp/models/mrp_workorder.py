# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, fields
from datetime import datetime


class MrpProductionWorkcenterLine(models.Model):
    _inherit = "mrp.workorder"

    qty_men = fields.Integer(
        string="Men Quantity",
    )
    qty_approved = fields.Float(
        string="Approved Quantity",
        default=0.0,
        digits="Product Unit of Measure",
    )
    labor_type = fields.Selection(
        selection=[("labor_cost_piece", "Labor Cost/Piece"),
                   ("labor_cost_day", "Labor Cost/Day"),
                   ("labor_cost_day_ot", "Labor Cost/Day(OT)")],
        string="Labor Type",
    )
    budget_unit = fields.Float(
        string="Budget/Unit",
        default=0.0,
    )

    def record_production(self):
        self.ensure_one()
        Timeline = self.env["mrp.workcenter.productivity"]
        domain = [
            ("workorder_id", "in", self.ids),
            ("date_end", "=", False),
            ("user_id", "=", self.env.user.id),
        ]
        timeline = Timeline.search(domain, limit=1)
        timeline.write({
            "line_ids": [(0, 0, {
                "date_start":
                    not timeline.line_ids and timeline.date_start or
                    timeline.line_ids.sorted("date_end", reverse=True)[0].date_end,
                "date_end": datetime.now(),
                "qty_done": self.qty_producing,
                "qty_men": self.qty_men,
            })]
        })
        self.qty_men = 0
        return super().record_production()
