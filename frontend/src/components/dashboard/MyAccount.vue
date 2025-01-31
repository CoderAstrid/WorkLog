<template>
    <v-card>
      <v-card-title>My Account</v-card-title>
      <v-form ref="form" @submit.prevent="updateProfile">
        <v-text-field v-model="admin.name" label="Name" required></v-text-field>
        <v-text-field v-model="admin.email" label="Email" required></v-text-field>
        <v-btn color="primary" type="submit">Save Changes</v-btn>
      </v-form>
    </v-card>
  </template>
  
  <script>
  export default {
    data() {
      return {
        admin: {
          name: "",
          email: "",
        },
      };
    },
    async mounted() {
      const response = await this.$http.get("admin/profile/");
      this.admin = response.data;
    },
    methods: {
      async updateProfile() {
        await this.$http.put("admin/profile/", this.admin);
        alert("Profile updated successfully");
      },
    },
  };
  </script>
  