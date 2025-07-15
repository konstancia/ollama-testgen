 Here's a simple example of JUnit tests for your requirement using Java. Please note that this is a basic implementation, and you might need to adjust it according to your project structure and specifics.

```java
package com.example;

import org.junit.Assert;
import org.junit.Test;
import static org.junit.Assert.*;

public class HackathonLoginTest {

    private final LoginService loginService = new LoginService();

    @Test
    public void testValidEmailAndPassword() {
        String email = "valid@email.com";
        String password = "securePassword";
        boolean result = loginService.login(email, password);
        assertTrue("Login should be successful", result);
    }

    @Test
    public void testInvalidCredentials() {
        String email = "invalidEmail";
        String password = "wrongPassword";
        boolean result = loginService.login(email, password);
        assertFalse("Login should fail with invalid credentials", result);
    }

    @Test
    public void testBlankFields() {
        String email = "";
        String password = "";
        boolean result = loginService.login(email, password);
        assertFalse("Login should fail with blank fields", result);
    }

    @Test
    public void testEmptyEmail() {
        String email = null;
        String password = "validPassword";
        boolean result = loginService.login(email, password);
        assertFalse("Login should fail with empty email", result);
    }

    @Test
    public void testEmptyPassword() {
        String email = "validEmail@example.com";
        String password = null;
        boolean result = loginService.login(email, password);
        assertFalse("Login should fail with empty password", result);
    }
}
```

This example includes tests for valid input (valid email and password), invalid input (invalid credentials), blank fields, edge cases (empty email and empty password). The `LoginService` class would be the one responsible for handling the login process.