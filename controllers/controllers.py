from odoo import http
from odoo.http import request as req
import json, base64


class FetchJobs(http.Controller):
    @http.route('/dev-jobs', type='http', auth='public', csrf=False, cors='*')
    def fetch_jobs(self):
        dev_jobs = req.env['dev.job'].sudo().search([])

        jobs_list = []

        for job in dev_jobs:
            if job.company_logo:
                image_base64 = base64.b64decode(job.company_logo)
                company_logo = base64.b64encode(image_base64).decode('utf-8')
            jobs_list.append({
                'job_id': job.id,
                'job_title': job.job_title,
                'job_type': job.job_type,
                'company_name': job.company_name,
                'company_logo': company_logo if company_logo else '',
                'country': job.country.name,
            })

        return json.dumps({'code': 200, 'dev_jobs': jobs_list})