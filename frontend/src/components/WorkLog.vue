<template>
  <v-container>
    <v-btn @click="fetchWorkLogs" color="primary">Load Work Logs</v-btn>
    <v-list v-for="log in workLogs" :key="log.id">
      <v-list-item>
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
      const response = await this.$http.get('worklogs/');
      this.workLogs = response.data;
    }
  }
}
</script>
