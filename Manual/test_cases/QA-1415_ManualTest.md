 - **Title:** Valid Email and Password Login for Secure Account Access
- **Preconditions:** The user has a registered account with a valid email and password. The user is a returning user. The application is launched and the login page is visible.
- **Test Steps:**
  1. Navigate to the login page of the application.
  2. Enter a valid registered email address in the email field.
  3. Enter a valid registered password in the password field.
  4. Click on the 'Login' button.
- **Expected Result:** The user should be successfully logged in and redirected to their account dashboard.

- **Title:** Invalid Credentials Login - Error Message Display
- **Preconditions:** The user has a registered account with a valid email and password. The user is a returning user. The application is launched and the login page is visible.
- **Test Steps:**
  1. Navigate to the login page of the application.
  2. Enter an incorrect email address in the email field (not a registered email).
  3. Enter a valid registered password in the password field.
  4. Click on the 'Login' button.
- **Expected Result:** An error message should be displayed indicating that the provided email is not registered or the login credentials are invalid.

- **Title:** Blank Fields Validation - "Required" Message Display
- **Preconditions:** The user has a registered account with a valid email and password. The application is launched and the login page is visible.
- **Test Steps:**
  1. Navigate to the login page of the application.
  2. Leave the email field empty.
  3. Enter a valid registered password in the password field.
  4. Click on the 'Login' button.
- **Expected Result:** A message should be displayed indicating that the email field is required and cannot be left blank. Repeat steps 2-4 for the password field to ensure password validation as well.