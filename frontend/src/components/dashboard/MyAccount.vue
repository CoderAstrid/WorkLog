<template>
  <v-container class="account-container">
    <v-card class="pa-5 account-card">
      <v-card-title>{{ isAdmin ? "Admin Profile" : "My Account" }}</v-card-title>
      
      <v-form ref="form" @submit.prevent="updateProfile">
        <v-text-field v-model="userProfile.username" label="User ID" required></v-text-field>
        <v-text-field v-model="userProfile.first_name" label="First Name" required></v-text-field>
        <v-text-field v-model="userProfile.last_name" label="Last Name" required></v-text-field>
        <v-text-field v-model="userProfile.email" label="Email" required></v-text-field>
        <v-text-field v-model="userProfile.password" label="New Password" type="password"></v-text-field>

        <v-btn color="primary" type="submit">Save Changes</v-btn>
        <v-btn color="red" class="ml-2" @click="resetPassword">Reset Password</v-btn>
      </v-form>
    </v-card>
  </v-container>
  
</template>

<script>
export default {
  props: {
    isAdmin: Boolean,  // Determine if this is the admin's profile
  },
  data() {
    return {
      userProfile: {
        username: "",
        first_name: "",
        last_name: "",
        email: "",
        password: "",
      },
    };
  },
  async mounted() {
    this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      try {
        const endpoint = this.isAdmin ? "admin/profile/" : "user/profile/";
        const response = await this.$http.get(endpoint, {
          headers: { Authorization: `Token ${localStorage.getItem("token")}` },
        });

        this.userProfile = {
          username: response.data.username,
          first_name: response.data.first_name,
          last_name: response.data.last_name,
          email: response.data.email,
          password: "", // Leave blank to prevent overwriting
        };
      } catch (error) {
        console.error("Error fetching user profile:", error);
      }
    },
    async updateProfile() {
      try {
        const endpoint = this.isAdmin ? "admin/profile/" : "user/profile/";
        await this.$http.put(endpoint, this.userProfile, {
          headers: { Authorization: `Token ${localStorage.getItem("token")}` },
        });
        alert("Profile updated successfully!");
      } catch (error) {
        console.error("Error updating profile:", error);
      }
    },
    async resetPassword() {
      try {
        await this.$http.post("user/reset-password/", {
          email: this.userProfile.email,
        });
        alert("Password reset link sent to email!");
      } catch (error) {
        console.error("Error sending password reset:", error);
      }
    },
  },
};
</script>
