from django.views import generic
from django.shortcuts import render
from contactlist.odoo_client import OdooClient

def employee_detail(request, pk):
    odoo_client = OdooClient()

    # proj_ids = odoo_client.models.execute_kw(
    #             odoo_client.db,
    #             odoo_client.uid,
    #             odoo_client.password,
    #             'project.project', 
    #             'search', 
    #             [[['active', '=', True]]]
    #         )
    
    # projects = odoo_client.models.execute_kw(
    #             odoo_client.db,
    #             odoo_client.uid,
    #             odoo_client.password,
    #             'project.project',
    #             'read',
    #             [proj_ids],
    #             {'fields': ['id', 'name', 'partner_id', 'company_id']}
    #         )

    # projects = odoo_client.models.execute_kw(
    #             odoo_client.db,
    #             odoo_client.uid,
    #             odoo_client.password,
    #             'project.project',
    #             'read',
    #             [18],
    #             {'fields': ['id', 'name', 'partner_id', 'company_id', 'timesheet_ids']}
    #         )

    ts_ids = odoo_client.models.execute_kw(
                odoo_client.db,
                odoo_client.uid,
                odoo_client.password,
                'account.analytic.line', 
                'search', 
                [[['employee_id', '=', pk], 
                  ['date', '>', '2025-01-01'],
                  ['date', '<', '2025-02-01']]]
            )

    ts_records = odoo_client.models.execute_kw(
                odoo_client.db,
                odoo_client.uid,
                odoo_client.password,
                'account.analytic.line',
                'read',
                [ts_ids],
                {'fields': ['id', 'name', 'date', 'unit_amount', 
                            'employee_id', 'project_id']}
            )

    for ts in ts_records:
        ts.setdefault('project', ts['project_id'][1])
        ts['project_id'] = ts['project_id'][0]
    
    return render(request, 'employee_details.html', {'data': ts_records})



class EmployeeListView(generic.View):
    """
    View to fetch a list of active employees from Odoo and render a template.
    """
    def get(self, request, *args, **kwargs):
        # try:
        # Initialize Odoo client
        odoo_client = OdooClient()
        print("Logged in")
        # Fetch active employees
        employee_ids = odoo_client.models.execute_kw(
            odoo_client.db,
            odoo_client.uid,
            odoo_client.password,
            'hr.employee', 
            'search', 
            [[['active', '=', True]]]
        )
        print(employee_ids)
        # Fetch detailed employee records
        employees = odoo_client.models.execute_kw(
            odoo_client.db,
            odoo_client.uid,
            odoo_client.password,
            'hr.employee',
            'read',
            [employee_ids],
            {'fields': ['id', 'name', 'work_phone', 'work_email']}
            # {'fields': ['id', 'name', 'avatar_256', 'work_phone', 'work_email']}
        )

        # Render the template with the employee data
        return render(request, 'employee.html', {'employees': employees})
        # except Exception as e:
        #     # Handle the error and render an error template or message
        #     return render(request, 'error_template.html', {'error': f"An error occurred while fetching employees: {str(e)}"})