<template>
    <v-container>
      <v-card>
        <v-card-title>Reset Password</v-card-title>
        <v-form @submit.prevent="resetPassword">
          <v-text-field v-model="new_password" label="New Password" type="password" required></v-text-field>
          <v-btn type="submit" color="primary">Reset Password</v-btn>
        </v-form>
      </v-card>
    </v-container>
  </template>
  
  <script>
  export default {
    data() {
      return { new_password: '' };
    },
    methods: {
      async resetPassword() {
        try {
          await this.$http.post(`reset-password/${this.$route.params.token}/`, { new_password: this.new_password });
          alert('Password reset successful');
          this.$router.push('/login');
        } catch (error) {
          alert('Error resetting password');
        }
      }
    }
  };
  </script>
  