package main

import (
	cloudErrorLog "cloudErrorLog.com/cloudfunction"
)

// Function used to perform manual integration testing
func main() {

	payload := cloudErrorLog.Payload{
		TextPayload: "Traceback (most recent call last):\n  File \"/layers/google.python.pip/pip/lib/python3.9/site-packages/flask/app.py\", line 2077, in wsgi_app\n    response = self.full_dispatch_request()\n  File \"/layers/google.python.pip/pip/lib/python3.9/site-packages/flask/app.py\", line 1525, in full_dispatch_request\n    rv = self.handle_user_exception(e)\n  File \"/layers/google.python.pip/pip/lib/python3.9/site-packages/flask/app.py\", line 1523, in full_dispatch_request\n    rv = self.dispatch_request()\n  File \"/layers/google.python.pip/pip/lib/python3.9/site-packages/flask/app.py\", line 1509, in dispatch_request\n    return self.ensure_sync(self.view_functions[rule.endpoint])(**req.view_args)\n  File \"/layers/google.python.pip/pip/lib/python3.9/site-packages/functions_framework/__init__.py\", line 99, in view_func\n    return function(request._get_current_object())\n  File \"/layers/google.python.pip/pip/lib/python3.9/site-packages/functions_framework/__init__.py\", line 80, in wrapper\n    return func(*args, **kwargs)\n  File \"/workspace/main.py\", line 51, in exp\n    last_message_timestamp: str = doc.get(\"last_message_timestamp\")\n  File \"/layers/google.python.pip/pip/lib/python3.9/site-packages/google/cloud/firestore_v1/base_document.py\", line 475, in get\n    nested_data = field_path_module.get_nested_value(field_path, self._data)\n  File \"/layers/google.python.pip/pip/lib/python3.9/site-packages/google/cloud/firestore_v1/field_path.py\", line 239, in get_nested_value\n    raise KeyError(msg)\nKeyError: \"'last_message_timestamp' is not contained in the data\"",
		Timestamp:   "2022-06-26T23:45:14.641209Z",
		Severity:    "ERROR",
	}

	payload.Resource.Type = "cloud_function"
	payload.Resource.Labels.FunctionName = "exp"
	payload.Resource.Labels.Region = "us-central1"
	payload.Resource.Labels.ProjectId = "archy-f06ed"

	cloudErrorLog.SendErrorLogToDiscordChannel(&payload)
}
