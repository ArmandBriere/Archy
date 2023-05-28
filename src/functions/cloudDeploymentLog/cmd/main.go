package main

import (
	cloudDeploymentLog "cloudDeploymentLog.com/cloudfunction"
)

// Function used to perform manual integration testing
func main() {

	payload := cloudDeploymentLog.Payload{
		Timestamp: "2022-06-26T23:45:14.641209Z",
		Severity:  "NOTICE",
		ProtoPayload: cloudDeploymentLog.ProtoPayload{
			MethodName: "google.cloud.functions.v1.CloudFunctionsService.UpdateFunction",
			AuthenticationInfo: cloudDeploymentLog.AuthenticationInfo{
				PrincipalEmail: "manual-test@archy.com",
			},
		},
		Resource: cloudDeploymentLog.Resource{
			Type: "cloud_function",
			Labels: cloudDeploymentLog.Labels{
				FunctionName: "dev_exp",
				Region:       "us-central1",
				ProjectId:    "archy-f06ed",
			},
		},
	}

	err := cloudDeploymentLog.SendErrorLogToDiscordChannel(&payload)
	if err != nil {
		panic(nil)
	}
}
