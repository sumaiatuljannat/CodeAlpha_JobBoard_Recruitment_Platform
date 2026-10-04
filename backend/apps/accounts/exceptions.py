from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        custom_data = {
            'success': False,
            'status_code': response.status_code,
            'message': 'An error occurred during request processing.',
            'error_code': 'VALIDATION_ERROR' if response.status_code == 400 else 'ERROR',
            'errors': response.data
        }
        
        # If response.data has 'detail', use it as the main message
        if isinstance(response.data, dict) and 'detail' in response.data:
            custom_data['message'] = str(response.data['detail'])
            if response.status_code == 401:
                custom_data['error_code'] = 'AUTHENTICATION_REQUIRED'
            elif response.status_code == 403:
                custom_data['error_code'] = 'PERMISSION_DENIED'
            elif response.status_code == 404:
                custom_data['error_code'] = 'NOT_FOUND'

        response.data = custom_data

    return response
