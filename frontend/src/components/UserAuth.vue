<template>
    <v-container class="fill-height d-flex align-center justify-center">
      <v-card class="pa-5" max-width="400">
        <v-tabs v-model="tab">
          <v-tab>Login</v-tab>
          <v-tab>Register</v-tab>
          <v-tab>Forgot Password</v-tab>
        </v-tabs>
  
        <v-tabs-items v-model="tab">
          <!-- Login Form -->
          <v-tab-item>
            <v-form @submit.prevent="login">
              <v-text-field v-model="loginData.username" label="Username" required></v-text-field>
              <v-text-field v-model="loginData.password" label="Password" type="password" required></v-text-field>
              <v-btn type="submit" color="primary" block>Login</v-btn>
            </v-form>
          </v-tab-item>
  
          <!-- Registration Form -->
          <v-tab-item>
            <v-form @submit.prevent="register">
              <v-text-field v-model="registerData.username" label="Username" required></v-text-field>
              <v-text-field v-model="registerData.email" label="Email" type="email" required></v-text-field>
              <v-text-field v-model="registerData.password" label="Password" type="password" required></v-text-field>
              <v-btn type="submit" color="primary" block>Register</v-btn>
            </v-form>
          </v-tab-item>
  
          <!-- Forgot Password Form -->
          <v-tab-item>
            <v-form @submit.prevent="forgotPassword">
              <v-text-field v-model="forgotData.email" label="Enter your email" type="email" required></v-text-field>
              <v-btn type="submit" color="primary" block>Reset Password</v-btn>
            </v-form>
          </v-tab-item>
        </v-tabs-items>
      </v-card>
    </v-container>
  </template>
  
  <script>
  export default {
    data() {
      return {
        tab: 0,
        loginData: { username: '', password: '' },
        registerData: { username: '', email: '', password: '' },
        forgotData: { email: '' }
      };
    },
    methods: {
      async login() {
        try {
          const response = await this.$http.post('login/', this.loginData);
          localStorage.setItem('token', response.data.token);
          this.$router.push('/worklog');
        } catch (error) {
          alert('Login failed');
        }
      },
      async register() {
        try {
          const response = await this.$http.post('register/', this.registerData);
          console.log(response.data);  // Display response in console
          alert('Registration successful');
        } catch (error) {
          alert('Registration failed');
        }
      },
      async forgotPassword() {
        try {
          await this.$http.post('forgot-password/', this.forgotData);
          // console.log(response.data);  // Display response in console
          alert('Password reset link sent!');
        } catch (error) {
          alert('Error sending reset link');
        }
      }
    }
  };
  </script>
  