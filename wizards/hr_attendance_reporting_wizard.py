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
from __future__ import division
import time
import datetime
from openerp.osv import fields, osv
from datetime import date, datetime, timedelta
import openerp.addons.decimal_precision as dp
from mako.template import Template
from openerp import SUPERUSER_ID
import pytz

class hr_attendance_reporting(osv.osv_memory):
	_name = "hr.attendance.reporting"
	_description = "HR  Attendance Report Wizard"
	
	_columns = {
		'attandance_report_id': fields.many2one('ir.actions.report.xml', required=True, string="Report Name", domain=[('model', '=', 'hr.attendance')]),
		'employee_id': fields.many2one('hr.employee', required=True, string="Employee"),
		'date_from': fields.date(string="From", required=True),
		'date_to': fields.date(string="To", required=True),
	}
	
	_defaults={
		'date_to': fields.date.today(),
	}
	
	def action_print(self, cr, uid, ids, context=None):
		res = {}
		for wizard in self.browse(cr, uid, ids, context):
			report_name= wizard.attandance_report_id.report_name
			datas = {
				'ids': self.pool.get('hr.attendance').search(cr, uid, [('employee_id.name','=',wizard.employee_id.name),('name','>=',wizard.date_from),('name','<',wizard.date_to)], order="name",context=context),
				'model': 'hr.attendance',
				'form': self.read(cr, uid, ids, [], context=context)
				}
			res = {
				'type': 'ir.actions.report.xml',
				'report_name': report_name,
				'datas': datas,
				}
		return res