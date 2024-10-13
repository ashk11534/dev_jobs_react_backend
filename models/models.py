from odoo import fields, models, api


class DevJob(models.Model):
    _name = 'dev.job'
    _description = 'dev.job'
    _rec_name = 'job_title'
    _order = 'id desc'

    job_title = fields.Char(string='Job title')
    job_type = fields.Selection([
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time')
    ], string='Job type')
    company_name = fields.Char(string='Company name')
    company_logo = fields.Image(string='Company logo')
    country = fields.Many2one('res.country', string='Country')
