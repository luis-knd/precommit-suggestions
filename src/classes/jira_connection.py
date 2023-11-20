import json
import logging
import os
from http import HTTPStatus

import requests
from requests.auth import HTTPBasicAuth


class JiraAPI:

    def __init__(self):
        self.base_url = os.getenv("JIRA_URL")
        self.auth = HTTPBasicAuth(os.getenv("JIRA_USER"), os.getenv("JIRA_API_TOKEN"))

    def comment_issue(self, issue_key, comment_text, file_name=None):
        try:
            logging.info("creating comment in jira to give visibility to the CR suggestion")
            endpoint = f"{self.base_url}/rest/api/2/issue/{issue_key}/comment"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "X-Atlassian-Token": "no-check"
            }

            comment_data = json.dumps({
                "body": f"{comment_text} [^{file_name}]"
            })

            response = requests.request("POST", endpoint, data=comment_data, headers=headers,
                                        auth=self.auth)

            if response.status_code == HTTPStatus.CREATED:
                logging.info("comment added successfully.")
            else:
                logging.error(f"failed to add comment. Status code: {response.status_code}")
                logging.error(response.text)
        except Exception as e:
            logging.error(f"an error occurred to commenting on the jira: {e}")
            return str(f"an error ocurred: {e}")

    def add_attachments_issue(self, issue_key, attachment_path=None):
        try:
            logging.info("uploading CR suggestion file to Jira")
            endpoint = f"{self.base_url}/rest/api/2/issue/{issue_key}/attachments"
            headers = {
                "Accept": "application/json",
                "X-Atlassian-Token": "no-check"
            }

            response = requests.request("POST", endpoint, headers=headers, auth=self.auth, files={
                "file": (attachment_path, open(attachment_path, "rb"), "application-type")
            })

            if response.status_code == HTTPStatus.OK:
                logging.info("file added successfully.")
            else:
                logging.error(f"failed to upload file. Status code: {response.status_code}")
                logging.error(response.text)
        except Exception as e:
            logging.error(f"an error occurred when uploading file on the jira: {e}")
            return str(f"an error ocurred: {e}")
