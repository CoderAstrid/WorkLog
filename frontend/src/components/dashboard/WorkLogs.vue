<template>
  <v-container fluid>
    <v-card>
      <v-card-title>All Work Logs</v-card-title>
      <v-data-table
        v-model="selectedLogs"
        :headers="headers"
        :items="workLogs"
        item-value="id"
        class="elevation-1 mt-4"
        show-select
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
      </v-data-table>
    </v-card>
    <v-dialog v-model="confirmDeleteDialog" max-width="400px">
      <v-card>
        <v-card-title class="headline">Confirm Deletion</v-card-title>
        <v-card-text>
          Are you sure you want to delete the selected work logs?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" text @click="confirmDeleteDialog = false">Cancel</v-btn>
          <v-btn color="red" text @click="deleteSelectedLogs">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
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
        selectedLogs: [],  // Store selected log IDs
        workLogs: [],
        headers: [
          { text: "", value: "data-table-select", width: "30px" },  // Checkbox Column
          { text: "Date", value: "date", width: "120px" },
          { text: "ID", value: "username", width: "240px" },  // ✅ Change value to user__username
          { text: "Full Name", value: "full_name", width: "240px" },  // ✅ Change value to user__username    
          { text: "Work Content", value: "content", width: "auto" },
          { text: "Notes", value: "notes", width: "auto" },
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
  };
  </script>
  