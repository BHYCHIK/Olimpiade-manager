# This file contains functions that returns jsons replies on incorrect requests
# Copyright Ivan Remen (i.remen@corp.mail.ru) BMSTU 2013

def request_not_json():
	return '{"error_code": 1, "error_text": "Your request is not json"}'

def unknown_api_function():
	return '{"error_code": 2, "error_text": "Unknown api function or no cmd field in request"}'
