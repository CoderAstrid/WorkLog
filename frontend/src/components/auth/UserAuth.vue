<template>
  <div class="login-container">
    <!-- Background Video -->
    <video class="background-video" autoplay muted loop playsinline>
      <source src="/videos/typing.mp4" type="video/mp4" />
      Your browser does not support HTML5 video.
    </video>
    <!-- Dark Overlay -->
    <div class="overlay"></div>
    <!-- Centered Login Form -->
    <v-container class="fill-height d-flex align-center justify-center">
      <v-card class="pa-5 login-form">
        <v-tabs v-model="tab">
          <v-tab>Login</v-tab>
          <v-tab>Register</v-tab>
          <v-tab>Forgot Password</v-tab>
        </v-tabs>
        <v-tabs-items v-model="tab">
          <!-- Login Form -->
          <v-tab-item>
            <v-form @submit.prevent="login">
              <v-text-field v-model="loginData.username" label="User ID" required></v-text-field>
              <v-text-field v-model="loginData.password" label="Password" type="password" required></v-text-field>
              <v-btn type="submit" color="primary" block>Login</v-btn>
            </v-form>
          </v-tab-item>

          <!-- Registration Form -->
          <v-tab-item>
            <v-form @submit.prevent="register">
              <v-text-field v-model="registerData.username" label="User ID" required></v-text-field>
              <v-text-field v-model="registerData.first_name" label="First Name" required></v-text-field>
              <v-text-field v-model="registerData.last_name" label="Last Name" required></v-text-field>
              <v-text-field v-model="registerData.email" label="Email" type="email" required></v-text-field>
              <v-checkbox
                v-model="registerData.is_admin"
                label="Register as Admin"
                color="primary"
                hide-details
                dense  
                class="align-checkbox"              
              ></v-checkbox>
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
  </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        tab: 0,
        loginData: { username: '', password: '' },
        registerData: { username: '', email: '', password: '', is_admin: false },
        forgotData: { email: '' }
      };
    },
    methods: {
      async login() {
        try {
          console.log("Sending login request:", this.loginData);
          const response = await this.$http.post('login/', this.loginData);
          console.log("Response received:", response.data);
          localStorage.setItem('token', response.data.token);
          localStorage.setItem('role', response.data.role);  // Ensure role is stored
          if (response.data.role === 'admin') {
            this.$router.push('/admin');
            console.log("admin");
          } else {
            this.$router.push('/worklog');
            console.log("worklog");
          }
        } catch (error) {
          alert(error.response?.data?.error || 'Login failed');
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
 