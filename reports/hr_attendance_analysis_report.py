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
from datetime import datetime ,date, timedelta 
from openerp.osv import osv, fields
from openerp.report import report_sxw
import pytz
from openerp import SUPERUSER_ID

class ParticularReport(osv.AbstractModel):
	_name = 'report.hr_overtime.hr_attendance_analysis'


	def _get_day(self, date):
		day_name = str(datetime.strptime(str(date),"%Y-%m-%d").weekday())
		if day_name == "0":
			day_name = "Monday"
		if day_name == "1":
			day_name = "Tuesday"
		if day_name == "2":
			day_name ="Wednesday"
		if day_name == "3":
			day_name = "Thursday"
		if day_name == "4":
			day_name = "Friday"
		if day_name == "5":
			day_name = "Saturday"
		if day_name == "6":
			day_name = "Sunday"
		return day_name
		
	def _get_index_day(self, date):
		day_name = str(datetime.strptime(str(date),"%Y-%m-%d").weekday())
		return day_name
		
	def _get_month(self, date):
		if date:
			return datetime.strptime(date,"%Y-%m-%d").month
		return 0
		
	def _get_year(self, date):
		if date:
			return datetime.strptime(date,"%Y-%m-%d").year
		return 0
			
			
	def _get_time_from_float(self, float_type):
		str_off_time = str(float_type)
		official_hour = str_off_time.split('.')[0]
		official_minute = ("%2d" % int(str(float("0." + str_off_time.split('.')[1]) * 60).split('.')[0])).replace(' ','0')
		str_off_time = official_hour + ":" + official_minute
		str_off_time = datetime.strptime(str_off_time,"%H:%M").time()
		return str_off_time
		
	def _get_float_from_time(self,time_type):
		signOnP = [int(n) for n in time_type.split(":")]
		signOnH = signOnP[0] + signOnP[1]/60.0
		return signOnH
		
		

	def render_html(self, cr, uid, ids, data=None, context=None):
		report_obj = self.pool['report']
		report = report_obj._get_report_from_name(
			cr, uid, 'hr_overtime.hr_attendance_analysis'
		)
		from_date_x = self.pool.get('hr.attendance.reporting').browse(cr, uid, context.get('active_id'), context=context).date_from
		to_date_x = self.pool.get('hr.attendance.reporting').browse(cr, uid, context.get('active_id'), context=context).date_to
		
		from_date = datetime.strptime(from_date_x, "%Y-%m-%d")
		to_date = datetime.strptime(to_date_x, "%Y-%m-%d")
		
		day = timedelta(days=1)
		all_dates = [(from_date + timedelta(days=x)).date() for x in range((to_date- from_date).days + 1)]
		
		user_pool = self.pool.get('res.users')
		user = user_pool.browse(cr, SUPERUSER_ID, uid)
		tz = pytz.timezone(user.partner_id.tz) or False
		
		def _get_sign_in_date(docs , date):
			attendance_time = "Not Found"
			for object in docs:
				if object.action == 'sign_in':
					att_date = datetime.strptime(object.name,"%Y-%m-%d %H:%M:%S").date()
					if date == att_date:
						attendance_datetime = object.name
						attendance_time = pytz.utc.localize(datetime.strptime(attendance_datetime,"%Y-%m-%d %H:%M:%S")).astimezone(tz)
						attendance_time = attendance_time.time()
						return attendance_time
						break
			return attendance_time
		
		def _get_sign_out_date(docs , date):
			attendance_time = "Not Found"
			for object in docs:
				if object.action == 'sign_out':
					att_date = datetime.strptime(object.name,"%Y-%m-%d %H:%M:%S").date()
					if date == att_date:
						attendance_datetime = object.name
						attendance_time = pytz.utc.localize(datetime.strptime(attendance_datetime,"%Y-%m-%d %H:%M:%S")).astimezone(tz)
						attendance_time = attendance_time.time()
						return attendance_time
						break
			return attendance_time
		
		
		
		def _get_leave(docs,date):
			leave_name =" "
			leave_obj = self.pool.get('hr.holidays')
			for object in docs:
				employee_id = object.employee_id.id
				break
			leave_ids = leave_obj.search(cr, uid, [
				('employee_id','=', employee_id),
				('state','=','validate')], context=context)
			if leave_ids:
				for leave in leave_obj.browse(cr, uid, leave_ids, context=context):
					leave_date_from = datetime.strptime(leave.date_from,"%Y-%m-%d %H:%M:%S").date()
					leave_date_to = datetime.strptime(leave.date_to,"%Y-%m-%d %H:%M:%S").date()
					if leave_date_from <= date and leave_date_to >= date:
						leave_name = leave.name
			return leave_name
			
			
		def _get_diff_time(docs,sign_in_time,date):
			FMT = '%H:%M:%S'
			tdelta = timedelta(hours=00, minutes=00, seconds=00)
			if sign_in_time == "Not Found":
				return tdelta
			else:
				for object in docs:
					employee_id = object.employee_id.id
					break
				employee = self.pool.get('hr.employee').browse(cr, uid, employee_id, context=context)
				for wk in employee.contract_id.working_hours.attendance_ids:
					if wk.dayofweek == self._get_index_day(date):
						working_time = self._get_time_from_float(wk.hour_from)
						tdelta = datetime.strptime(str(sign_in_time), FMT) - datetime.strptime(str(working_time), FMT)
						if tdelta < timedelta(hours=00, minutes=00, seconds=00):
							return ""
						return tdelta
						
						
		def get_end_hour_of_the_day(date_in, working_hours_id):
			hour = 0.0
			if type(date_in) is datetime:
				working_hours = self.pool.get('resource.calendar').browse(cr, uid, working_hours_id, context=context)
				for line in working_hours.attendance_ids:
					# First assign to hour
					if int(line.dayofweek) == date_in.weekday() and hour == 0.0:
						hour = line.hour_to
					# Other assignments to hour
					# No need for this part but it's a fail safe condition
					elif int(line.dayofweek) == date_in.weekday() and hour != 0.0 and line.hour_from < hour:
						hour = line.hour_to
			return hour
						
						
		def _get_overtime(docs,date):
			for object in docs:
				employee_id = object.employee_id.id
				break
			employee = self.pool.get('hr.employee').browse(cr, uid, employee_id, context=context)
			day_ids = []
			for day in employee.contract_id.working_hours.attendance_ids:
				day_ids.append(day.dayofweek)
			
			val_overtime=""
			sign_in_date = ""
			sign_in_attendance_time = timedelta(hours=00, minutes=00, seconds=00)
			sign_out_date = ""
			sign_out_attendance_time = timedelta(hours=00, minutes=00, seconds=00)
	
			for object in docs:
				att_date = pytz.utc.localize(datetime.strptime(object.name,"%Y-%m-%d %H:%M:%S")).astimezone(tz)
				if att_date.date() == date:
					hour_to = get_end_hour_of_the_day(att_date, employee.contract_id.working_hours.id)
					hour_to_time = self._get_time_from_float(hour_to)
										
					if employee.contract_id.overtime_structure_id.overtime_method == 'ov_attendance':
						# get Official Leave 
						holiday_status_id = self.pool.get('hr.holidays.status').search(cr, uid, [('name','=','Official Leave')], context=context)[0]
						domain =[
							('employee_id','=',object.employee_id.id),
							('holiday_status_id','=',holiday_status_id)
						]
						leave_ids = self.pool.get('hr.holidays').search(cr, uid, domain, context=context)
						Flage = False
						for leave in self.pool.get('hr.holidays').browse(cr, uid, leave_ids, context=context):
							to_dt= datetime.strptime(leave.date_to, "%Y-%m-%d %H:%M:%S").date()
							from_dt= datetime.strptime(leave.date_from, "%Y-%m-%d %H:%M:%S").date()
							for n in range(((to_dt+timedelta(days=1)) - from_dt).days):
								if att_date.date() == from_dt:
									Flage = True
								from_dt += timedelta(days=1)
								
						for rule in employee.contract_id.overtime_structure_id.hr_ov_structure_rule_ids:
							
							# First condition overtime in Working Day 
							if self._get_index_day(att_date.date()) in day_ids:
								if Flage == False:
									if rule.type == 'working_day' and object.action == 'sign_out':
										start_overtime = hour_to + rule.begin_after
										start_overtime_time = self._get_time_from_float(start_overtime)
										start_overtime = tz.localize(datetime.combine(att_date.date(), start_overtime_time))
										if start_overtime > att_date:
											continue 
										diff_time = att_date - start_overtime
										val_overtime = self._get_float_from_time(str(diff_time)) * rule.rate
										val_overtime = self._get_time_from_float(val_overtime)
										return val_overtime
								else:
									if rule.type == 'official_leave':
										if object.action == 'sign_in':
											sign_in_date = att_date.date()
											sign_in_attendance_time = att_date
										
										elif object.action == 'sign_out':
											sign_out_date = att_date.date()
											sign_out_attendance_time = att_date
										
										if sign_in_date == sign_out_date:
											diff_time = sign_out_attendance_time - sign_in_attendance_time
											val_overtime = self._get_float_from_time(str(diff_time)) * rule.rate
											val_overtime = self._get_time_from_float(val_overtime)
											return val_overtime
							else:
								if rule.type == 'weekend':
									if object.action == 'sign_in':
										sign_in_date = att_date.date()
										sign_in_attendance_time = att_date
									
									elif object.action == 'sign_out':
										sign_out_date = att_date.date()
										sign_out_attendance_time = att_date
									
									if sign_in_date == sign_out_date:
										diff_time = sign_out_attendance_time - sign_in_attendance_time
										val_overtime = self._get_float_from_time(str(diff_time)) * rule.rate
										val_overtime = self._get_time_from_float(val_overtime)
										return val_overtime
		
					else:
				
						for rule in employee.contract_id.overtime_structure_id.hr_ov_structure_rule_ids:
							ov_ids = self.pool.get('hr.overtime').search(cr, uid, [('employee_id','=',employee.id),('state','=','approve')], context=context)
							for overtime in self.pool.get('hr.overtime').browse(cr, uid, ov_ids, context=context):
								ov_date = pytz.utc.localize(datetime.strptime(overtime.from_date,"%Y-%m-%d %H:%M:%S")).astimezone(tz)
								if rule.type == overtime.type:
									if att_date.date() == ov_date.date() == date:
										val_overtime = overtime.total_time * rule.rate
										val_overtime = self._get_time_from_float(val_overtime)
										return val_overtime
		
		docargs = {
			'doc_ids': ids,
			'doc_model': report.model,
			'docs': self.pool[report.model].browse(cr, uid, ids, context=context),
			'print_date': fields.datetime.now,
			'from_date': from_date_x,
			'to_date': to_date_x,
			'dates': all_dates,
			'get_day': self._get_day,
			'get_sign_in_date': _get_sign_in_date,
			'get_sign_out_date': _get_sign_out_date,
			'get_leave':_get_leave,
			'get_month': self._get_month,
			'get_year': self._get_year,
			'get_diff_time': _get_diff_time,
			'get_overtime': _get_overtime,
			
		}
		return report_obj.render(cr, uid, ids, 'hr_overtime.hr_attendance_analysis', docargs, context=context)