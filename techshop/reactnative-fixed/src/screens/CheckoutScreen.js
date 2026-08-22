import React, { useState } from 'react';
import {
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  KeyboardAvoidingView,
  ScrollView,
  Platform,
  Keyboard,
} from 'react-native';
import { useCart } from '../context/CartContext';

const FIELDS = [
  { key: 'firstName', label: 'First Name', keyboard: 'default' },
  { key: 'lastName', label: 'Last Name', keyboard: 'default' },
  { key: 'email', label: 'Email', keyboard: 'email-address' },
  { key: 'phone', label: 'Phone', keyboard: 'number-pad' },
  { key: 'card', label: 'Card Number', keyboard: 'number-pad' },
  { key: 'expiry', label: 'Expiry (MM/YY)', keyboard: 'default' },
  // FIXED (BUG-010): CVV uses the numeric keypad.
  { key: 'cvv', label: 'CVV', keyboard: 'number-pad' },
];

function isExpiryInPast(mmYY) {
  const m = /^(\d{2})\/(\d{2})$/.exec(mmYY);
  if (!m) return true;
  const month = parseInt(m[1], 10);
  const year = 2000 + parseInt(m[2], 10);
  if (month < 1 || month > 12) return true;
  const now = new Date();
  const expiry = new Date(year, month, 0, 23, 59, 59); // last day of expiry month
  return expiry < now;
}

export default function CheckoutScreen({ navigation }) {
  const { total, clearCart } = useCart();
  const [form, setForm] = useState({});
  const [error, setError] = useState('');

  function update(key, value) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

  function validate() {
    // FIXED (BUG-012): every field is required.
    for (const f of FIELDS) {
      if (!form[f.key] || !form[f.key].trim()) {
        return 'All fields are required';
      }
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) return 'Enter a valid email';
    if (!/^\d{10}$/.test(form.phone)) return 'Phone must be 10 digits';
    if (!/^\d{16}$/.test(form.card)) return 'Card number must be 16 digits';
    // FIXED (BUG-009): reject past expiry dates.
    if (isExpiryInPast(form.expiry)) return 'Expiry date must not be in the past';
    // FIXED (BUG-010): CVV must be exactly 3 digits.
    if (!/^\d{3}$/.test(form.cvv)) return 'CVV must be 3 digits';
    return '';
  }

  function onSubmit() {
    Keyboard.dismiss();
    const problem = validate();
    if (problem) {
      setError(problem);
      return;
    }
    setError('');
    const orderRef = 'TS-' + Math.floor(100000 + Math.random() * 900000);
    clearCart();
    navigation.navigate('Confirmation', { orderRef, total });
  }

  // FIXED (BUG-017): KeyboardAvoidingView + ScrollView keep the focused
  // field (including CVV at the bottom) visible above the keyboard.
  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      keyboardVerticalOffset={Platform.OS === 'ios' ? 100 : 0}
    >
      <ScrollView
        contentContainerStyle={styles.scroll}
        keyboardShouldPersistTaps="handled"
      >
        <Text style={styles.heading}>Checkout</Text>

        {FIELDS.map((f) => (
          <TextInput
            key={f.key}
            testID={`checkout-${f.key}`}
            accessibilityLabel={f.label}
            style={styles.input}
            placeholder={f.label}
            keyboardType={f.keyboard}
            autoCapitalize="none"
            value={form[f.key] || ''}
            onChangeText={(v) => update(f.key, v)}
            returnKeyType={f.key === 'cvv' ? 'done' : 'next'}
            onSubmitEditing={f.key === 'cvv' ? onSubmit : undefined}
          />
        ))}

        {error ? (
          <Text testID="checkout-error" style={styles.error}>
            {error}
          </Text>
        ) : null}

        <TouchableOpacity testID="checkout-submit" style={styles.button} onPress={onSubmit}>
          <Text style={styles.buttonText}>Place Order</Text>
        </TouchableOpacity>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
  scroll: { padding: 16, paddingBottom: 250 },
  heading: { fontSize: 22, fontWeight: '800', color: '#1a1442', marginBottom: 12 },
  input: { borderWidth: 1, borderColor: '#ccc', borderRadius: 10, padding: 12, fontSize: 15, marginBottom: 10 },
  error: { color: '#c0392b', marginBottom: 10 },
  button: { backgroundColor: '#3b2fb5', padding: 16, borderRadius: 10, alignItems: 'center', marginTop: 6 },
  buttonText: { color: '#fff', fontSize: 17, fontWeight: '700' },
});
