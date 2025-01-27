<template>
    <v-card>
      <v-card-title>All Work Logs</v-card-title>
      <v-data-table
        :headers="headers"
        :items="workLogs"
        class="elevation-1"
      >
        <template #item.actions="{ item }">
          <v-btn color="primary" @click="editLog(item)">Edit</v-btn>
        </template>
      </v-data-table>
    </v-card>
  </template>
  
  <script>
  /* eslint-disable no-unused-vars */
  export default {
    data() {
      return {
        workLogs: [],
        headers: [
          { text: "Date", value: "date" },
          { text: "User", value: "user" },
          { text: "Work Content", value: "content" },
          { text: "Actions", value: "actions", sortable: false },
        ],
      };
    },
    async mounted() {
      try {
        const response = await this.$http.get('admin/worklogs/', {
          headers: { Authorization: `Token ${localStorage.getItem('token')}` },
        });
        this.workLogs = response.data;
      } catch (error) {
        console.error('Error fetching work logs:', error);
      }
    },
    methods: {
      editLog(log) {
        // Redirect to log editing page
      },
    },
  };
  </script>
  