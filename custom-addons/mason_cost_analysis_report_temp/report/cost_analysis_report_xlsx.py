# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models


class CostAnalysisReportXLSX(models.TransientModel):
    _name = "report.mason_cost_analysis_report.cost_analysis_report_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Cost Analysis Report Excel"

    def _get_ws_params(self, wb, data, objects):
        report_template = {
            "mo_name": {
                "header": {"value": "MO"},
                "data": {"value": self._render("mo_name")},
                "width": 20,
            },
            "wo_name": {
                "header": {"value": "WO"},
                "data": {"value": self._render("wo_name")},
                "width": 20,
            },
            "origin": {
                "header": {"value": "Source (MO)"},
                "data": {"value": self._render("origin")},
                "width": 20,
            },
            "labor_type": {
                "header": {"value": "Labor Type"},
                "data": {"value": self._render("labor_type")},
                "width": 20,
            },
            "product_qty": {
                "header": {"value": "Production Quantity"},
                "data": {
                    "value": self._render("product_qty"),
                    "format": self.format_tcell_amount_right,
                },
                "width": 20,
            },
            "budget_unit": {
                "header": {"value": "Budget/Unit"},
                "data": {
                    "value": self._render("budget_unit"),
                    "format": self.format_tcell_amount_right,
                },
                "width": 20,
            },
            "total_budget": {
                "header": {"value": "Total Budget"},
                "data": {
                    "value": self._render("total_budget"),
                    "format": self.format_tcell_amount_right,
                },
                "width": 20,
            },
            "qty_produced": {
                "header": {"value": "Quantity Produced"},
                "data": {
                    "value": self._render("qty_produced"),
                    "format": self.format_tcell_amount_right,
                },
                "width": 20,
            },
            "hour_spent": {
                "header": {"value": "Hour Spent"},
                "data": {
                    "value": self._render("hour_spent"),
                    "format": self.format_tcell_amount_right,
                },
                "width": 20,
            },
            "statistic": {
                "header": {"value": "Statistic (Q/Hr)"},
                "data": {
                    "value": self._render("statistic"),
                    "format": self.format_tcell_amount_right,
                },
                "width": 20,
            },
            "labor_cost_day": {
                "header": {"value": "Labor cost/day"},
                "data": {
                    "value": self._render("labor_cost_day"),
                    "format": self.format_tcell_amount_right,
                },
                "width": 20,
            },
            "multiplier": {
                "header": {"value": "Multiplier"},
                "data": {
                    "value": self._render("multiplier"),
                    "format": self.format_tcell_amount_right,
                },
                "width": 20,
            },
            "cost_unit": {
                "header": {"value": "Cost/Unit"},
                "data": {
                    "value": self._render("cost_unit"),
                    "format": self.format_tcell_amount_right,
                },
                "width": 20,
            },
            "total_payment": {
                "header": {"value": "Total Payment"},
                "data": {
                    "value": self._render("total_payment"),
                    "format": self.format_tcell_amount_right,
                },
                "width": 20,
            },
        }
        ws_params = {
            "ws_name": "Cost Analysis Report",
            "generate_ws_method": "_cost_analysis_report",
            "title": "Cost Analysis Report",
            "wanted_list": report_template,
            "col_specs": report_template,
        }
        return [ws_params]

    def _cost_analysis_report(self, wb, ws, ws_params, data, objects):
        ws.set_portrait()
        ws.fit_to_pages(1, 0)
        ws.set_header(self.xls_headers["standard"])
        ws.set_footer(self.xls_footers["standard"])
        self._set_column_width(ws, ws_params)
        row_pos = 0
        # title
        row_pos = self._write_ws_title(ws, row_pos, ws_params, True)
        # filter data
        labor_type_dict = dict(objects._fields["labor_type"].selection)
        ws.write_column(row_pos, 0, ["Labor Type :"], self.format_left_bold)
        ws.write_column(
            row_pos,
            1,
            [
                (labor_type_dict.get(objects.labor_type)) or "",
            ],
        )
        row_pos += 2
        # cost analysis report table
        row_pos = self._write_line(
            ws,
            row_pos,
            ws_params,
            col_specs_section="header",
            default_format=self.format_theader_blue_center,
        )
        ws.freeze_panes(row_pos, 0)
        for obj in objects:
            for line in obj.results:
                # Total Budget = Production Quantity x Budget per unit
                total_budget = line.product_qty * line.budget_unit
                # Hour Spent
                hour_spent = line.get_hour_spent(line.duration)
                # Statistic = Quantity Produced / Hour Spent
                statistic = hour_spent and line.qty_produced / hour_spent or 0
                cost_unit = 0
                if statistic:
                    if line.labor_type in ['labor_cost_piece', 'labor_cost_day_ot']:
                        # Cost per unit = (Labor cost per day / 8 x Multiplier) / statistic
                        cost_unit = (line.labor_cost_day / 8 * line.multiplier) / statistic
                    elif line.labor_type == 'labor_cost_day':
                        # Cost per unit = (Labor cost per day x multiplier) / statistic
                        cost_unit = (line.labor_cost_day * line.multiplier) / statistic
                # Total Payment = Cost per unit x Quantity Produced
                total_payment = cost_unit * line.qty_produced
                row_pos = self._write_line(
                    ws,
                    row_pos,
                    ws_params,
                    col_specs_section="data",
                    render_space={
                        "mo_name": line.mo_name or "",
                        "wo_name": line.wo_name or "",
                        "origin": line.origin or "",
                        "labor_type": labor_type_dict.get(line.labor_type, ""),
                        "product_qty": line.product_qty or 0.00,
                        "budget_unit": line.budget_unit or 0.00,
                        "total_budget": total_budget or 0.00,
                        "qty_produced": line.qty_produced or 0.00,
                        "hour_spent": hour_spent,
                        "statistic": statistic or 0.00,
                        "labor_cost_day": line.labor_cost_day or 0.00,
                        "multiplier": line.multiplier or 0.00,
                        "cost_unit": cost_unit or 0.00,
                        "total_payment": total_payment or 0.00,
                    },
                    default_format=self.format_tcell_left,
                )
