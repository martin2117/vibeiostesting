import React, { useState } from 'react';
import {
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  KeyboardAvoidingView,
  ScrollView,
  Platform,
} from 'react-native';
import { useAuth } from '../context/AuthContext';

export default function LoginScreen() {
  const { login, error } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  function onSubmit() {
    login(email, password);
  }

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <ScrollView
        contentContainerStyle={styles.scroll}
        keyboardShouldPersistTaps="handled"
      >
        <Text style={styles.brand}>TechShop</Text>
        <Text style={styles.subtitle}>Sign in to continue</Text>

        <TextInput
          testID="login-email"
          accessibilityLabel="Email"
          style={styles.input}
          placeholder="Email"
          autoCapitalize="none"
          autoCorrect={false}
          spellCheck={false}
          keyboardType="email-address"
          value={email}
          onChangeText={setEmail}
        />

        {/* FIXED (BUG-001): secureTextEntry masks the password. */}
        <TextInput
          testID="login-password"
          accessibilityLabel="Password"
          style={styles.input}
          placeholder="Password"
          secureTextEntry={true}
          autoCorrect={false}
          spellCheck={false}
          value={password}
          onChangeText={setPassword}
          onSubmitEditing={onSubmit}
        />

        {error ? (
          <Text testID="login-error" style={styles.error}>
            {error}
          </Text>
        ) : null}

        {/* FIXED (BUG-016): the button now has a stable accessibility identifier. */}
        <TouchableOpacity testID="login-submit" style={styles.button} onPress={onSubmit}>
          <Text style={styles.buttonText}>Log In</Text>
        </TouchableOpacity>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
  scroll: { flexGrow: 1, justifyContent: 'center', padding: 24 },
  brand: { fontSize: 34, fontWeight: '800', color: '#3b2fb5', textAlign: 'center' },
  subtitle: { fontSize: 16, color: '#666', textAlign: 'center', marginBottom: 28 },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 10,
    padding: 14,
    fontSize: 16,
    marginBottom: 14,
  },
  error: { color: '#c0392b', marginBottom: 12 },
  button: {
    backgroundColor: '#3b2fb5',
    padding: 16,
    borderRadius: 10,
    alignItems: 'center',
    marginTop: 8,
  },
  buttonText: { color: '#fff', fontSize: 17, fontWeight: '700' },
});
