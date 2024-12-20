=======================
Howto use ESP32 and AWS
=======================

1. Create an account and log to `AWS <https://aws.amazon.com/>`_ (Amazon Web Services).

2. In the **IoT Core** service, go to **Manage > All devices > Things** and click on **Create things**.

    * Create single thing
    * Thing name: `ESP32`
    * No shadow
    * Auto-generate a new certificate
    * Policies: click on **Create policy**
        * Policy names: `esp32-policy`
        * Use Policy examples or create them yourself by clicking on **JSON** and replacing the `region <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html>`_ and account ID with your own:
        ```JSON
        {
        "Version": "2012-10-17",
        "Statement": [
            {
            "Effect": "Allow",
            "Action": "iot:Connect",
            "Resource": "arn:aws:iot:eu-central-1:<account-id>:client/${iot:Connection.Thing.ThingName}"
            },
            {
            "Effect": "Allow",
            "Action": "iot:Publish",
            "Resource": "arn:aws:iot:eu-central-1:<account-id>:topic/${iot:Connection.Thing.ThingName}*"
            }
        ]
        }
        ```
        * Click on **Create**
        * Select your policy name and click on **Create thing**
        * **Important:** Download the `Public key file`, `Private key file`, and `Amazon Root CA certificate`
    