# Installation 
- Clone the Repository
`git clone https://github.com/cgmonali/reviewExtractor`

- Navigate to project directory.
`cd reviewExtractor`

- Setup virtual environment

```bash
python3 -m venv env #Create virtual environment 
source env/bin/activate #Activate virtual environment 
```


- Install django,playwright and dependencies
```bash
  pip install django
  pip install playwright
  playwright install
  pip install beautifulsoup4
  ```

## **API Documentation: Endpoint**

### 1. URL Input Endpoint: /enter-url/

- **Description:**
This endpoint allows users to submit a product page URL from which reviews will be extracted. 
The user will be provided with a user interface (UI) to enter the URL of the desired product page.
<img width="1436" alt="Screenshot 2024-10-13 at 4 17 27 PM" src="https://github.com/user-attachments/assets/37487ffd-6a44-4fa1-8e9c-a1730f8e95ad">

- **Expected Response:**
Upon submitting the URL, the system will process the input and return the reviews found on the specified product page.
<img width="1435" alt="Screenshot 2024-10-13 at 4 40 46 PM" src="https://github.com/user-attachments/assets/9f9faefd-b4bc-4542-9ea2-560b35437d74">

- **Example Workflow:**
  - Navigate to the URL: http://127.0.0.1:8003/enter-url/.

  - Input Example URL: Enter <https://www.amazon.in/One94Store-Serial-String-Christmas-Decoration/dp/B0DC7V55RM?pd_rd_w=zLvsd&reviewerType=all_reviews&pageNumber=1>
  - Receive Output: After processing, one will receive the extracted reviews of the product.
 
### 2. Review Extraction Endpoint: /api/reviews/?page={url}
- **Description:**
This endpoint retrieves raw JSON data containing reviews for a specified product page URL.
Users can provide the URL of the product page in the query parameter to fetch the corresponding reviews.
<img width="1440" alt="Screenshot 2024-10-13 at 4 49 32 PM" src="https://github.com/user-attachments/assets/7eaf19a9-a3f0-4f87-86c6-bd6392d39c08">

# Solution Approach

## Technologies Used
- **Backend**:python,django
- **Frontend**:HTML,CSS,JS

## Backend

- **Using Playwright for Web Scraping**
Playwright to launch a headless browser:
This allows the server to access the full content of the page, including dynamically loaded content.
- **Parsing HTML Content**
The HTML content is parsed using BeautifulSoup to find all review elements:
- **Handling Pagination**
The script iterates through the pagination by incrementing the page number until no more reviews are found.
This ensures that all available reviews are retrieved.
- **Structuring JSON Response**
After collecting all reviews, the function creates a structured JSON response 

## Frontend

- **Form Submission**:
A form allows users to input a product URL.
Upon submission, JavaScript captures the input and sends it to the server via an AJAX POST request.

- **Dynamic Content Rendering**:
After receiving the JSON response, the script dynamically updates the DOM to display total reviews and
individual review details, including title, rating, date, and content.

- **Pagination**:
The reviews are paginated to improve readability. Users can navigate through the pages using Previous and Next 
buttons, with the script calculating which reviews to display based on the current page.

## **Workflow**
```
Start
  |
User Enters URL
  |
Submit Form
  |
Send AJAX Request to Django Server
  |
Extract Product Reviews using Playwright & BeautifulSoup
  |
Format Data as JSON and Return Response to Client
  |
Display Reviews on UI with Pagination Controls
  |
 End
```
