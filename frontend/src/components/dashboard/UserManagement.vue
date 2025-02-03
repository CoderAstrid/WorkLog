<template>
  <v-card>
    <v-card-title>User Management</v-card-title>
    <v-data-table :headers="headers" :items="users" class="elevation-1">
      <template v-slot:item.full_name="{ item }">
        <span>{{ item.first_name }} {{ item.last_name }}</span>
      </template>
      <template v-slot:item.is_staff="{ item }">
        <v-checkbox
          :input-value="item.is_staff"
          readonly
          disabled
        ></v-checkbox>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-btn color="primary" @click="editUser(item)">Edit</v-btn>
        <v-btn color="error" @click="resetPassword(item)">Reset Password</v-btn>
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      users: [],
      headers: [
        { text: "No", value: "id", width: "70px" },
        { text: "ID", value: "username", width: "240px" },
        { text: "Full Name", value: "full_name", width: "240px" },    
        { text: "Email", value: "email", width: "auto" },
        { text: "Admin", value: "is_staff" },  // ✅ Show Admin column
      ],
    };
  },
  async mounted() {
    try {
      const response = await this.$http.get('admin/users/', {
        headers: { Authorization: `Token ${localStorage.getItem('token')}` },
      });
      this.users = response.data;
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  },
  methods: {
    editUser(user) {
      console.log(user.email);
    },
  },
  async resetPassword(user) {
    try {
      await this.$http.post('admin/reset-password/', { email: user.email });
      alert("Password reset email sent.");
    } catch (error) {
      alert("Error sending reset email.");
    }
  }
};
</script>
