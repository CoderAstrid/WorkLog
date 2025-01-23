<template>
  <v-container class="green-background fill-height d-flex align-center justify-center">
    <v-card class="pa-5" max-width="800">
      <h1 class="text-center">{{ username }}'s Log</h1>
      <v-form @submit.prevent="submitWorkLog">
        <v-text-field v-model="newLog.date" label="Date" type="date" required></v-text-field>
        <v-text-field v-model="newLog.content" label="Work Content" required></v-text-field>
        <v-textarea v-model="newLog.notes" label="Notes"></v-textarea>
        <v-btn type="submit" color="primary">Add Work Log</v-btn>
      </v-form>

      <v-data-table
        :headers="headers"
        :items="workLogs"
        class="elevation-1 mt-4"
        no-data-text="No work logs available"
      ></v-data-table>
    </v-card>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      username: localStorage.getItem('username') || 'User',
      newLog: {
        date: '',
        content: '',
        notes: '',
      },
      workLogs: [],
      headers: [
        { text: 'Date', value: 'date' },
        { text: 'Work Content', value: 'content' },
        { text: 'Notes', value: 'notes' },
      ],
    };
  },
  async mounted() {
    this.fetchWorkLogs();
  },
  methods: {
    async fetchWorkLogs() {
      try {
        const response = await this.$http.get('worklogs/', {
          headers: { Authorization: `Token ${localStorage.getItem('token')}` },
        });
        this.workLogs = response.data;
      } catch (error) {
        console.error('Error fetching work logs:', error);
      }
    },
    async submitWorkLog() {
      try {
        this.newLog.user = localStorage.getItem('user_id');  // Ensure user ID is included
        await this.$http.post('add_work_log/', this.newLog, {
          headers: { Authorization: `Token ${localStorage.getItem('token')}` },
        });
        alert('Work log added successfully');
        this.fetchWorkLogs();  // Refresh table after submission
      } catch (error) {
        console.error('Error adding work log:', error.response.data);
      }
    }
  },
};
</script>

<style scoped>
.green-background {
  background-color: #4CAF50; /* Green background */
  padding: 20px;
  height: 100vh;
}
</style>
