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
      <v-card class="pa-6 login-form">
        <!-- Tabs for Login, Register, Forgot Password -->
        <v-tabs v-model="tab" grow class="tab-container">
          <v-tab><v-icon left>mdi-login</v-icon> LOGIN</v-tab>
          <v-tab><v-icon left>mdi-account-plus</v-icon> REGISTER</v-tab>
          <v-tab><v-icon left>mdi-lock-reset</v-icon> FORGOT PASSWORD</v-tab>
        </v-tabs>

        <v-tabs-items v-model="tab">
          <!-- Login Form -->
          <v-tab-item>
            <v-form @submit.prevent="login">
              <v-text-field v-model="loginData.username" label="User ID" class="input-box"></v-text-field>
              <v-text-field v-model="loginData.password" label="Password" type="password" class="input-box"></v-text-field>
              <v-btn type="submit" color="primary" block class="action-btn">LOGIN</v-btn>
            </v-form>
          </v-tab-item>

          <!-- Registration Form -->
          <v-tab-item>
            <v-form @submit.prevent="register">
              <v-text-field v-model="registerData.username" label="User ID" class="input-box"></v-text-field>
              <v-text-field v-model="registerData.first_name" label="First Name" class="input-box"></v-text-field>
              <v-text-field v-model="registerData.last_name" label="Last Name" class="input-box"></v-text-field>
              <v-text-field v-model="registerData.email" label="Email" type="email" class="input-box"></v-text-field>
              <v-checkbox v-model="registerData.is_admin" label="Register as Admin" class="align-checkbox"></v-checkbox>
              <v-text-field v-model="registerData.password" label="Password" type="password" class="input-box"></v-text-field>
              <v-btn type="submit" color="success" block class="action-btn">REGISTER</v-btn>
            </v-form>
          </v-tab-item>

          <!-- Forgot Password Form -->
          <v-tab-item>
            <v-form @submit.prevent="forgotPassword">
              <v-text-field v-model="forgotData.email" label="Enter your email" type="email" class="input-box"></v-text-field>
              <v-btn type="submit" color="warning" block class="action-btn">RESET PASSWORD</v-btn>
            </v-form>
          </v-tab-item>
        </v-tabs-items>
      </v-card>
    </v-container>
  </div>
</template>

<style scoped>
/* ✅ Background Video */
.background-video {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.6;
  z-index: 0;
}

/* ✅ Dark Overlay for Better Readability */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  z-index: 1;
}

/* ✅ Centered Login Form */
.login-form {
  position: relative;
  z-index: 2;
  max-width: 450px;
  width: 100%;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.3);
}

/* ✅ Tabs Styling */
.tab-container {
  background: #f5f5f5;
  border-radius: 12px 12px 0 0;
  font-weight: bold;
}

/* ✅ Input Field Styling */
.input-box {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  margin-bottom: 16px; /* Ensure consistent spacing */
}

/* ✅ Ensure Consistent Input Padding */
.v-input__control {
  min-height: 50px !important;
}

/* ✅ Button Styling */
.action-btn {
  font-weight: bold;
  letter-spacing: 0.5px;
  padding: 12px;
  border-radius: 8px;
  margin-top: 10px;
}

/* ✅ Align Checkbox */
.align-checkbox {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 10px;
}
</style>

<script>
export default {
  data() {
    return {
      tab: 0,
      loginData: { username: "", password: "" },
      registerData: { username: "", first_name: "", last_name: "", email: "", password: "", is_admin: false },
      forgotData: { email: "" },
    };
  },
  methods: {
    async login() {
      try {
        console.log("Sending login request:", this.loginData);
        const response = await this.$http.post("login/", this.loginData);
        console.log("Response received:", response.data);
        localStorage.setItem("token", response.data.token);
        localStorage.setItem("role", response.data.role);

        if (response.data.role === "admin") {
          this.$router.push("/admin");
        } else {
          this.$router.push("/worklog");
        }
      } catch (error) {
        alert(error.response?.data?.error || "Login failed");
      }
    },
    async register() {
      try {
        const response = await this.$http.post("register/", this.registerData);
        console.log(response.data);
        alert("Registration successful");
      } catch (error) {
        alert("Registration failed");
      }
    },
    async forgotPassword() {
      try {
        await this.$http.post("forgot-password/", this.forgotData);
        alert("Password reset link sent!");
      } catch (error) {
        alert("Error sending reset link");
      }
    },
  },
};
</script>
