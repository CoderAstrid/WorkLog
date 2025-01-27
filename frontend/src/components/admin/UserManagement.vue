<template>
    <v-card>
      <v-card-title>User Management</v-card-title>
      <v-data-table
        :headers="headers"
        :items="users"
        class="elevation-1"
      >
        <template #item.actions="{ item }">
          <v-btn color="primary" @click="editUser(item)">Edit</v-btn>
        </template>
      </v-data-table>
    </v-card>
  </template>
  
  <script>
  /* eslint-disable no-unused-vars */
  export default {
    data() {
      return {
        users: [],
        headers: [
          { text: "Name", value: "name" },
          { text: "Email", value: "email" },
          { text: "Role", value: "role" },
          { text: "Actions", value: "actions", sortable: false },
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
        // Redirect to user editing form
      },
    },
  };
  </script>
  