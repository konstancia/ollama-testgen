 **Test Case 1: Verifying Correct Rendering of Battery States**

- **Title**: Verification of Correct Rendering of Battery States
- **Preconditions**: The iOS app is installed and running, the feature flag for battery indicator is enabled.
- **Test Steps**:
    1. Open the iOS app on a device.
    2. Observe the battery indicator within the app.
    3. Check if the following states are correctly represented:
        - Full Battery (100%)
        - Medium Battery (50-99%)
        - Low Battery (10-49%)
        - Critical Battery (<10%)
    4. For each state, record the visual representation of the battery level.
- **Expected Result**: The battery indicator correctly renders all four visual states as defined in the requirement.

**Test Case 2: Verifying Usage of Backend API for Battery Status**

- **Title**: Verification of Using Backend API for Battery Status
- **Preconditions**: The iOS app is installed and running, the feature flag for battery indicator is enabled, internet connection is available.
- **Test Steps**:
    1. Open the iOS app on a device with an internet connection.
    2. Observe the battery indicator within the app.
    3. Check if the battery level updates when the battery status changes (e.g., charging, discharging).
    4. Record the visual representation of the battery level at various intervals during the test case.
- **Expected Result**: The battery indicator updates correctly and pulls data from the backend API to display the current battery status.

**Test Case 3: Verifying Handling of API Failure Gracefully**

- **Title**: Verification of Handling API Failure Gracefully
- **Preconditions**: The iOS app is installed and running, the feature flag for battery indicator is enabled, internet connection is unavailable or API call fails.
- **Test Steps**:
    1. Open the iOS app on a device without an internet connection or simulate an API failure.
    2. Observe the battery indicator within the app.
    3. Check if the battery indicator shows a grayed-out state indicating that the API call failed.
- **Expected Result**: When the API fails, the battery indicator correctly displays a grayed-out state instead of showing an incorrect battery level.