 Here is a basic example of how you might structure test cases for this requirement using JUnit and Mockito in Java. Please note that this is a simplified example and may need to be adjusted based on your specific project setup, API endpoints, and device configurations.

```java
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import static org.junit.Assert.*;

@RunWith(MockitoJUnitRunner.class)
public class BatteryIndicatorTest {

    @Mock
    private BackendAPI api;

    @Test
    public void testBatteryIndicator_validInput() {
        // Given
        when(api.getBatteryStatus()).thenReturn(new BatteryStatus("100"));

        // When
        BatteryIndicator indicator = new BatteryIndicator(api);
        int batteryLevel = indicator.getCurrentBatteryLevel();

        // Then
        assertEquals(100, batteryLevel);
    }

    @Test
    public void testBatteryIndicator_invalidInput() {
        // Given
        when(api.getBatteryStatus()).thenReturn("invalid");

        // When
        BatteryIndicator indicator = new BatteryIndicator(api);
        int batteryLevel = indicator.getCurrentBatteryLevel();

        // Then
        assertNotNull(indicator.getErrorMessage());
        assertEquals(-1, batteryLevel);
    }

    @Test
    public void testBatteryIndicator_edgeCase() {
        // Given
        when(api.getBatteryStatus()).thenReturn("0");

        // When
        BatteryIndicator indicator = new BatteryIndicator(api);
        int batteryLevel = indicator.getCurrentBatteryLevel();

        // Then
        assertEquals(0, batteryLevel);
    }

    @Test
    public void testBatteryIndicator_featureFlag() {
        // Given
        when(api.getBatteryStatus()).thenReturn("100");
        // Assume feature flag is turned off (for example, by returning false)
        when(indicator.isFeatureEnabled()).thenReturn(false);

        // When
        BatteryIndicator indicator = new BatteryIndicator(api);
        int batteryLevel = indicator.getCurrentBatteryLevel();

        // Then
        assertNull(batteryLevel);
    }
}
```

This example includes tests for valid input, invalid input, an edge case (battery level at 0), and a test for the feature flag functionality. You'll need to replace `BackendAPI`, `BatteryStatus`, and `BatteryIndicator` with your actual class names and implementations. Additionally, you might want to consider adding more tests for different API failure scenarios or various edge cases based on the specific requirements of your project.