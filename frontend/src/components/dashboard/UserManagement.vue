<template>
  <v-container fluid>
    <v-card class="pa-4">
      <v-card-title class="d-flex justify-space-between align-center">
        <h3>👥 User Management</h3>
      </v-card-title>

      <v-data-table
        :headers="headers"
        :items="users"
        class="elevation-2 mt-4"
        dense
        item-value="id"
      >
        <!-- ✅ Full Name Column -->
        <template v-slot:item.full_name="{ item }">
          <span>{{ item.first_name }} {{ item.last_name }}</span>
        </template>

        <!-- ✅ Admin Column (Yes / No) -->
        <template v-slot:item.is_staff="{ item }">
          <span class="admin-label" :class="item.is_staff ? 'admin-yes' : 'admin-no'">
            {{ item.is_staff ? "✔ Yes" : "✖ No" }}
          </span>
        </template>        
      </v-data-table>
    </v-card>
  </v-container>
</template>

<style scoped>
/* ✅ Admin Column (Yes/No) Design */
.admin-label {
  font-weight: bold;
  padding: 4px 10px;
  border-radius: 5px;
}

.admin-yes {
  color: #2E7D32; /* Green */
  background: rgba(76, 175, 80, 0.15);
}

.admin-no {
  color: #D32F2F; /* Red */
  background: rgba(211, 47, 47, 0.15);
}

/* ✅ Action Buttons */
.v-btn {
  min-width: 110px;
}
</style>

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
