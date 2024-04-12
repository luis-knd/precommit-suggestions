import json
import logging
import os

import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException


class JiraAPI:
    """
    Represents the JiraAPI class for interacting with Jira.

    Attributes:
        base_url (str): The base url of the Jira instance.
        auth (requests.auth.HTTPBasicAuth): The HTTP Basic Authentication object.

    """

    def __init__(self):
        """
        Initializes a new instance of the JiraAPI class.
        """
        self.base_url = os.getenv("JIRA_URL")
        self.auth = HTTPBasicAuth(os.getenv("JIRA_USER"), os.getenv("JIRA_API_TOKEN"))

    def comment_issue(self, issue_key, comment_text, file_name=None):
        """
        Adds a comment to a Jira issue.

        Args:
            issue_key (str): The key of the Jira issue.
            comment_text (str): The text of the comment.
            file_name (str, optional): The name of the file to reference in the comment.

        Returns:
            str: A message indicating the success or failure of the operation.
        """
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

            response = requests.post(endpoint, data=comment_data, headers=headers, auth=self.auth)

            response.raise_for_status()
            logging.info("comment added successfully.")
        except RequestException as e:
            logging.error(f"an error occurred when commenting on Jira: {e}")
            return str(f"an error occurred: {e}")
        except Exception as e:
            logging.error(f"an unexpected error occurred to commenting on the jira: {e}")
            return str(f"an unexpected error ocurred: {e}")

    def add_attachments_issue(self, issue_key, attachment_path=None):
        """
        Adds attachments to a Jira issue.

        Args:
            issue_key (str): The key of the Jira issue.
            attachment_path (str): The path to the file to be attached.

        Returns:
            str: A message indicating the success or failure of the operation.
        """
        try:
            logging.info("uploading CR suggestion file to Jira")
            endpoint = f"{self.base_url}/rest/api/2/issue/{issue_key}/attachments"
            headers = {
                "Accept": "application/json",
                "X-Atlassian-Token": "no-check"
            }

            response = requests.post(endpoint, headers=headers, auth=self.auth, files={
                "file": (attachment_path, open(attachment_path, "rb"), "application-type")
            })

            response.raise_for_status()
            logging.info("file added successfully.")
        except RequestException as e:
            logging.error(f"an error occurred when uploading a file to Jira: {e}")
            return str(f"An error occurred: {e}")
        except Exception as e:
            logging.error(f"an unexpected error occurred when uploading file on the jira: {e}")
            return str(f"an unexpected error ocurred: {e}")
