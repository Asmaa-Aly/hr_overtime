# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014-2015 Asmaa Aly.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
	'name' : 'Overtime Management',
	'version' : '0.1',
	'author' : 'Asmaa Aly',
	'category' : 'Human Resources',
	'description' : """
		The purpose of this module is to manage Overtime for all employee or for each department through odoo 8 HR Overtime Module as HR new feature. 
		Integrated with Payroll Management 
		Integrated with contract
		Integrated with attendance 

		Created By Asmaa Aly
	""",

	'depends' : ['hr', 'hr_contract','hr_payroll'],
	'data': [
		'sequences/hr_overtime_sequence.xml',
		'datas/hr_payroll_rule.xml',
		'views/hr_overtime_view.xml',
		'reports/report_view.xml',
		'reports/hr_attendance_analysis_report.xml',
		'wizards/views/hr_attendance_report_view.xml',
	],

	'installable': True,
	'auto_install': False,
}

