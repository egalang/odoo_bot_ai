# Odoo Bot AI Integration Module

This Odoo module integrates with an external AI service to provide chatbot functionality within Odoo's Discuss application and allows for PDF document uploads for AI knowledge enrichment.

## Features

* **Ask AI Command (`/ask_ai`):** Allows users in Discuss channels to query an external AI service directly.
    * Users can type `/ask_ai [your question]` in a channel.
    * The module sends the query to a configured AI API.
    * The AI's response is then posted back in the Discuss channel.
  
* **PDF Document Upload for AI:** Enables User to upload PDF documents to Odoo, which can then be processed by the external AI service to enhance its knowledge base.
    * A new model `pdf.uploads` is introduced to manage uploaded PDF files.
    * User can upload PDF files with associated names.
    * The module automatically sends the uploaded PDF content to the configured AI API for processing.
    * Tracks the upload status (Pending, Success, Failed).
    * Allows deleting uploaded PDFs, which also triggers a request to the AI API to remove associated vector data.
  
* **Configuration:** Provides a settings screen to configure the connection to the external AI API.
    * Allows setting the API URL.
    * Ensures only one AI configuration can be active at a time.
    * Enables/disables the PDF upload feature.

## Installation

1.  Place the module directory (e.g., `odoo_bot_ai`) in your Odoo addons path.
2.  Update your Odoo modules list.
3.  Install the "Odoo Bot AI Integration" module.

## Configuration

1.  Go to **Settings > General Settings**.
2.  Find the **Odoo Bot AI** section in the **DISCUSS**.
3.  Click on **Manage Odoo Bot AI Configuration** to access the configuration settings.
4.  **Create a new configuration** or edit an existing one.
5.  **Configuration Name:** Give the configuration a descriptive name.
6.  **API URL:** Enter the URL of your external AI service API. Ensure it includes the protocol (e.g., `http://` or `https://`). The default is `http://host.docker.internal:8000/`.
7.  **In Use:** Select this checkbox to make this configuration the active one. Only one configuration can be active at a time.
8.  Save the configuration.

## Usage

### Asking AI in Discuss Channels

1.  Open any Discuss channel in Odoo.
2.  Type `/ask_ai` followed by your question. For example: `/ask_ai What is the Appraisal Module?`
3.  Press Enter.
4.  The module will send your question to the configured AI service.
5.  The AI's response will be posted in the Discuss channel as a new message from the system bot (typically OdooBot).


### Uploading PDF Documents

1.  Ensure the "Enable PDF Upload" setting is checked in the Odoo Bot AI configuration.
1.  Go to **Settings > General Settings**.
2.  Find the **Odoo Bot AI** section in the **DISCUSS**.
3.  Click on **Manage Odoo Bot AI Configuration** to access the configuration settings.
4.  Upon opening Select a configuration you want to upload the following pdf(s)
5.  Click on **Add a line** to upload a new PDF document.
6.  **PDF File:** Upload the PDF file using the file selector.
7.  The module will automatically upload the PDF content to the configured AI API.
8.  The **Status** field will indicate the upload status:
    * **Pending:** The upload is in progress.
    * **Success:** The upload was successful.
    * **Failed:** The upload failed.
9.  You can view and manage the uploaded PDF documents in this section.
10.  Deleting a PDF record will also attempt to remove the associated vector data from the AI service.

## Technical Details

* **Dependencies:** This module relies on the standard Odoo `discuss` module.
* **External API Communication:** The module uses the `requests` library to communicate with the external AI service API. Ensure this library is installed in your Odoo environment.
* **PDF Handling:** The module reads the content of uploaded PDF files and sends it to the AI API for processing. The specific processing of the PDF content is handled by the external AI service.
* **PDF Upload Storage:** Uploaded PDF file data is stored as a binary field in the `pdf.uploads` model.

## Troubleshooting

* **Ensure the AI API is running and accessible:** Check if the API URL is correct and if the external AI service is running.
* **Check Odoo logs:** Look for any error messages in the Odoo logs related to the module or API communication.
* **Verify API endpoint:** Make sure the API endpoints (`/query/` for `/ask_ai` and `/upload_pdf/` for PDF uploads, `/vectors` for delete) are correct and the AI service is listening on those endpoints.
* **Network connectivity:** Ensure that the Odoo server can communicate with the external AI service.
* **PDF Upload Failures:** Check the Odoo logs for details on why a PDF upload might have failed. This could be due to network issues, API errors, or incorrect file formats.

