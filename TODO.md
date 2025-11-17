# Python SDK - TODO

## Missing Utility Methods

~~Add the following utility methods to match Dart SDK:~~

### Configuration Methods
- [x] `set_header(key: str, value: str) -> None` - Set custom HTTP headers ✅ **COMPLETED**

### Lifecycle Methods
- [x] `dispose() -> None` - Clean up resources (HTTP session, etc.) ✅ **COMPLETED**

## Notes
- Python now has 44 public methods (was 42)
- Dart has 46 public methods
- All critical utility methods have been implemented
- Python already has most utility methods that TypeScript is missing

## Implementation Details

Both methods have been added to `src/circular_protocol_api/client.py`:

1. **set_header()** - Lines 285-302
   - Allows setting custom HTTP headers for all API requests
   - Headers are stored in `self.headers` dict and merged in `_make_request()`

2. **dispose()** - Lines 304-321
   - Properly closes the HTTP session to free resources
   - Should be called when done using the API client
