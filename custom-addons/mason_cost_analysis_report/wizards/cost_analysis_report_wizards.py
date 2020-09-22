# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, fields
from odoo.tools.safe_eval import safe_eval


class CostAnalysisReportWizards(models.TransientModel):
    _name = "cost.analysis.report.wizards"
    _description = "Cost Analysis Report Wizards"

    labor_type = fields.Selection(
        selection=[("labor_cost_piece", "Labor Cost/Piece"),
                   ("labor_cost_day", "Labor Cost/Day"),
                   ("labor_cost_day_ot", "Labor Cost/Day(OT)")],
        string="Labor Type",
    )

    def button_export_html(self):
        self.ensure_one()
        xml_id = "mason_cost_analysis_report.action_cost_analysis_report_html"
        action = self.env.ref(xml_id)
        vals = action.read()[0]
        context = vals.get("context", {})
        if context:
            context = safe_eval(context)
        model = self.env["cost.analysis.report"]
        report = model.create(self._prepare_cost_analysis_report())
        context["active_id"] = report.id
        context["active_ids"] = report.ids
        vals["context"] = context
        return vals

    def button_export_pdf(self):
        self.ensure_one()
        report_type = "qweb-pdf"
        return self._export(report_type)

    def button_export_xlsx(self):
        self.ensure_one()
        report_type = "xlsx"
        return self._export(report_type)

    def _prepare_cost_analysis_report(self):
        self.ensure_one()
        return {
            "labor_type": self.labor_type,
        }

    def _export(self, report_type):
        model = self.env["cost.analysis.report"]
        report = model.create(self._prepare_cost_analysis_report())
        return report.print_report(report_type)
