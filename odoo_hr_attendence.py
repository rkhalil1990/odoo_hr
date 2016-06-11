from openerp import models, fields, api

class odooAttendenceInherit(models.Model):
    _inherit ="hr.attendance"

    @api.depends('action', 'time', 'start_time')
    def _late_compute(self):
        for record in self:
            if record.action == 'sign_in':
                record.late = record.time - record.start_time
        return True

    @api.depends('action', 'time', 'end_time')
    def _overtime_compute(self):
        for record in self:
            if record.action == 'sign_out':
                record.overtime = record.time - record.end_time - 2
            if record.overtime < 0:
                record.overtime = 0
        return True

    @api.model
    def create(self, values):
        contacts1 = self.env['hr.employee'].search([('id','=',values['employee_id'])])
        contract = self.env['hr.contract'].search([('employee_id','=',values['employee_id'])])
        values['image']=contacts1.image
        values['start_time']=contract.working_from
        values['end_time']=contract.working_to
        return super(odooAttendenceInherit,self).create(values)

    @api.multi
    def write(self, values):
        contacts1 = self.env['hr.employee'].search([('id','=',values['employee_id'])])
        contract = self.env['hr.contract'].search([('employee_id','=',values['employee_id'])])
        values['image']=contacts1.image
        values['start_time']=contract.working_from
        values['end_time']=contract.working_to
        return super(odooAttendenceInherit,self).write(values)


    image=fields.Binary()
    time=fields.Float(string="time", required=True)
    late=fields.Float(compute=_late_compute, store=True)
    overtime=fields.Float(compute=_overtime_compute, store=True)
    start_time=fields.Float(string="start_time")
    end_time=fields.Float(string="end_time")









