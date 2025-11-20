"""
Circular Protocol Python SDK Helper Function Tests

Tests for utility functions in the _helpers module including:
- Encoding functions (hex_fix, string_to_hex, hex_to_string)
- Timestamp formatting
- Error handling
- Transaction polling
"""

import pytest
from datetime import datetime
from circular_protocol_api._helpers import (
    hex_fix,
    string_to_hex,
    hex_to_string,
    pad_number,
    get_formatted_timestamp,
    get_error,
)


class TestEncodingHelpers:
    """Test encoding and decoding helper functions"""

    def test_hex_fix_removes_0x_prefix(self):
        """Should remove 0x prefix from hex strings"""
        assert hex_fix('0x1234ab') == '1234ab'
        assert hex_fix('0X1234AB') == '1234AB'

    def test_hex_fix_handles_no_prefix(self):
        """Should pass through strings without prefix"""
        assert hex_fix('1234ab') == '1234ab'
        assert hex_fix('ABCD') == 'ABCD'

    def test_string_to_hex_converts_correctly(self):
        """Should convert strings to hex encoding"""
        assert string_to_hex('abc') == '616263'
        assert string_to_hex('Hello') == '48656c6c6f'
        assert string_to_hex('') == ''

    def test_hex_to_string_converts_correctly(self):
        """Should convert hex to strings"""
        assert hex_to_string('616263') == 'abc'
        assert hex_to_string('48656c6c6f') == 'Hello'
        assert hex_to_string('0x616263') == 'abc'  # Should handle 0x prefix

    def test_roundtrip_string_hex_conversion(self):
        """Should maintain data integrity in roundtrip conversion"""
        original = 'Circular Protocol Test Message 🚀'
        hex_encoded = string_to_hex(original)
        decoded = hex_to_string(hex_encoded)
        assert decoded == original

    def test_hex_conversion_with_special_characters(self):
        """Should handle special characters correctly"""
        special_str = '{"key": "value", "num": 123}'
        hex_ver = string_to_hex(special_str)
        decoded = hex_to_string(hex_ver)
        assert decoded == special_str


class TestNumberPadding:
    """Test number padding helpers"""

    def test_pad_number_adds_leading_zero(self):
        """Should pad single digits with leading zeros"""
        assert pad_number(1) == '01'
        assert pad_number(9) == '09'

    def test_pad_number_preserves_double_digits(self):
        """Should not modify double digit numbers"""
        assert pad_number(10) == '10'
        assert pad_number(99) == '99'

    def test_pad_number_custom_length(self):
        """Should pad to custom length"""
        assert pad_number(1, 3) == '001'
        assert pad_number(42, 4) == '0042'
        assert pad_number(999, 5) == '00999'


class TestTimestampFormatting:
    """Test timestamp generation"""

    def test_get_formatted_timestamp_returns_correct_format(self):
        """Should return timestamp in YYYY:MM:DD-hh:mm:ss format"""
        timestamp = get_formatted_timestamp()
        
        # Check format pattern
        assert len(timestamp) == 19
        assert timestamp[4] == ':'
        assert timestamp[7] == ':'
        assert timestamp[10] == '-'
        assert timestamp[13] == ':'
        assert timestamp[16] == ':'

    def test_get_formatted_timestamp_contains_valid_values(self):
        """Should contain valid date/time components"""
        timestamp = get_formatted_timestamp()
        parts = timestamp.replace(':', '-').split('-')
        
        year, month, day, hour, minute, second = map(int, parts)
        
        assert 2025 <= year <= 2100
        assert 1 <= month <= 12
        assert 1 <= day <= 31
        assert 0 <= hour <= 23
        assert 0 <= minute <= 59
        assert 0 <= second <= 59

    def test_get_formatted_timestamp_is_current(self):
        """Should generate timestamp close to current time"""
        before = datetime.utcnow()
        timestamp = get_formatted_timestamp()
        after = datetime.utcnow()
        
        # Extract year from timestamp
        year = int(timestamp.split(':')[0])
        
        assert before.year <= year <= after.year


class TestErrorHelpers:
    """Test error code helpers"""

    def test_get_error_returns_known_codes(self):
        """Should return error messages for known codes"""
        assert get_error(100) == 'Success'
        assert get_error(117) == 'Invalid Payload'
        assert get_error(119) == 'Invalid Signature'
        assert get_error(121) == 'Invalid Nonce'
        assert get_error(404) == 'Not Found'
        assert get_error(500) == 'Internal Server Error'

    def test_get_error_handles_unknown_codes(self):
        """Should return generic message for unknown codes"""
        result = get_error(999)
        assert 'Unknown error code: 999' in result

        result = get_error(42)
        assert 'Unknown error code: 42' in result


class TestHexProcessing:
    """Test advanced hex processing scenarios"""

    def test_hex_fix_empty_string(self):
        """Should handle empty strings"""
        assert hex_fix('') == ''

    def test_hex_to_string_handles_long_hex(self):
        """Should handle long hex strings correctly"""
        # Long message
        original = 'a' * 1000
        hex_ver = string_to_hex(original)
        decoded = hex_to_string(hex_ver)
        assert decoded == original
        assert len(hex_ver) == len(original) * 2  # Each char = 2 hex digits

    def test_hex_encoding_preserves_unicode(self):
        """Should correctly encode/decode unicode characters"""
        unicode_str = '你好世界 🌍'
        hex_ver = string_to_hex(unicode_str)
        decoded = hex_to_string(hex_ver)
        assert decoded == unicode_str


class TestHelperIntegration:
    """Test helper functions working together"""

    def test_transaction_payload_preparation(self):
        """Should prepare transaction payload correctly"""
        # Simulate preparing a transaction payload
        payload_data = '{"action": "transfer", "amount": 100}'
        payload_hex = string_to_hex(payload_data)
        
        # Remove any 0x prefix if added by accident
        clean_hex = hex_fix(payload_hex)
        
        # Verify it can be decoded back
        decoded_payload = hex_to_string(clean_hex)
        assert decoded_payload == payload_data

    def test_timestamp_consistency(self):
        """Should generate consistent timestamp format"""
        timestamps = [get_formatted_timestamp() for _ in range(5)]
        
        # All should have same format
        for ts in timestamps:
            assert len(ts) == 19
            assert ts.count(':') == 4
            assert ts.count('-') == 1
