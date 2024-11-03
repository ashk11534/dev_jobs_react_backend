from odoo import http
from odoo.http import request as req
import json, base64
from bs4 import BeautifulSoup
from odoo import models, api
import cx_Oracle

class FetchJobs(http.Controller):

    @http.route('/dev-jobs', type='http', methods=['GET', 'OPTIONS'], auth='none', cors='*')
    def fetch_jobs(self):
        dev_jobs = req.env['dev.job'].sudo().search([])

        jobs_list = []

        for job in dev_jobs:
            if job.company_logo:
                image_base64 = base64.b64decode(job.company_logo)
                company_logo = base64.b64encode(image_base64).decode('utf-8')
            jobs_list.append({
                'job_id': job.id,
                'created_date': job.format_created_date(),
                'job_title': job.job_title,
                'job_type': job.job_type,
                'company_name': job.company_name,
                'company_logo': company_logo if company_logo else '',
                'country': job.country.name,
            })

        return req.make_response(json.dumps({'code': 200, 'dev_jobs': jobs_list}), headers=[
            ('Content-Type', 'application/json'),
            ('Access-Control-Allow-Methods', 'GET, OPTIONS'),
        ])

    @http.route('/job-details/<int:job_id>', type='http', methods=['GET', 'OPTIONS'], auth='none', cors='*')
    def job_details(self, job_id):
        job_obj = req.env['dev.job'].sudo().search([('id', '=', job_id)])

        if job_obj.company_logo:
            image_base64 = base64.b64decode(job_obj.company_logo)
            company_logo = base64.b64encode(image_base64).decode('utf-8')

        job_data = {
            'job_title': job_obj.job_title,
            'created_date': job_obj.format_created_date(),
            'job_type': job_obj.job_type,
            'job_description': BeautifulSoup(job_obj.job_description, 'html.parser').get_text() if job_obj.job_description else '',
            'company_name': job_obj.company_name,
            'company_logo': company_logo if company_logo else '',
            'company_website_url': job_obj.company_website_url,
            'country': job_obj.country.name
        }

        return req.make_response(json.dumps({'code': 200, 'job_data': job_data}), headers=[
            ('Content-Type', 'application/json'),
            ('Access-Control-Allow-Methods', 'GET, OPTIONS')
        ])

    @http.route('/job-application', type='http', methods=['POST', 'OPTIONS'], auth='none', csrf=False, cors='*')
    def submit_application(self, **kwargs):
        form_data = req.httprequest.form
        email = form_data.get('email').strip() if form_data.get('email') else ''
        cover_letter = form_data.get('coverLetter').strip() if form_data.get('coverLetter') else ''
        resume = base64.b64encode(req.httprequest.files.get('resume').read()) if req.httprequest.files.get('resume') else None
        job_id = int(form_data.get('jobId')) if form_data.get('jobId') else None

        req.env['job.application'].sudo().create({
            'email': email,
            'cover_letter': cover_letter,
            'resume': resume,
            'job_id': job_id
        })

        return req.make_response(json.dumps({'code': 200}), headers=[
            ('Content-Type', 'application/json'),
            ('Access-Control-Allow-Methods', 'POST, OPTIONS')
        ])

    @http.route('/job-search', type='http', methods=['POST', 'OPTIONS'], auth='none', csrf=False, cors='*')
    def search_job(self, **kwargs):
        form_data = req.httprequest.form

        print(form_data)

        title = form_data.get('title').strip() if form_data.get('title') else None
        location = form_data.get('location').strip() if form_data.get('location') else None
        fullTime = 'full_time' if form_data.get('fullTime') == 'true' else None

        query_list = ['|']

        if title:
            query_list.append(('job_title', 'ilike', title))
            query_list.append(('company_name', 'ilike', title))

        if location:
            query_list.append(('country.name', 'ilike', location))

        if fullTime:
            query_list.append(('job_type', '=', fullTime))

        if (len(query_list) == 1 or len(query_list) == 2 or len(query_list) == 3) and not title:
            query_list.remove('|')

        dev_jobs = req.env['dev.job'].sudo().search(query_list)

        jobs_list = []

        for job in dev_jobs:
            if job.company_logo:
                image_base64 = base64.b64decode(job.company_logo)
                company_logo = base64.b64encode(image_base64).decode('utf-8')
            jobs_list.append({
                'job_id': job.id,
                'created_date': job.format_created_date(),
                'job_title': job.job_title,
                'job_type': job.job_type,
                'company_name': job.company_name,
                'company_logo': company_logo if company_logo else '',
                'country': job.country.name,
            })

        print(title, location, fullTime)

        return req.make_response(json.dumps({'code': 200, 'dev_jobs': jobs_list}), headers=[
            ('Content-Type', 'application/json'),
            ('Access-Control-Allow-Methods', 'POST, OPTIONS')
        ])

def connect_to_oracle():
    dsn = cx_Oracle.makedsn('localhost', '1521', sid='XE')
    user = 'ashik'
    password = 'root'

    connection = cx_Oracle.connect(user, password, dsn)
    cursor = connection.cursor()

    return connection, cursor


class OracleConnector(http.Controller):
    @http.route('/retrieve-data-from-oracle', type='http', auth='public')
    def retrieve_data_from_oracle(self):

        connection = cursor = None

        try:
            connection, cursor = connect_to_oracle()

            cursor.execute("SELECT * FROM EMP")
            rows = cursor.fetchall()

            for row in rows:
                # Perform desired operations with Odoo models or data processing here
                print(row[0], row[1])

        except cx_Oracle.DatabaseError as e:
            print("There was an error connecting to the Oracle database:", e)

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @http.route('/create-a-new-table', type='http', auth='public')
    def create_a_new_table(self):

        connection = cursor = None

        try:
            connection, cursor = connect_to_oracle()

            cursor.execute("""CREATE TABLE student (
                student_id NUMBER(10) PRIMARY KEY,
                name VARCHAR2(50),
                age NUMBER(3)
            )""")

        except cx_Oracle.DatabaseError as e:
            print('There was an error connecting to the oracle database', e)

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @http.route('/insert-data-into-student-table', type='http', auth='public')
    def insert_data_into_student_table(self):

        connection = cursor = None

        try:
            connection, cursor = connect_to_oracle()

            cursor.execute("""INSERT INTO student 
            (student_id, name, age)
            VALUES (2, 'Joy', 26)
            """)

            connection.commit()

        except cx_Oracle.DatabaseError as e:
            print('There was an error connecting to the Oracle database', e)

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    @http.route('/delete-from-table', type='http', auth='public')
    def delete_from_table(self):
        connection = cursor = None

        try:
            connection, cursor = connect_to_oracle()

            cursor.execute("""DELETE FROM student WHERE student_id=1""")

            connection.commit()

        except cx_Oracle.DatabaseError as e:
            print('There was an error connecting to the Oracle database', e)

        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()


    @http.route('/update-a-record', type='http', auth='public')
    def update_a_record(self):
        connection = cursor = None

        try:
            connection, cursor = connect_to_oracle()

            cursor.execute("""UPDATE student SET name='Shamiul', age=29 WHERE student_id=2""")

            connection.commit()

        except cx_Oracle.DatabaseError as e:
            print('There was an error connecting to the Oracle database', e)

        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()



