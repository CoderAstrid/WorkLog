<template>
  <v-container fluid>
    <v-card>
      <v-card-title>All Work Logs</v-card-title>
      <v-data-table
        :headers="headers"
        :items="workLogs"
        class="elevation-1"
        dense
      >
        <template v-slot:item.full_name="{ item }">
          <span>{{ item.first_name }} {{ item.last_name }}</span>
        </template>

        <template v-slot:item.content="{ item }">
          <pre class="multiline-text">{{ item.content }}</pre>
        </template>

        <template v-slot:item.notes="{ item }">
          <pre class="multiline-text">{{ item.notes }}</pre>
        </template>

        <template v-slot:item.actions="{ item }">
          <v-btn color="primary" @click="editLog(item)">Edit</v-btn>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<style scoped>
/* Ensures multi-line text wraps properly */
.multiline-text {
  white-space: pre-wrap;  /* Keeps line breaks */
  word-wrap: break-word;  /* Prevents overflow */
  max-width: 100%;
}
</style>
  
  <script>
  /* eslint-disable no-unused-vars */
  export default {
    data() {
      return {
        workLogs: [],
        headers: [
          { text: "Date", value: "date", width: "120px" },
          { text: "ID", value: "username", width: "240px" },  // ✅ Change value to user__username
          { text: "Full Name", value: "full_name", width: "240px" },  // ✅ Change value to user__username    
          { text: "Work Content", value: "content", width: "auto" },
          { text: "Notes", value: "notes", width: "auto" },
          { text: "Actions", value: "actions", sortable: false, width: "120px" },
        ],
      };
    },
    async mounted() {
      try {
        const token = localStorage.getItem('token');
        const response = await this.$http.get('admin/worklogs/', {
            headers: { Authorization: `Token ${token}` }
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
  