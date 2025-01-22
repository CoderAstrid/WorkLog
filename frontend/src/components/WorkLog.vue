<template>
  <v-container>
    <h1>Your Work Logs</h1>
    <v-btn color="primary" @click="fetchWorkLogs">Load Work Logs</v-btn>
    <v-list v-if="workLogs.length">
      <v-list-item v-for="log in workLogs" :key="log.id">
        <v-list-item-content>
          <v-list-item-title>{{ log.date }} - {{ log.content }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      workLogs: []
    };
  },
  methods: {
    async fetchWorkLogs() {
      try {
        const response = await this.$http.get('worklogs/', {
          headers: { Authorization: `Token ${localStorage.getItem('token')}` }
        });
        this.workLogs = response.data;
      } catch (error) {
        console.error('Error fetching work logs:', error);
      }
    }
  }
};
</script>
